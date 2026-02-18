# Tool Guide: Splunk — Common SOC Investigation Queries

| Field          | Value                                        |
|----------------|----------------------------------------------|
| **Document ID**   | SOC-TG-004                                |
| **Title**         | Splunk Query Reference for SOC Analysts   |
| **Author**        | Mike O'Brien                               |
| **Last Updated**  | 2025-11-20                                 |
| **Status**        | Active                                     |
| **Review Cycle**  | Quarterly                                  |
| **Classification**| Internal — Meridian National Bank           |

---

## 1. Purpose

This document provides a curated library of Splunk SPL queries commonly used by Meridian SOC analysts during investigations. Queries are organized by investigation type and include explanations, expected output, and tuning guidance.

## 2. Splunk Environment Overview

| Component | Details |
|-----------|---------|
| Splunk Version | 9.1.2 Enterprise |
| Search Head URL | `https://splunk-sh.meridian.internal:8089` |
| Deployment | Clustered (3 search heads, 12 indexers) |
| Default Search Window | Last 24 hours (adjust as needed) |
| License | 500 GB/day ingest |

### 2.1 Key Indexes

| Index | Sourcetype(s) | Description | Retention |
|-------|--------------|-------------|-----------|
| `auth` | `windows:security`, `azure:ad`, `linux:auth` | Authentication events | 365 days |
| `endpoint` | `crowdstrike:events`, `crowdstrike:detections` | Endpoint telemetry | 180 days |
| `email` | `proofpoint:tap`, `proofpoint:tap:clicks` | Email security events | 365 days |
| `network` | `pan:traffic`, `pan:threat`, `stream:dns` | Network traffic and DNS | 90 days |
| `cloud` | `aws:cloudtrail`, `aws:guardduty`, `azure:activity` | Cloud service logs | 365 days |
| `proxy` | `bluecoat:proxy`, `zscaler:web` | Web proxy logs | 90 days |
| `threat_intel` | `ioc_feed`, `misp:events` | Threat intelligence data | Unlimited |

## 3. Authentication Investigation Queries

### 3.1 Failed Authentication — Brute Force Detection

```spl
index=auth sourcetype=windows:security EventCode=4625
| bin _time span=5m
| stats count by src_ip, user, dest, _time
| where count > 10
| sort -count
```

**Use case:** Detect brute force attempts. Threshold of 10 failures in 5 minutes.

### 3.2 Successful Login After Multiple Failures

```spl
index=auth sourcetype=windows:security EventCode IN (4625, 4624)
| sort _time
| streamstats count(eval(EventCode=4625)) AS fail_count count(eval(EventCode=4624)) AS success_count by user, src_ip
| where EventCode=4624 AND fail_count > 5
| table _time, user, src_ip, dest, fail_count
```

**Use case:** Identify successful credential stuffing. Indicates potential compromised account.

### 3.3 Logon from Unusual Location

```spl
index=auth sourcetype=azure:ad
| search ResultType=0
| iplocation ClientIP
| where NOT (Country="United States" OR Country="Canada" OR Country="United Kingdom")
| table _time, UserPrincipalName, ClientIP, Country, City, AppDisplayName
| sort -_time
```

**Use case:** Flag logins from countries where Meridian has no operations.

### 3.4 Service Account Anomalies

```spl
index=auth sourcetype=windows:security EventCode=4624
| search user="svc_*"
| stats dc(src_ip) AS unique_sources, values(src_ip) AS source_ips by user
| where unique_sources > 3
| sort -unique_sources
```

**Use case:** Service accounts should authenticate from predictable sources. Multiple sources may indicate credential theft.

> **See:** [Knowledge Base: False Positives (SOC-KB-008)](08-knowledge-base-false-positives.md) — Section 4 covers known service account patterns that generate false positive alerts.

## 4. Email Security Queries

### 4.1 Phishing Email Search by Sender

```spl
index=email sourcetype=proofpoint:tap
| search sender="*@<suspicious_domain>"
| stats count by recipient, subject, action, threatsInfoMap{}.classification
| sort -count
```

### 4.2 URL Click Analysis

```spl
index=email sourcetype=proofpoint:tap:clicks
| search url="*<suspicious_url_pattern>*"
| stats count by recipient, url, clickTime, classification
| sort -clickTime
```

### 4.3 Email with Suspicious Attachment Types

```spl
index=email sourcetype=proofpoint:tap
| search attachmentTypes IN ("application/x-msdownload", "application/x-iso9660-image", "application/vnd.ms-htmlhelp", "application/zip")
| where action="delivered"
| table _time, sender, recipient, subject, attachmentNames, attachmentTypes
| sort -_time
```

**Use case:** Detect delivery of potentially malicious file types. Cross-reference with the phishing runbook.

> **See:** [Phishing Runbook (SOC-RB-001)](01-runbook-phishing.md) — Section 5.2 for the full email investigation workflow.

## 5. Malware and Endpoint Queries

### 5.1 Process Execution by Hash

```spl
index=endpoint sourcetype=crowdstrike:events event_type="ProcessRollup2"
| search SHA256HashData="<HASH>"
| table _time, ComputerName, UserName, FileName, FilePath, CommandLine, ParentBaseFileName
| sort _time
```

### 5.2 PowerShell Suspicious Commands

```spl
index=endpoint sourcetype=crowdstrike:events
| search FileName="powershell.exe" OR FileName="pwsh.exe"
| where match(CommandLine, "(?i)(encodedcommand|invoke-expression|iex|downloadstring|invoke-webrequest|frombase64)")
| table _time, ComputerName, UserName, CommandLine, ParentBaseFileName
| sort -_time
```

### 5.3 Lateral Movement Indicators

```spl
index=endpoint sourcetype=crowdstrike:events
| search event_type="ProcessRollup2"
| where (FileName IN ("psexec.exe","psexec64.exe","wmic.exe") OR match(CommandLine, "(?i)(invoke-command|enter-pssession|new-pssession|invoke-wmimethod)"))
| table _time, ComputerName, UserName, FileName, CommandLine, ParentBaseFileName
| sort -_time
```

> **See:** [Malware Runbook (SOC-RB-002)](02-runbook-malware.md) for the full malware investigation procedure.

## 6. Network Investigation Queries

### 6.1 Outbound Traffic to Rare Destinations

```spl
index=network sourcetype=pan:traffic direction=outbound
| stats sum(bytes_out) AS total_bytes, count by dest_ip, dest_port, app
| where count < 5 AND total_bytes > 10485760
| sort -total_bytes
| iplocation dest_ip
| table dest_ip, dest_port, app, total_bytes, Country, City
```

**Use case:** Detect data exfiltration to unusual destinations. Threshold: >10MB to a destination seen fewer than 5 times.

### 6.2 DNS Tunneling Detection

```spl
index=dns sourcetype=stream:dns
| eval query_length=len(query)
| where query_length > 50
| stats count, avg(query_length) AS avg_len, max(query_length) AS max_len by src_ip, query
| where count > 100 AND avg_len > 60
| sort -count
```

### 6.3 Beaconing Detection

```spl
index=network sourcetype=pan:traffic direction=outbound
| bin _time span=1m
| stats count by src_ip, dest_ip, dest_port, _time
| streamstats current=f last(_time) AS prev_time by src_ip, dest_ip, dest_port
| eval interval=_time-prev_time
| stats stdev(interval) AS interval_stdev, avg(interval) AS interval_avg, count by src_ip, dest_ip, dest_port
| where interval_stdev < 30 AND count > 50 AND interval_avg > 0
| sort interval_stdev
```

**Use case:** Detect C2 beaconing behavior. Low standard deviation in connection intervals indicates programmatic communication.

## 7. AWS CloudTrail Queries

### 7.1 IAM Key Usage from New IP

```spl
index=cloud sourcetype=aws:cloudtrail
| search userIdentity.type="IAMUser"
| stats earliest(_time) AS first_seen, count by userIdentity.userName, sourceIPAddress
| where first_seen > relative_time(now(), "-24h")
| table userIdentity.userName, sourceIPAddress, first_seen, count
| sort -first_seen
```

### 7.2 Console Login Without MFA

```spl
index=cloud sourcetype=aws:cloudtrail eventName=ConsoleLogin
| where NOT additionalEventData.MFAUsed="Yes"
| table _time, userIdentity.userName, sourceIPAddress, responseElements.ConsoleLogin
| sort -_time
```

> **See:** [Tool Guide: AWS Security (SOC-TG-005)](05-tool-guide-aws-security.md) for additional CloudTrail analysis and GuardDuty triage procedures.

## 8. Saved Searches and Dashboards

### 8.1 Key Saved Searches

| Saved Search Name | Schedule | Alert Action |
|-------------------|----------|--------------|
| `SOC-CORR-AUTH-001: Brute Force` | Every 5 min | Slack #soc-alerts, ServiceNow |
| `SOC-CORR-AUTH-002: Impossible Travel` | Every 15 min | Slack #soc-alerts |
| `SOC-CORR-EMAIL-001: Phishing Delivered` | Every 5 min | Slack #soc-alerts, ServiceNow |
| `SOC-CORR-MAL-001: EDR Critical Alert` | Every 1 min | Slack #soc-alerts, PagerDuty, ServiceNow |
| `SOC-CORR-NET-001: C2 Beaconing` | Every 15 min | Slack #soc-alerts, ServiceNow |
| `SOC-CORR-CLOUD-001: GuardDuty High` | Every 5 min | Slack #soc-alerts, ServiceNow |

### 8.2 Key Dashboards

| Dashboard | URL |
|-----------|-----|
| SOC Overview | `https://splunk-sh.meridian.internal/app/soc/overview` |
| Active Incidents | `https://splunk-sh.meridian.internal/app/soc/incidents` |
| Email Security | `https://splunk-sh.meridian.internal/app/soc/email_security` |
| Authentication Monitoring | `https://splunk-sh.meridian.internal/app/soc/auth_monitor` |
| Network Anomalies | `https://splunk-sh.meridian.internal/app/soc/network_anomalies` |
| Cloud Security | `https://splunk-sh.meridian.internal/app/soc/cloud_security` |

## 9. Query Performance Tips

- Always specify an index and sourcetype to avoid scanning unnecessary data.
- Use `earliest` and `latest` to limit the time range (e.g., `earliest=-24h latest=now`).
- Avoid `search *` — always include at least one filtering field.
- Use `tstats` instead of `search` for indexed fields when performance is critical:

```spl
| tstats count where index=auth by _time, host, source
| timechart span=1h count by host
```

- For large result sets, use `| head 1000` during initial investigation.
- Save commonly used base searches as macros to improve consistency.

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact Mike O'Brien (mike.obrien@meridianbank.com) or post in Slack #soc-general.*
