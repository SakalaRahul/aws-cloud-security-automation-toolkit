import boto3
from botocore.exceptions import ClientError

class AwsS3Provider:
    def __init__(self, profile=None, region=None):
        session = boto3.Session(profile_name=profile, region_name=region)
        self.client = session.client("s3")

    def list_buckets(self):
        return [b["Name"] for b in self.client.list_buckets().get("Buckets", [])]

    def _optional(self, method, **kwargs):
        try:
            return getattr(self.client, method)(**kwargs)
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {"NoSuchPublicAccessBlockConfiguration", "ServerSideEncryptionConfigurationNotFoundError"}:
                return None
            raise

    def inspect_bucket(self, bucket):
        public = self._optional("get_public_access_block", Bucket=bucket)
        encryption = self._optional("get_bucket_encryption", Bucket=bucket)
        policy = self._optional("get_bucket_policy_status", Bucket=bucket)
        return {
            "public_access": public.get("PublicAccessBlockConfiguration") if public else None,
            "encryption": encryption.get("ServerSideEncryptionConfiguration") if encryption else None,
            "policy_public": policy.get("PolicyStatus", {}).get("IsPublic") if policy else None,
        }
