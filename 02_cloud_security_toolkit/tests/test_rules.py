from security_audit.rules import public_access_finding, encryption_finding, policy_finding

def test_public_access_pass():
    config = {k: True for k in ["BlockPublicAcls","IgnorePublicAcls","BlockPublicPolicy","RestrictPublicBuckets"]}
    assert public_access_finding("demo", config).status == "PASS"

def test_public_access_fail():
    config = {k: False for k in ["BlockPublicAcls","IgnorePublicAcls","BlockPublicPolicy","RestrictPublicBuckets"]}
    assert public_access_finding("demo", config).status == "FAIL"

def test_missing_encryption_is_unknown():
    assert encryption_finding("demo", None).status == "UNKNOWN"

def test_public_policy_fail():
    assert policy_finding("demo", True).severity == "HIGH"
