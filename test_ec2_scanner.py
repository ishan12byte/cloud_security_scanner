from scanner.ec2_scanner import scan_ec2

results = scan_ec2()

print(f"\nFindings: {len(results)}\n")

for finding in results:
    print(finding)