import boto3
from botocore.exceptions import ClientError

from scanner.utils import create_finding

ec2 = boto3.client("ec2")

def scan_ec2():
    findings = []

    try:
        reservations = ec2.describe_instances()["Reservations"]

        for reservation in reservations:

            for instance in reservation["Instances"]:

                instance_id = instance["InstanceId"]
                state = instance["State"]["Name"]

                if instance.get("PublicIpAddress"):
                    findings.append(create_finding("EC2", instance_id, "MEDIUM", "Instance has a public ip address"))

                if state == "stopped":
                    findings.append(create_finding("EC2", instance_id, "LOW", "Instance is stopped"))

                try:
                    termination =ec2.describe_instance_attribute(
                        InstanceId=instance_id,
                        Attribute="disableApiTermination"
                    )

                    if not termination["DisableApiTermination"]["Value"]:

                        findings.append(create_finding("EC2", instance_id, "LOW", "Termination protection disabled"))
                    
                except ClientError as e:

                    error_code = e.response["Error"]["Code"]
                    findings.append(create_finding("EC2", instance_id, "MEDIUM", f"Unable to check termination protection: {error_code}"))
    
    except ClientError as e:

        error_code = e.response["Error"]["Code"]
        findings.append(create_finding("EC2", "ALL_INSTANCES", "MEDIUM", f"Unable to scan instances: {error_code}"))

    try:
        volumes = ec2.describe_volumes()["Volumes"]

        for volume in volumes:

            volume_id = volume["VolumeId"]

            if not volume["Encrypted"]:
                findings.append(create_finding("EC2", volume_id, "MEDIUM", "Volume is not encrypted"))

    except ClientError as e:

        error_code = e.response["Error"]["Code"]
        findings.append(create_finding("EC2", "ALL_VOlUME", "MEDIUM", f"Unable to scan volumes: {error_code}"))

    return findings