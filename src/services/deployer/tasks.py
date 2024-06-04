import os
import subprocess

from botocore.exceptions import ClientError

from logger import get_logger
from utils import (
    get_s3_key,
    download_repository,
    process_and_validate_files,
    upload_codebase_s3
)


logger = get_logger(__name__)

CODEBASE_ROOT_PATH = "./codebase"


def send_email(email: str) -> None:
    """
    Send email to user regarding their application deployment status
    """
    pass


def deploy(repo_link: str, _id: str, email: str, plan: str, instance: str) -> None:
    """
    Given a public repo link, Process the codebase and deploy it onto the cloud
    """

    project_name = repo_link.split('/')[-1]
    download_path = f"{CODEBASE_ROOT_PATH}/{_id}"
    codebase_path = f"{download_path}/{project_name}-master"

    instance_init_file = "./instance.init.sh"
    aws_bucket = os.getenv("AWS_BUCKET_NAME")
    s3_key = get_s3_key(project_name)

    download_repository(_id, repo_link, download_path)

    try:
        process_and_validate_files(codebase_path)
        upload_codebase_s3(codebase_path, s3_key, aws_bucket)
        print(f'https://{aws_bucket.lower()}.s3.amazonaws.com/{s3_key}')
    except (FileNotFoundError, ClientError) as e:
        logger.error(e)
        return

    output = subprocess.run([instance_init_file, codebase_path,
                             project_name], check=False, capture_output=True)

    print(output.stdout.decode())
