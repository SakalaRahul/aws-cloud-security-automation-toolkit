from security_audit.rules import public_access_finding, encryption_finding, policy_finding

def audit(provider):
    findings = []
    for bucket in provider.list_buckets():
        try:
            state = provider.inspect_bucket(bucket)
            findings.extend([
                public_access_finding(bucket, state["public_access"]),
                encryption_finding(bucket, state["encryption"]),
                policy_finding(bucket, state["policy_public"]),
            ])
        except Exception as exc:
            from security_audit.models import Finding
            findings.append(Finding(bucket, "BUCKET_INSPECTION", "MEDIUM", "UNKNOWN",
                                    f"Inspection failed: {type(exc).__name__}",
                                    "Check IAM permissions, region and CloudTrail for the failed API call."))
    return findings
