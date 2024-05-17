import os
import shutil
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

from logger import get_logger


logger = get_logger(__name__)

BOILERPLATE_ROOT_PATH = "./boilerplate"
CODEBASE_ROOT_PATH = "./codebase"


def send_email(email: str) -> None:
    """
    Send email to user regarding their application deployment status
    """
    pass


def download_repository(_id: str, repo_link: str) -> None:
    """
    Given a public repo link, Download and extract the codebase files
    """

    # Download repository as a zipfile from the given repo link
    with urlopen(repo_link + "/archive/refs/heads/master.zip") as response:
        # Open it as ZipFile object
        with ZipFile(file=BytesIO(response.read()), mode="a") as zipfile:
            # Extract codebase
            zipfile.extractall(path=f"{CODEBASE_ROOT_PATH}/{_id}")


def get_main_app_name(path: str) -> str | None:
    """
    Get the main app name where the manage.py file resides
    """

    for root, _, files in os.walk(path):
        if "manage.py" in files:
            return os.path.basename(root)
    return None


def copy_boilerplate_files(path: str, is_docker_configured: bool) -> None:
    """
    Copy the boilerplate files into the codebase
    """

    if is_docker_configured:
        shutil.copy2(f"{BOILERPLATE_ROOT_PATH}/nginx.conf",
                     f"{path}/nginx.conf")
        return

    for filename in os.listdir("./boilerplate"):
        shutil.copy2(f"{BOILERPLATE_ROOT_PATH}/{filename}",
                     f"{path}/{filename}")


def process_and_validate_files(_id: str) -> bool:
    """
    Validate the codebase files and process them for ease of deployment
    """

    codebase_path = f"{CODEBASE_ROOT_PATH}/{_id}"
    is_docker_configured = False

    for filename in os.listdir(codebase_path):
        if "docker-compose.yml" in filename or "compose.yml" in filename:
            is_docker_configured = True
            break

    copy_boilerplate_files(codebase_path, is_docker_configured)

    if is_docker_configured:
        return True

    main_app = get_main_app_name(codebase_path)

    if not main_app:
        raise FileNotFoundError(
            "manage.py not found in the project. Cannot proceed further")

    with open(f"{codebase_path}/.env", "a", encoding="utf-8") as fp:
        fp.write(f"MAIN_APP={main_app}")

    return False


def deploy(repo_link: str, _id: str, email: str, plan: str, instance: str) -> None:
    """
    Given a public repo link, Process the codebase and deploy it onto the cloud
    """

    download_repository(_id, repo_link)

    try:
        process_and_validate_files(_id)
    except FileNotFoundError as e:
        logger.error(e)
