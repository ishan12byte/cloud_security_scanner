from scanner.s3_scanner import scan_s3
from scanner.sg_scanner import scan_security_groups
from scanner.iam_scanner import scan_iam
from scanner.ec2_scanner import scan_ec2


def run_scan():

    findings = []

    findings.extend(scan_s3())
    findings.extend(scan_security_groups())
    findings.extend(scan_iam())
    findings.extend(scan_ec2())

    return findings