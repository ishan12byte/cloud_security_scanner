import boto3
from botocore.exceptions import ClientError
from scanner.utils import create_finding

s3 = boto3.client("s3")

def scan_s3():
    findings = []
    buckets = s3.list_buckets()["Buckets"]

    for bucket in buckets:
        bucket_name = bucket["Name"]

        try:
            versioning = s3.get_bucket_versioning(Bucket=bucket_name)
            status = versioning.get("Status")

            if status != "Enabled":
                findings.append(
                        create_finding("S3", bucket_name, "LOW", "Versioning disabled")
                )
        
        except ClientError as e:
            findings.append(
                    create_finding("S3", bucket_name, "MEDIUM", f"Unable to check versioning: {str(e)}")
            )

        try:
            s3.get_bucket_encryption(Bucket=bucket_name)
        
        except ClientError as e:

            error_code = e.response["Error"]["Code"]

            if error_code == "ServerSideEncryptionConfigurationNotFoundError":
                findings.append(
                        create_finding("S3", bucket_name, "MEDIUM", "Bucket default encryption not configured")
                )

            else:
                findings.append(
                        create_finding("S3", bucket_name, "MEDIUM", f"Unable to check encryption: {error_code}")
                )

        try:
            public_access = s3.get_public_access_block(Bucket=bucket_name)
            config = public_access["PublicAccessBlockConfiguration"]

            if not all(config.values()):
                findings.append(
                        create_finding("S3", bucket_name, "HIGH", "Public access block partially disabled")
                )
            
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "NoSuchPublicAccessBlockConfiguration":
                findings.append(
                        create_finding("S3", bucket_name, "HIGH", "Public access block not configured")
                )

            else:
                findings.append(
                        create_finding("S3", bucket_name, "MEDIUM", f"Unable to check public access block: {error_code}")
                )

    return findings