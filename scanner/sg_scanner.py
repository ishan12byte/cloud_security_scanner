import boto3
from scanner.utils import create_finding

ec2 = boto3.client("ec2")

def scan_security_groups():
    findings = []

    groups = ec2.describe_security_groups()["SecurityGroups"]

    database_ports = {
                    3306: "MySQL",
                    5432: "PostgreSQL",
                    1433: "SQL Server",
                    27017: "MongoDB"
                }

    for sg in groups:

        group_name = sg["GroupName"]
        group_id = sg["GroupId"]
        resource = f"{group_name}({group_id})"

        for permission in sg.get("IpPermissions", []):

            from_port = permission.get("FromPort")
            to_port =permission.get("ToPort")

            for ip_range in permission.get("IpRanges", []):

                cidr = ip_range.get("CidrIp")

                if cidr != "0.0.0.0/0":
                    continue

                if permission.get("IpProtocol") == "-1":
                    findings.append(
                        create_finding("Security Group", resource, "CRITICAL", "All traffic open to the internet")
                    )
                    continue

                if from_port == 22:
                    findings.append(
                        create_finding("Security Group", resource, "HIGH", "SSH open to the internet")
                    )

                if from_port == 3389:
                    findings.append(
                        create_finding("Security Group", resource, "HIGH", "RDP open to the internet")
                    )

                # Might add as information later as HTTP is intentionally open to the internet
                # if from_port == 80:
                #     findings.append(
                #         create_finding("Security Group", resource, "LOW", "HTTP exposed to the internet")
                #     )

                # if from_port == 443:
                #     findings.append(
                #         create_finding("Security Group", resource, "LOW", "HTTPS exposed to the internet")
                #     )

                if from_port in database_ports:
                    findings.append(
                        create_finding("Security Group", resource, "HIGH", f"{database_ports[from_port]} exposed to the internet")
                    )

            for ipv6_ranges in permission.get("Ipv6Ranges", []):

                if ipv6_range.get("CidrIpv6") == "::/0":
                    findings.append(create_finding("Security Group", resource, "HIGH", "IPv6 access open to the internet"))

    return findings