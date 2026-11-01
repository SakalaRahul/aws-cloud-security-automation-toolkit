from security_audit.models import Finding

def public_access_finding(bucket, config):
    if config is None:
        return Finding(bucket, "S3_PUBLIC_ACCESS_BLOCK", "HIGH", "UNKNOWN",
                       "Unable to read public access block configuration.",
                       "Grant the audit role s3:GetPublicAccessBlock and rerun.")
    flags = ["BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]
    enabled = [bool(config.get(k, False)) for k in flags]
    if all(enabled):
        return Finding(bucket, "S3_PUBLIC_ACCESS_BLOCK", "INFO", "PASS",
                       "All four public-access-block controls are enabled.", "No action required.")
    return Finding(bucket, "S3_PUBLIC_ACCESS_BLOCK", "HIGH", "FAIL",
                   "One or more public-access-block controls are disabled.",
                   "Enable all four S3 Block Public Access settings unless an approved exception exists.")

def encryption_finding(bucket, config):
    if config is None:
        return Finding(bucket, "S3_DEFAULT_ENCRYPTION", "MEDIUM", "UNKNOWN",
                       "Encryption configuration unavailable or not configured.",
                       "Verify permissions and configure default SSE-S3 or SSE-KMS encryption.")
    rules = config.get("Rules", [])
    if rules:
        return Finding(bucket, "S3_DEFAULT_ENCRYPTION", "INFO", "PASS",
                       "Default server-side encryption configuration exists.", "Review KMS key policy if SSE-KMS is used.")
    return Finding(bucket, "S3_DEFAULT_ENCRYPTION", "MEDIUM", "FAIL",
                   "No default encryption rule was returned.",
                   "Configure default server-side encryption for the bucket.")

def policy_finding(bucket, is_public):
    if is_public is None:
        return Finding(bucket, "S3_BUCKET_POLICY_PUBLIC", "MEDIUM", "UNKNOWN",
                       "Bucket policy status could not be determined.",
                       "Grant s3:GetBucketPolicyStatus and rerun.")
    if is_public:
        return Finding(bucket, "S3_BUCKET_POLICY_PUBLIC", "HIGH", "FAIL",
                       "AWS reports the bucket policy as public.",
                       "Review the bucket policy and remove unintended public principals or actions.")
    return Finding(bucket, "S3_BUCKET_POLICY_PUBLIC", "INFO", "PASS",
                   "AWS does not classify the bucket policy as public.", "No action required.")
