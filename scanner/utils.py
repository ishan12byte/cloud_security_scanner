from datetime import datetime

def create_finding(service, resource, severity, issue):
    return{
        "service": service,
        "resource": resource,
        "severity": severity,
        "issue": issue,
        "timestamp": datetime.now().isoformat()
    }