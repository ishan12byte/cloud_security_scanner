    import boto3
    from botocore.exceptions import  ClientError
    from datetime import datetime, timezone

    from scanner.utils import create_finding

    iam = boto3.client("iam")

    def scan_iam():
        findings = []
        privileged_policies = {"AdministratorAccess", "PowerUserAccess"}

        users = iam.list_users()["Users"]

        for user in users:

            username = user["UserName"]

            try:
                mfa_devices= iam.list_mfa_devices(UserName=username)["MFADevices"]

                if len(mfa_devices) == 0:
                    findings.append(create_finding("IAM", username, "MEDIUM", "MFA not enabled"))

            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                findings.append(create_finding("IAM", username, "MEDIUM", f"Unable to check MFA: {error_code}"))

            try:
                policies = iam.list_attached_user_policies(UserName=username)["AttachedPolicies"]

                for policy in policies:

                    if policy["PolicyName"] in privileged_policies:
                        findings.append(create_finding("IAM", username, "HIGH", f"{policy['PolicyName']} attached"))

            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                findings.append(create_finding("IAM", username, "MEDIUM", f"Unable to check policies: {error_code}"))

            try:
                access_keys = iam.list_access_keys(UserName=username)["AccessKeyMetadata"]

                if len(access_keys)>1:
                    findings.append(create_finding("IAM", username, "LOW", f"User has {len(access_keys)} access keys"))

                for key in access_keys:
                    age = ( datetime.now(timezone.utc)-key["CreateDate"] ).days

                    if age > 90:
                        findings.append(create_finding("IAM", username, "LOW", f"Access key older than 90 days ({age} days)"))

            except ClientError as e:
                error_code = e.response["Error"]["Code"]
                findings.append(create_finding("IAM", username, "MEDIUM", f"Unable to check access keys: {error_code}"))

            try:
                groups = iam.list_groups_for_user(UserName=username)["Groups"]

                for group in groups:

                    group_name = group["GroupName"]

                    policies = iam.list_attached_group_policies(GroupName=group_name)["AttachedPolicies"]

                    for policy in policies:

                        if policy["PolicyName"] in privileged_policies:
                            findings.append(create_finding("IAM", username, "HIGH", f"{policy['PolicyName']} inherited from the group {group_name}"))

            except ClientError as e:

                error_code = e.response["Error"]["Code"]
                findings.append(create_finding("IAM", username, "MEDIUM", f"Unable to check group policies: {error_code}"))

            # Power User access will be added too
            # Will add Passwordless User later
            #As well as a check for custom policies providing admin access

        return findings 