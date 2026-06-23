from scanner.sg_scanner import scan_security_groups

results = scan_security_groups()

print(f"\nFindings: {len(results)}\n")

for finding in results:
    print(finding)