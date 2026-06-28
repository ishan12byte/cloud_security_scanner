import boto3

from scanner.s3_scanner import scan_s3
from scanner.sg_scanner import scan_security_groups
from scanner.iam_scanner import scan_iam
from scanner.ec2_scanner import scan_ec2
from scanner.severity import SEVERITY_ORDER


def run_scan(session=None):

    if session is None:
        session = boto3.Session()
    
    s3 = session.client("s3")
    ec2 = session.client("ec2")
    iam = session.client("iam")
    
    findings = []

    findings.extend(scan_s3(s3))
    findings.extend(scan_security_groups(ec2))
    findings.extend(scan_iam(iam))
    findings.extend(scan_ec2(ec2))

    findings.sort(
    key=lambda x: SEVERITY_ORDER.get(
        x["severity"],
        0
    ),
    reverse=True)
    
    return findings