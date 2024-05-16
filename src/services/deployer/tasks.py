from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


def send_email(email: str) -> None:
    pass


def download_repository(_id: str, repo_link: str):
    with urlopen(repo_link + "/archive/refs/heads/master.zip") as response:
        with ZipFile(BytesIO(response.read())) as zipfile:
            zipfile.extractall(path=f"./codebase/{_id}")


def deploy(repo_link: str, _id: str, email: str, plan: str, instance: str) -> None:
    download_repository(_id, repo_link)
