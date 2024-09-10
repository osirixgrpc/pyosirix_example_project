__version__ = "0.0.1-dev.35"
__author__ = "Matthew D Blackledge"
__maintainer__ = "Matthew D Blackledge"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2024, Matthew D Blackledge"
__url__ = "https://github.com/osirixgrpc/pyosirix_example_project"
__git_hash__ = "HASH_PLACEHOLDER"  # Updated by GitHub Actions prior to packaging

from pyosirix_example import server, client, utilities


def _fetch_latest_github_commit_hash() -> str:
    """ Fetch the latest commit hash from the GitHub repository using the GitHub API.

    Returns:
        str: The latest commit hash from the repository.

    Raises:
        requests.RequestException: If there is an error fetching the commit hash from GitHub.
    """
    import requests

    url = f"https://api.github.com/repos/osirixgrpc/pyosirix_example_project/commits/main"
    headers = {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    latest_commit = response.json()
    return latest_commit['sha']


def get_git_hash() -> str:
    """ Get git hash of the project.

    Returns:
         str: Obtained from last git push if not hardcoded as __git_hash__.
    """
    if __git_hash__ == "HASH_PLACEHOLDER":
        return _fetch_latest_github_commit_hash()
    return __git_hash__
