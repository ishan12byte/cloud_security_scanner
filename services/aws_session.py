import boto3


def create_clients(access_key, secret_key, region):

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    return {
        "s3": session.client("s3"),
        "ec2": session.client("ec2"),
        "iam": session.client("iam")
    }