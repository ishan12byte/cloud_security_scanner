from scanner.s3_scanner import scan_s3

results = scan_s3()

print(f"\nFindings: {len(results)}\n")

for finding in results:
    print(finding)