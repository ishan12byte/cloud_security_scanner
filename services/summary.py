from collections import Counter

def generate_summary(findings):
    
    severity_counts = Counter()
    service_counts = Counter()
    
    for finding in findings:
        
        severity_counts[finding["severity"]] += 1
        service_counts[finding["service"]] += 1
        
    summary = {
        "total_findings": len(findings),

        "severity": {
            "critical": severity_counts["CRITICAL"],
            "high": severity_counts["HIGH"],
            "medium": severity_counts["MEDIUM"],
            "low": severity_counts["LOW"]
        },

        "services": dict(service_counts)
    }

    return summary
    