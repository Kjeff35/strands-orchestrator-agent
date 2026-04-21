import os
from dotenv import load_dotenv
from strands.models import BedrockModel

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")
MODEL_ID = os.getenv("MODEL_ID", "eu.anthropic.claude-haiku-4-5-20251001-v1:0")


def get_model() -> BedrockModel:
    return BedrockModel(model_id=MODEL_ID, region_name=AWS_REGION, max_tokens=4096)
