import os
import shutil
import subprocess

import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError

from logger import get_logger
from utils import (
    get_s3_key,
    download_repository,
    process_and_validate_files,
    upload_codebase_s3,
    get_instance_dns_from_json
)


logger = get_logger(__name__)

CODEBASE_ROOT_PATH = "./codebase"
INSTANCE_OUTPUT_PATH = "./terraform/instance_data.json"


def send_email(subject: str, body: str, recipient: str) -> None:
    """
    Send email to user regarding their application deployment status
    """

    ses = boto3.client("ses")
    sender = os.getenv("AWS_SES_SENDER")

    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        "Data": body,
                        "Charset": "UTF-8"
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender,
        )

        logger.info({
            "msg": "Email sent successfully",
            "response": response
        })

    except (ClientError, NoCredentialsError, PartialCredentialsError) as e:
        logger.error(e)


def deploy(repo_link: str, _id: str, email: str, plan: str, instance: str) -> None:
    """
    Given a public repo link, Process the codebase and deploy it onto the cloud
    """

    try:
        project_name = repo_link.split('/')[-1]
        download_path = f"{CODEBASE_ROOT_PATH}/{_id}"
        codebase_path = f"{download_path}/{project_name}-master"

        aws_bucket = os.getenv("AWS_BUCKET_NAME")
        s3_key = get_s3_key(project_name)

        # Code processing
        download_repository(_id, repo_link, download_path)
        process_and_validate_files(codebase_path)
        upload_codebase_s3(codebase_path, s3_key, aws_bucket)

        # Remove the codebase from local
        shutil.rmtree(download_path)

        # Setup the infrastructure for deployment
        output = subprocess.run(
            [
                "./terraform.sh",
                project_name,
                f'https://{aws_bucket.lower()}.s3.amazonaws.com/{s3_key}',
                INSTANCE_OUTPUT_PATH.split("/")[-1]
            ],
            check=False,
            stdout=subprocess.PIPE,
            text=True
        )

        logger.info(output.stdout)

        if output.returncode != 0:
            raise subprocess.SubprocessError()

        instance_dns = get_instance_dns_from_json(INSTANCE_OUTPUT_PATH)

        os.remove(INSTANCE_OUTPUT_PATH)

        logger.info("Instance Public IPv4 DNS: %s", instance_dns)

        send_email.apply_async(kwargs={
            "subject": "Deployment Success🎉",
            "body": f"Your project deployed successfully.\n\nYou can access your project using this URL: {instance_dns}",
            "recipient": email
        })
    except Exception as e:
        logger.error(e)

        send_email.apply_async(kwargs={
            "subject": "Deployment Failed😞",
            "body": "Due to an internal error, Your project deployment as failed.",
            "recipient": email
        })
