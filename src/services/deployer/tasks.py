from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


def send_email(email: str) -> None:
    pass


def download_repository(_id: str, repo_link: str):
    # Download repository as a zipfile from the given repo link
    with urlopen(repo_link + "/archive/refs/heads/master.zip") as response:
        # Open it as ZipFile object
        with ZipFile(file=BytesIO(response.read()), mode="a") as zipfile:
            # Extract codebase
            zipfile.extractall(path=f"./codebase/{_id}")


def deploy(repo_link: str, _id: str, email: str, plan: str, instance: str) -> None:
    download_repository(_id, repo_link)
