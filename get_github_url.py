import re
import requests
from urllib.parse import urlparse
from importlib import metadata

import click


def get_citations_cff_from_github(github_url: str) -> None:
    response = requests.get(f"{github_url}/raw/main/CITATION.cff")

    if response.status_code == 200:
        # Save the content of the CITATIONS.cff file to a local file.
        with open("CITATION.cff", "wb") as file:
            file.write(response.content)
        print("CITATION.cff file downloaded successfully.")
    else:
        print("Failed to download CITATION.cff file.")

    print(response.request.url)


@click.command()
@click.argument('package_name')
def get_github_url(package_name):
    try:
        metadata_json = metadata.metadata(package_name).json

        home_page = metadata_json.get("home_page", "")
        download_url = metadata_json.get("download_url", "")

        # Define a regular expression pattern to match GitHub URLs.
        github_url_pattern = r"https://github\.com/[^/]+/[^/]+"
        github_url = None

        def _extract_github_url(url):
            parsed_url = urlparse(url)
            if parsed_url.netloc == 'github.com':
                parts = parsed_url.path.strip('/').split('/')
                if len(parts) >= 2:
                    return f"https://github.com/{parts[0]}/{parts[1]}"
            return None

        # Check if either the homepage or download URL matches the GitHub URL pattern.
        if re.match(github_url_pattern, home_page):
            github_url = _extract_github_url(home_page)
        elif re.match(github_url_pattern, download_url):
            github_url = _extract_github_url(download_url)

        if github_url:
            print(f"The GitHub repository URL for package '{package_name}' is: {github_url}")
        else:
            print(f"No GitHub repository found for package '{package_name}'.")
    except metadata.PackageNotFoundError:
        print(f"No metadata found for package '{package_name}'")


if __name__ == "__main__":
    get_github_url()
