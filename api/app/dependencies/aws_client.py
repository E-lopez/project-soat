import os
from dotenv import load_dotenv
import boto3
from functools import lru_cache
import logging

from botocore.exceptions import BotoCoreError, ClientError

from app.tasks.telemetry_service import TelemetryBedrockClient
from app.functions.utils import get_doppler_secret

logger = logging.getLogger(__name__)
env = os.getenv('APP_ENV', 'dev')
load_dotenv(f".env.{env}")

access_key = get_doppler_secret('AWS_ACCESS_KEY_ID', os.environ.get('AWS_ACCESS_KEY_ID'))
secret_key = get_doppler_secret('AWS_SECRET_ACCESS_KEY', os.environ.get('AWS_SECRET_ACCESS_KEY'))
region = os.environ.get('AWS_REGION', 'us-east-1')
session_token = get_doppler_secret('AWS_SESSION_TOKEN', os.environ.get('AWS_SESSION_TOKEN'))

@lru_cache(maxsize=1)
def get_bedrock_client():
    try:
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
    except (BotoCoreError, ClientError) as e:
        logging.exception(f"Failed to initialize AWS Bedrock client: {str(e)}")
        # We MUST re-raise so @lru_cache knows NOT to cache this failure
        raise e


def get_s3_client():
    try:
        return boto3.client(
            service_name="s3",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
    except (BotoCoreError, ClientError) as e:
        logging.exception(f"Failed to initialize AWS S3 client: {str(e)}")
        raise e
    
raw_client = get_bedrock_client()
bedrock_client = TelemetryBedrockClient(raw_client)
s3_client = get_s3_client()