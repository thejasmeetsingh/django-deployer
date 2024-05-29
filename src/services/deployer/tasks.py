import os
import shutil
import boto3
import datetime
import uuid
import subprocess
from botocore.exceptions import ClientError
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

    download_path = f"{CODEBASE_ROOT_PATH}/{_id}"

    # Download repository as a zipfile from the given repo link
    with urlopen(repo_link + "/archive/refs/heads/master.zip") as response:
        # Open it as ZipFile object
        with ZipFile(file=BytesIO(response.read()), mode="a") as zipfile:
            # Extract codebase
            zipfile.extractall(path=download_path)

    logger.info("Repository downloaded at: %s", download_path)


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

    for filename in os.listdir("./boilerplate"):
        if is_docker_configured and "Dockerfile" in filename:
            continue

        shutil.copy2(f"{BOILERPLATE_ROOT_PATH}/{filename}",
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


def deploy(repo_link: str, _id: str, email: str, plan: str, instance: str) -> None:
    """
    Given a public repo link, Process the codebase and deploy it onto the cloud
    """

    project_name = repo_link.split('/')[-1]
    codebase_path = f"{CODEBASE_ROOT_PATH}/{_id}/{project_name}-master"
    # instance_init_file = "./instance.init.sh"
    aws_bucket = os.getenv("AWS_BUCKET_NAME")
    s3_key = get_s3_key(project_name)

    download_repository(_id, repo_link)

    try:
        process_and_validate_files(codebase_path)
        upload_codebase_s3(codebase_path, s3_key, aws_bucket)
        print(f'https://{aws_bucket.lower()}.s3.amazonaws.com/{s3_key}')
    except (FileNotFoundError, ClientError) as e:
        logger.error(e)
        return

    # output = subprocess.run([instance_init_file, codebase_path,
    #                          project_name], check=False, capture_output=True)

    # print(output.stdout.decode())
