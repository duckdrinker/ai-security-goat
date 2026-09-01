"""
Out of scope for this detector (not a false negative): the same hardcoded-
credential shape as bad_hardcoded_api_key.yaml, but in a plain Python source
file rather than an agent/tool manifest. agent-uses-static-long-lived-
credential only scans manifests; a generic Secrets scanner is the right tool
for this file.
"""
BILLING_API_TOKEN = "sk-live-51H8x9K2mN7pQ4rT6vY8wZ1aB3cD5eF7gH9jK"
