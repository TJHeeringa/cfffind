from importlib import metadata
import pkg_resources
import re
import requests

import click


GITHUB_URL_PATTERN = "https://github\.com/[^/]+/[^/,]+"


@click.command()
def cfffind():
    installed_packages = [(d.project_name, d.version) for d in pkg_resources.working_set]
    github_urls = []
    no_github_packages = []
    for (package, version) in installed_packages:
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

    for url in github_urls:
        repository = "/".join(url.split("/")[3:])
        branch = "main"

        api_url = f"https://api.github.com/repos/{repository}/contents"

        response = requests.get(f"{api_url}?ref={branch}")

        if response.status_code == 200:
            files = response.json()

            for file in files:
                if file["name"].startswith("CITATION"):
                    print(file["download_url"])


if __name__ == "__main__":
    cfffind()
