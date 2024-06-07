import os
import shutil
import subprocess

import boto3
from celery import Celery
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

app = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL"),
    backend="rpc://"
)
app.conf.task_default_queue = os.getenv("CELERY_DEFAULT_QUEUE")


@app.task
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


@app.task
def deploy(repo_link: str, _id: str, email: str, instance: str) -> None:
    """
    Given a public repo link, Process the codebase and deploy it onto the cloud
    """

    try:
        codebase_root_path = "./codebase"
        instance_output_path = "./terraform/instance_data.json"

        project_name = repo_link.split('/')[-1]
        download_path = f"{codebase_root_path}/{_id}"
        codebase_path = f"{download_path}/{project_name}-master"

        aws_bucket = os.getenv("AWS_BUCKET_NAME")
        s3_key = get_s3_key(project_name)

        # Code processing
        download_repository(_id, repo_link, download_path)
        process_and_validate_files(codebase_path)
        upload_codebase_s3(codebase_path, s3_key, aws_bucket)

        # Setup the infrastructure for deployment
        output = subprocess.run(
            [
                "sh",
                "./terraform.sh",
                instance,
                project_name,
                f'https://{aws_bucket.lower()}.s3.amazonaws.com/{s3_key}',
                instance_output_path.split("/")[-1]
            ],
            check=False,
            stdout=subprocess.PIPE,
            text=True
        )

        if output.returncode != 0:
            raise subprocess.SubprocessError()

        logger.info("Infrastructure setup successfully")

        instance_dns = get_instance_dns_from_json(instance_output_path)

        logger.info("Instance Public IPv4 DNS: %s", instance_dns)

        send_email.apply_async(kwargs={
            "subject": "Deployment Succeeded🎉",
            "body": f"Your project deployed successfully.\n\nYou can access your project using this URL: http://{instance_dns}",
            "recipient": email
        })

    except Exception as e:
        logger.error(e)

        send_email.apply_async(kwargs={
            "subject": "Deployment Failed😞",
            "body": "Your deployment has failed due to an internal error.",
            "recipient": email
        })

    finally:
        # File cleanup
        shutil.rmtree(download_path)
        os.remove(instance_output_path)
