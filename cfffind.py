from importlib import metadata
import json
from pathlib import Path
import pkg_resources
import re
import requests
import subprocess
import yaml

import click


GITHUB_URL_PATTERN = "https://github\.com/[^/]+/[^/,]+"


@click.command()
@click.option('--output', '-o',
              type=click.Path(writable=True),
              default=Path("references.cff"),
              help="File to write citations to.")
@click.option('--summary/--no-summary', default=True)
@click.option('--warnings/--no-warnings', default=True)
def cfffind(output, summary, warnings):
    dependencies_with_versions = json.loads(
        subprocess.run(["conda", "env", "export", "--from-history", "--json"], text=True, capture_output=True).stdout
    )["dependencies"]
    dependencies = [dependency.split("=")[0] for dependency in dependencies_with_versions]

    installed_packages = [d.project_name for d in pkg_resources.working_set]

    not_found_dependencies = set(dependencies)
    primary_packages = []
    for package in installed_packages:
        installer = metadata.distribution(package).read_text("INSTALLER")
        if installer != "conda":
            continue
        try:
            path_url = json.loads(metadata.distribution(package).read_text("direct_url.json"))["url"]
            for dependency in not_found_dependencies:
                if dependency in path_url:
                    not_found_dependencies.remove(dependency)
                    primary_packages.append(package)
                    break
        except TypeError:
            if warnings:
                click.echo(f"Info: Package {package} is installed through conda, but does not have a valid `direct_url.json` file.")

    github_urls = []
    no_github_packages = []
    for package in installed_packages:
        package_metadata = metadata.metadata(package).json

        project_info = package_metadata.get('project_url', [])
        download_url = package_metadata.get('download_url', "")
        home_page = package_metadata.get('home_page', "")
        relevant_data = project_info + [download_url] + [home_page]
        mess = ", ".join(relevant_data)

        match = re.search(GITHUB_URL_PATTERN, mess)
        if match:
            github_urls.append(match.group())
        else:
            no_github_packages.append(package)

    citation_urls = []
    for url in github_urls:
        repository = "/".join(url.split("/")[3:])
        branch = "main"

        api_url = f"https://api.github.com/repos/{repository}/contents"

        response = requests.get(f"{api_url}?ref={branch}")

        if response.status_code == 200:
            files = response.json()

            for file in files:
                if file["name"].startswith("CITATION"):
                    citation_urls.append(file["download_url"])

    citation_output_file = {"references": []}
    for url in citation_urls:
        response = requests.get(url)

        if response.status_code == 200:
            citation_yaml = yaml.safe_load(response.text)
            citation_output_file["references"].append(citation_yaml)
            click.echo(citation_yaml)

    with open(output, "w", encoding="utf-8") as file:
        yaml.dump(citation_output_file, file, allow_unicode=True)

    if summary:
        click.echo("Summary:")
        click.echo(f"{len(primary_packages)} detected.")
        click.echo(f"{len(github_urls)} of total {len(installed_packages)} packages with Github url.")
        click.echo(f"{len(citation_urls)} of total {len(github_urls)} package with Github url has citation file.")


if __name__ == "__main__":
    cfffind()
