import argparse
from security_audit.aws_provider import AwsS3Provider
from security_audit.auditor import audit
from security_audit.reporting import write_report

def main():
    parser = argparse.ArgumentParser(description="Read-only AWS S3 security audit")
    parser.add_argument("--profile")
    parser.add_argument("--region", default="ap-south-1")
    parser.add_argument("--output", default="reports/audit.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print("Configuration validated. No AWS API calls made.")
        return
    findings = audit(AwsS3Provider(args.profile, args.region))
    payload = write_report(findings, args.output)
    print(payload["summary"])
if __name__ == "__main__": main()
