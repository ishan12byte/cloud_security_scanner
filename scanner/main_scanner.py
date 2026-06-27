from scanner.s3_scanner import scan_s3
from scanner.sg_scanner import scan_security_groups
from scanner.iam_scanner import scan_iam
from scanner.ec2_scanner import scan_ec2
from scanner.severity import SEVERITY_ORDER


def run_scan():

    findings = []

    findings.extend(scan_s3())
    findings.extend(scan_security_groups())
    findings.extend(scan_iam())
    findings.extend(scan_ec2())

    findings.sort(
    key=lambda x: SEVERITY_ORDER.get(
        x["severity"],
        0
    ),
    reverse=True)
    
    return findings