# Cloud Security Automation Toolkit

A modular Python security-audit tool for AWS S3. It inventories buckets, checks public-access
block settings, bucket policies and default encryption, and emits JSON findings with severity.

## Run locally
- Python 3.11+
- `pip install -r requirements.txt`
- `cp .env.example .env`
- Configure AWS credentials using an AWS profile or environment variables.
- `python -m security_audit.cli --profile default --region ap-south-1 --output reports/audit.json`
- `pytest -q`

Use `--dry-run` for configuration validation without making AWS API calls. This tool is read-only:
it does not modify bucket policies or encryption settings.

## IAM permissions
Use a dedicated read-only IAM role with only the required list/get permissions:
`s3:ListAllMyBuckets`, `s3:GetBucketLocation`, `s3:GetBucketPolicyStatus`,
`s3:GetPublicAccessBlock`, `s3:GetEncryptionConfiguration`.
Do not use administrator credentials. Missing permissions are recorded as `UNKNOWN`, not treated as secure.

## Design
- Provider abstraction isolates AWS SDK calls.
- Rules are pure functions and unit tested.
- Findings carry resource, check, severity, status and remediation guidance.
- JSON report is suitable for CI artifact upload or later dashboard ingestion.
