from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from aws_cdk import Duration

from constructs import Construct
from aws_cdk import aws_lambda
from aws_cdk import aws_ecr_assets
from aws_cdk import aws_s3 as s3


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.static_bucket = s3.Bucket(self, "Bucket")

        code = aws_lambda.Code.from_asset_image(
            "../",
            file="Dockerfile",
            platform=aws_ecr_assets.Platform.LINUX_AMD64,
        )

        lambda_settings = {
            "runtime": aws_lambda.Runtime.FROM_IMAGE,
            "code": code,
            "timeout": Duration.seconds(60),
            "handler": aws_lambda.Handler.FROM_IMAGE,
            "memory_size": 1024,
            "reserved_concurrent_executions": 10,
            "dead_letter_queue_enabled": True,
            "environment": {
                "SECRET_KEY": "big-secret",
                "STATIC_BUCKET": self.static_bucket.bucket_name,
            },
        }
        func = aws_lambda.Function(self, "django", **lambda_settings)
        self.static_bucket.grant_write(func)
