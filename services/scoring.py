SEVERITY_WEIGHTS = {
    "CRITICAL": 20,
    "HIGH": 10,
    "MEDIUM": 5,
    "LOW": 2
}


def calculate_security_score(findings):
    """
    Calculate security score out of 100.
    """

    score = 100

    deductions = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for finding in findings:

        severity = finding["severity"]

        if severity in SEVERITY_WEIGHTS:

            score -= SEVERITY_WEIGHTS[severity]
            deductions[severity] += SEVERITY_WEIGHTS[severity]

    score = max(score, 0)

    return {
        "score": score,
        "deductions": deductions
    }