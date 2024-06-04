import os
import uuid
import datetime
import shutil
from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen

import boto3

from logger import get_logger


logger = get_logger(__name__)


def download_repository(_id: str, repo_link: str, path: str) -> None:
    """
    Given a public repo link, Download and extract the codebase files
    """

    # Download repository as a zipfile from the given repo link
    with urlopen(repo_link + "/archive/refs/heads/master.zip") as response:
        # Open it as ZipFile object
        with ZipFile(file=BytesIO(response.read()), mode="a") as zipfile:
            # Extract codebase
            zipfile.extractall(path=path)

    logger.info("Repository downloaded at: %s", path)


def get_main_app_name(path: str) -> str | None:
    """
    Get the main app name where the manage.py file resides
    """

    for root, _, files in os.walk(path):
        if "wsgi.py" in files:
            return os.path.basename(root)
    return None


def copy_boilerplate_files(path: str, is_docker_configured: bool) -> None:
    """
    Copy the boilerplate files into the codebase
    """

    boilerplate_path = "./boilerplate"

    for filename in os.listdir(boilerplate_path):
        if is_docker_configured and "Dockerfile" in filename:
            continue

        shutil.copy2(f"{boilerplate_path}/{filename}",
                     f"{path}/{filename}")


def process_and_validate_files(codebase_path: str) -> bool:
    """
    Validate the codebase files and process them for ease of deployment
    """

    is_docker_configured = False

    # Check if docker is configured in the codebase
    for filename in os.listdir(codebase_path):
        if "Dockerfile" in filename:
            is_docker_configured = True
            break

    # Copy the relevant files present in the boilerplate into the codebase
    copy_boilerplate_files(codebase_path, is_docker_configured)

    main_app = get_main_app_name(codebase_path)

    if not main_app:
        raise FileNotFoundError(
            "WSGI file not found in the project. Cannot proceed further")

    with open(f"{codebase_path}/.env", "a", encoding="utf-8") as fp:
        fp.write(f"\nMAIN_APP={main_app}")

    logger.info("Codebase file processed successfully")
    return False


def get_s3_key(project_name: str) -> str:
    """
    Generate a unique object key for s3 file upload
    """

    timestamp = round(datetime.datetime.now(datetime.UTC).timestamp())
    return f"{project_name}/{timestamp}/codebase-{str(uuid.uuid4())}.zip"


def upload_codebase_s3(codebase_path: str, s3_key: str, aws_bucket: str) -> None:
    """
    Convert the codebase to a ZipFile and upload the ZipFile to S3
    """

    zip_content = BytesIO()
    s3 = boto3.client("s3")

    with ZipFile(zip_content, "w") as zipf:
        for root, _, files in os.walk(codebase_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=codebase_path)
                zipf.write(filename=file_path, arcname=arcname)

    zip_content.seek(0)

    s3.put_object(
        ACL="public-read",
        Body=zip_content,
        Bucket=aws_bucket,
        Key=s3_key,
        ContentType="application/zip"
    )

    zip_content.close()
    logger.info("File uploaded to s3 successfully")
