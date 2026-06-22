import boto3
from botocore.exceptions import ClientError
from datetime import datetime

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
                    {
                        "service":"S3",
                        "resource": bucket_name,
                        "severity": "LOW",
                        "issue": "Versioning disabled",
                        "timestamp": datetime.now().isoformat()
                    }
                )
        
        except ClientError as e:
            findings.append(
                {
                    "service":"S3",
                    "resource": bucket_name,
                    "severity": "MEDIUM",        
                    "issue": f"Unable to check versioning: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
            )

        try:
            s3.get_bucket_encryption(Bucket=bucket_name)
        
        except ClientError as e:

            error_code = e.response["Error"]["Code"]

            if error_code == "ServerSideEncryptionConfigurationNotFoundError":
                findings.append(
                    {
                        "service":"S3",
                        "resource": bucket_name,
                        "severity": "MEDIUM",        
                        "issue": "Bucket encryption disabled",
                        "timestamp": datetime.now().isoformat()
                    }
                )

            else:
                findings.append(
                    {
                        "service":"S3",
                        "resource": bucket_name,
                        "severity": "MEDIUM",        
                        "issue": f"Unable to check encryption: {error_code}",
                        "timestamp": datetime.now().isoformat()
                    }
                )

        try:
            public_access = s3.get_public_access_block(Bucket=bucket_name)
            config = public_access["PublicAccessBlockConfiguration"]

            if not all(config.values()):
                findings.append(
                    {
                        "service":"S3",
                        "resource": bucket_name,
                        "severity": "HIGH",        
                        "issue": "Public access block partially disabled",
                        "timestamp": datetime.now().isoformat()
                    }
                )
            
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "NoSuchPublicAccessBlockConfiguration":
                findings.append(
                    {
                        "service":"S3",
                        "resource": bucket_name,
                        "severity": "HIGH",        
                        "issue": "Public access block not configured",
                        "timestamp": datetime.now().isoformat()
                    }
                )

            else:
                findings.append(
                    {
                        "service":"S3",
                        "resource": bucket_name,
                        "severity": "MEDIUM",        
                        "issue": f"Unable to check public access block: {error_code}",
                        "timestamp": datetime.now().isoformat()
                    }
                )

    return findings