# Tool Guide: AWS Security — GuardDuty, CloudTrail, and Security Hub

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Document ID**   | SOC-TG-005                                      |
| **Title**         | AWS Security Tooling Guide for SOC Analysts     |
| **Author**        | Lisa Tran                                        |
| **Last Updated**  | 2025-11-05                                       |
| **Status**        | Active                                           |
| **Review Cycle**  | Quarterly                                        |
| **Classification**| Internal — Meridian National Bank                 |

---

## 1. Purpose

This guide provides SOC analysts with procedures for investigating security events in Meridian National Bank's AWS environment. It covers triage of GuardDuty findings, CloudTrail log analysis, Security Hub compliance checks, and common containment actions for cloud-based incidents.

## 2. AWS Environment Overview

### 2.1 Account Structure

| Account Name | Account ID | Purpose | VPC CIDR |
|-------------|------------|---------|----------|
| meridian-prod | 111222333444 | Production workloads | 10.50.0.0/16 |
| meridian-staging | 222333444555 | Staging and QA | 10.51.0.0/16 |
| meridian-dev | 333444555666 | Development | 10.52.0.0/16 |
| meridian-security | 444555666777 | Security tooling, log aggregation | 10.53.0.0/16 |
| meridian-shared-services | 555666777888 | DNS, Active Directory, CI/CD | 10.54.0.0/16 |

### 2.2 AWS CLI Configuration

All SOC analysts have access via the `meridian-security` SSO profile. Authenticate before running any commands:

```bash
aws sso login --profile meridian-security
```

To assume a role into another account for investigation:

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::111222333444:role/SOC-InvestigationRole \
  --role-session-name "soc-investigation-$(date +%Y%m%d)" \
  --profile meridian-security
```

Export the returned credentials before running commands against the target account.

## 3. Amazon GuardDuty

### 3.1 Overview

GuardDuty is enabled in all Meridian AWS accounts and sends findings to the `meridian-security` account as a delegated administrator. Findings are also forwarded to Splunk (`index=cloud sourcetype=aws:guardduty`).

### 3.2 Finding Severity Triage

| GuardDuty Severity | Meridian Severity | Action Required |
|--------------------|-------------------|-----------------|
| High (7.0 - 8.9) | P2 | Immediate investigation, notify SOC Manager |
| Medium (4.0 - 6.9) | P3 | Investigate within 2 hours |
| Low (1.0 - 3.9) | P4 | Review during shift, document in daily report |

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) for full severity mapping and escalation matrix.

### 3.3 Common GuardDuty Finding Types

#### Credential-Based Findings

| Finding Type | Description | Investigation Steps |
|-------------|-------------|---------------------|
| `UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B` | Console login from unusual IP | Check IP reputation, verify with user, check for MFA |
| `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS` | EC2 instance credentials used outside AWS | Immediately rotate credentials, check CloudTrail |
| `CredentialAccess:IAMUser/AnomalousBehavior` | API calls inconsistent with user baseline | Review CloudTrail events, compare to normal pattern |

#### Network-Based Findings

| Finding Type | Description | Investigation Steps |
|-------------|-------------|---------------------|
| `Backdoor:EC2/C&CActivity.B!DNS` | EC2 instance querying C2 domain | Isolate instance, check DNS logs, investigate process |
| `CryptoCurrency:EC2/BitcoinTool.B!DNS` | EC2 instance querying bitcoin-related domain | Check for unauthorized mining, review instance launch |
| `Trojan:EC2/DNSDataExfiltration` | DNS tunneling from EC2 instance | Isolate instance, collect forensics |

#### S3-Based Findings

| Finding Type | Description | Investigation Steps |
|-------------|-------------|---------------------|
| `Policy:S3/BucketPublicAccessGranted` | S3 bucket made public | Immediately revert, check for data exposure |
| `Exfiltration:S3/AnomalousBehavior` | Unusual S3 data access pattern | Check CloudTrail for GetObject calls, verify user |
| `Discovery:S3/MaliciousIPCaller.Custom` | S3 API calls from known malicious IP | Block IP, investigate IAM principal |

### 3.4 GuardDuty Investigation via CLI

List recent high-severity findings:

```bash
aws guardduty list-findings \
  --detector-id <DETECTOR_ID> \
  --finding-criteria '{"Criterion":{"severity":{"Gte":7},"updatedAt":{"GreaterThanOrEqual":1700000000000}}}' \
  --profile meridian-security \
  --region us-east-1
```

Get details for a specific finding:

```bash
aws guardduty get-findings \
  --detector-id <DETECTOR_ID> \
  --finding-ids "<FINDING_ID>" \
  --profile meridian-security \
  --region us-east-1 \
  | jq '.Findings[0] | {Type, Severity, Title, Description, Resource, Service}'
```

### 3.5 GuardDuty Findings in Splunk

```spl
index=cloud sourcetype=aws:guardduty
| where severity >= 7
| table _time, title, type, severity, accountId, region, resource.instanceDetails.instanceId
| sort -severity, -_time
```

## 4. AWS CloudTrail

### 4.1 Overview

CloudTrail is enabled in all accounts with organization-level trail. Logs are stored in the `meridian-cloudtrail-logs` S3 bucket in the security account with a 365-day retention policy. Logs are also forwarded to Splunk (`index=cloud sourcetype=aws:cloudtrail`).

### 4.2 Common Investigation Queries

#### Trace all actions by a specific IAM user:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=Username,AttributeValue="<USERNAME>" \
  --start-time "2025-11-01T00:00:00Z" \
  --end-time "2025-11-15T00:00:00Z" \
  --profile meridian-security \
  --region us-east-1 \
  | jq '.Events[] | {EventTime, EventName, Username: .Username, SourceIP: .CloudTrailEvent | fromjson | .sourceIPAddress}'
```

#### Find who created or modified a specific resource:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue="<RESOURCE_ARN>" \
  --profile meridian-security \
  --region us-east-1 \
  | jq '.Events[] | {EventTime, EventName, Username: .Username}'
```

#### Search for sensitive API calls:

```bash
# Search for IAM policy changes
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue="PutUserPolicy" \
  --start-time "2025-11-01T00:00:00Z" \
  --profile meridian-security \
  --region us-east-1

# Search for security group changes
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue="AuthorizeSecurityGroupIngress" \
  --start-time "2025-11-01T00:00:00Z" \
  --profile meridian-security \
  --region us-east-1
```

### 4.3 CloudTrail in Splunk

Search for unauthorized API calls (access denied):

```spl
index=cloud sourcetype=aws:cloudtrail errorCode="AccessDenied" OR errorCode="UnauthorizedAccess"
| stats count by userIdentity.userName, eventName, sourceIPAddress, errorCode
| where count > 5
| sort -count
```

Detect IAM user creation or privilege escalation:

```spl
index=cloud sourcetype=aws:cloudtrail
| search eventName IN ("CreateUser", "CreateAccessKey", "AttachUserPolicy", "PutUserPolicy", "AddUserToGroup", "CreateLoginProfile")
| table _time, userIdentity.userName, eventName, requestParameters, sourceIPAddress
| sort -_time
```

> **See:** [Tool Guide: Splunk (SOC-TG-004)](04-tool-guide-splunk.md) — Section 7 for additional CloudTrail SPL queries.

## 5. AWS Security Hub

### 5.1 Overview

Security Hub aggregates findings from GuardDuty, Inspector, Macie, IAM Access Analyzer, and Firewall Manager into a single dashboard. It also runs CIS AWS Foundations Benchmark and AWS Foundational Security Best Practices checks.

### 5.2 Compliance Standards Enabled

| Standard | Status | Target Score |
|----------|--------|-------------|
| CIS AWS Foundations Benchmark v1.4.0 | Active | > 90% |
| AWS Foundational Security Best Practices v1.0.0 | Active | > 95% |
| PCI DSS v3.2.1 | Active | > 95% |
| NIST 800-53 Rev 5 | Active | > 85% |

### 5.3 Security Hub CLI Queries

Get critical and high findings:

```bash
aws securityhub get-findings \
  --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"},{"Value":"HIGH","Comparison":"EQUALS"}],"WorkflowStatus":[{"Value":"NEW","Comparison":"EQUALS"}]}' \
  --profile meridian-security \
  --region us-east-1 \
  | jq '.Findings[] | {Title, Severity: .Severity.Label, Account: .AwsAccountId, Resource: .Resources[0].Id}'
```

## 6. Containment Actions

### 6.1 Quarantine an EC2 Instance

Apply the quarantine security group that blocks all inbound and outbound traffic except SSM:

```bash
# Get current security groups (save for restoration)
aws ec2 describe-instances \
  --instance-ids <INSTANCE_ID> \
  --query 'Reservations[].Instances[].SecurityGroups' \
  --profile meridian-security \
  --region us-east-1

# Apply quarantine security group
aws ec2 modify-instance-attribute \
  --instance-id <INSTANCE_ID> \
  --groups sg-0a1b2c3d4e5f67890 \
  --profile meridian-security \
  --region us-east-1
```

### 6.2 Disable an IAM Access Key

```bash
aws iam update-access-key \
  --user-name <USERNAME> \
  --access-key-id <ACCESS_KEY_ID> \
  --status Inactive \
  --profile meridian-security
```

### 6.3 Revoke IAM Role Sessions

```bash
aws iam put-role-policy \
  --role-name <ROLE_NAME> \
  --policy-name RevokeOlderSessions \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "DateLessThan": {
          "aws:TokenIssueTime": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
        }
      }
    }]
  }' \
  --profile meridian-security
```

### 6.4 S3 Bucket Emergency Lockdown

If a bucket is found to be publicly accessible or compromised:

```bash
# Block all public access
aws s3api put-public-access-block \
  --bucket <BUCKET_NAME> \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
  --profile meridian-security

# Add deny-all bucket policy temporarily
aws s3api put-bucket-policy \
  --bucket <BUCKET_NAME> \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [{
      "Sid": "EmergencyDenyAll",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::<BUCKET_NAME>/*"
    }]
  }' \
  --profile meridian-security
```

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact Lisa Tran (lisa.tran@meridianbank.com) or post in Slack #soc-cloud-security.*
