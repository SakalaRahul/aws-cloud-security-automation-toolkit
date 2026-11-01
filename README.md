# AWS Cloud Security Automation Toolkit

A Python-based, read-only AWS S3 security auditing tool that checks bucket security configurations and generates structured JSON reports. The project uses **Boto3** to interact with AWS and **Pytest** for automated testing.

## Project Overview

Cloud storage misconfigurations can expose sensitive data and create security risks. This toolkit helps identify common Amazon S3 security configuration issues by inspecting buckets and reporting potential findings.

The tool performs read-only checks. It does not modify bucket configurations, policies, permissions, or other AWS resources.

## Key Features

- **S3 Public Access Block Audit:** Checks whether all four S3 Block Public Access controls are enabled.
- **Default Encryption Audit:** Checks whether a default server-side encryption configuration exists.
- **Bucket Policy Audit:** Identifies whether AWS reports an S3 bucket policy as public.
- **Security Findings:** Classifies results as `PASS`, `FAIL`, or `UNKNOWN`.
- **JSON Reporting:** Generates a structured report with timestamps, findings, severity levels, and remediation guidance.
- **Dry Run Mode:** Allows the CLI to run without making AWS API calls.
- **Automated Testing:** Uses Pytest to test security audit rules.
- **CI Integration:** GitHub Actions runs the automated tests on pushes and pull requests.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Boto3 | AWS SDK integration |
| Amazon S3 | Cloud storage security auditing |
| Pytest | Automated testing |
| JSON | Security report generation |
| GitHub Actions | Continuous Integration |

## Architecture

```text
              Python CLI
                  |
                  v
           AWS S3 Provider
                  |
                  v
          List S3 Buckets
                  |
                  v
          Security Auditor
                  |
       +----------+----------+
       |          |          |
       v          v          v
   Public      Default    Bucket Policy
   Access      Encryption    Audit
   Audit        Audit
       |          |          |
       +----------+----------+
                  |
                  v
          Security Findings
                  |
                  v
             JSON Report
```

## Security Checks

The toolkit currently evaluates three security areas:

| Check | What it evaluates |
|---|---|
| S3 Public Access Block | Whether all four public-access-block settings are enabled |
| S3 Default Encryption | Whether a default server-side encryption configuration exists |
| S3 Bucket Policy | Whether AWS classifies the bucket policy as public |

Each finding includes the affected resource, check name, severity, status, explanation, and suggested remediation.

## Project Structure

```text
aws-cloud-security-automation-toolkit/
│
├── security_audit/
│   ├── __init__.py
│   ├── cli.py
│   ├── aws_provider.py
│   ├── auditor.py
│   ├── rules.py
│   ├── models.py
│   └── reporting.py
│
├── tests/
│   └── test_rules.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── .env.example
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/aws-cloud-security-automation-toolkit.git
cd aws-cloud-security-automation-toolkit
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Credentials

Install and configure the AWS CLI, then configure a named AWS profile or use your default profile.

```bash
aws configure
```

The tool uses Boto3 to access AWS credentials through the standard AWS credential chain.

Use an IAM identity with only the permissions required for the audit. The relevant read permissions include:

- `s3:ListAllMyBuckets`
- `s3:GetBucketPublicAccessBlock`
- `s3:GetEncryptionConfiguration`
- `s3:GetBucketPolicyStatus`

Do not commit AWS access keys, secret keys, or other credentials to GitHub.

### 5. Run in Dry Run Mode

```bash
python -m security_audit.cli --dry-run
```

This mode exits without making AWS API calls.

### 6. Run the Security Audit

```bash
python -m security_audit.cli --profile default --region ap-south-1 --output reports/audit.json
```

Change the AWS profile and region arguments as required.

The report is generated at:

```text
reports/audit.json
```

### 7. Run Automated Tests

```bash
pytest -q
```

GitHub Actions also runs the test suite automatically when code is pushed or a pull request is opened.

## Sample Report Format

The generated JSON report contains a summary and individual security findings.

```json
{
  "summary": {
    "total": 3,
    "failed": 1,
    "unknown": 0
  },
  "findings": [
    {
      "resource": "example-bucket",
      "check": "S3_PUBLIC_ACCESS_BLOCK",
      "severity": "INFO",
      "status": "PASS",
      "message": "All four public-access-block controls are enabled.",
      "remediation": "No action required."
    }
  ]
}
```

*Illustrative report format; actual results depend on the AWS account being audited.*

## Security and Limitations

- The toolkit performs read-only AWS S3 inspection.
- It does not automatically remediate security findings.
- It checks the S3 security configurations described above; it is not a complete AWS security assessment.
- Results depend on the AWS identity's permissions and the information returned by AWS APIs.
- An `UNKNOWN` result means the required configuration could not be determined; it should not automatically be treated as a confirmed misconfiguration.
- Test execution does not require AWS credentials.

## Future Enhancements

- Add CloudWatch monitoring and alerting.
- Support additional AWS security checks.
- Add CSV and HTML report formats.
- Introduce scheduled security audits.
- Add configurable security policies and severity thresholds.
- Explore automated remediation with explicit approval controls.

## Author

**Rahul Sakala**

- GitHub: https://github.com/SakalaRahul
- LinkedIn: https://linkedin.com/in/24rahul

---

*This project is intended for learning and demonstrating Python-based cloud security auditing and AWS SDK integration. Run it only against AWS accounts you are authorized to inspect.*
