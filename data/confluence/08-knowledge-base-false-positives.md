# Knowledge Base: Common False Positive Patterns and Tuning Guidance

| Field          | Value                                                   |
|----------------|---------------------------------------------------------|
| **Document ID**   | SOC-KB-008                                           |
| **Title**         | False Positive Patterns and Alert Tuning Guide       |
| **Author**        | Mike O'Brien, Sarah Mitchell                          |
| **Last Updated**  | 2025-12-10                                            |
| **Status**        | Active                                                |
| **Review Cycle**  | Quarterly                                             |
| **Classification**| Internal — Meridian National Bank                      |

---

## 1. Purpose

This knowledge base documents known false positive (FP) patterns observed in Meridian SOC alert sources. It provides tuning guidance for analysts triaging alerts and serves as a reference for the Detection Engineering team when reviewing and refining correlation rules.

**Important:** Before closing an alert as a false positive, verify it matches a documented pattern below. If unsure, escalate to a Tier 2 analyst. Attackers sometimes mimic legitimate activity — always validate context.

## 2. Email Security False Positives

### 2.1 Marketing and Bulk Email Platforms

**Alert:** `SOC-CORR-EMAIL-001: Phishing — Suspicious Sender Delivered`

**Pattern:** Proofpoint flags emails from legitimate marketing platforms due to sender reputation scoring. The following domains are approved third-party senders for Meridian:

| Domain | Service | Approved By | Review Date |
|--------|---------|-------------|-------------|
| `*.mailchimp.com` | Marketing campaigns (HR, Corporate Comms) | Sarah Mitchell | 2025-09-15 |
| `*.sendgrid.net` | Transactional emails (IT notifications) | Mike O'Brien | 2025-09-15 |
| `*.hubspot.com` | Customer relationship management | Marketing Ops | 2025-10-01 |
| `*.constantcontact.com` | Employee newsletter | HR Department | 2025-08-20 |
| `*.salesforce.com` | CRM notifications | Sales Ops | 2025-09-01 |

**Tuning:** These domains are in the Proofpoint allowlist. If alerts still trigger, verify the specific sending subdomain and update the allowlist entry. Do not blanket-allow top-level domains.

> **See:** [Phishing Runbook (SOC-RB-001)](01-runbook-phishing.md) — Section 5.3 for IOC enrichment steps that help distinguish FPs from real phishing.

### 2.2 Internal Phishing Simulations

**Alert:** `SOC-CORR-EMAIL-001` through `SOC-CORR-EMAIL-014`

**Pattern:** Meridian runs monthly phishing simulations via **KnowBe4**. Simulation emails originate from:
- Sender domains: `*.training.knowbe4.com`
- Sending IPs: `147.160.167.0/24`
- Custom header: `X-KnowBe4-SimulationId: <UUID>`

**Tuning:** Phishing simulations are tagged in Proofpoint with the `X-KnowBe4-SimulationId` header. Splunk alerts include a lookup filter (`SOC-FP-PhishSim`) that suppresses known simulation senders. If a new simulation campaign triggers alerts, update the lookup table:

```spl
| inputlookup soc_fp_phishsim.csv
| append [| makeresults | eval sender="new-campaign@training.knowbe4.com", campaign_id="KB4-2025-12", active="true"]
| outputlookup soc_fp_phishsim.csv
```

### 2.3 Email Encryption and Secure Delivery Services

**Alert:** `SOC-CORR-EMAIL-005: Suspicious Attachment Type`

**Pattern:** Encrypted email services (Zix, Proofpoint Encryption) wrap emails in HTML attachments that trigger the suspicious attachment rule. Common FP sources:

- Zix encrypted messages: Attachment named `SecureMessageAtt.html`
- Proofpoint Encryption: Attachment named `Secure Message.html`
- Bank-to-bank SWIFT acknowledgments: PDF attachments from `*.swift.com`

**Tuning:** These patterns are in the allowlist for `SOC-CORR-EMAIL-005`. If new encrypted email patterns emerge, submit a tuning request.

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md) for the tuning request workflow.

## 3. Endpoint Security False Positives

### 3.1 Developer and IT Admin Tools

**Alert:** `SOC-DET-MAL-001: EDR — CrowdStrike Critical/High Severity`

**Pattern:** CrowdStrike frequently flags legitimate developer and IT administration tools. The following are known FP sources at Meridian:

| Tool | Process Path | User Group | FP Reason |
|------|-------------|------------|-----------|
| Python | `C:\Python311\python.exe` | Developers | Process injection detection (test frameworks) |
| Node.js | `C:\Program Files\nodejs\node.exe` | Developers | Suspicious child process spawning |
| PowerShell ISE | `C:\Windows\System32\WindowsPowerShell\*` | IT Admins | Encoded command execution |
| Chocolatey | `C:\ProgramData\chocolatey\*` | IT Admins | Downloading executables |
| PuTTY | `C:\Program Files\PuTTY\putty.exe` | IT/Network | Outbound SSH connection |
| WinSCP | `C:\Program Files\WinSCP\WinSCP.exe` | IT/Operations | File transfer flagged as exfil |
| Terraform | `C:\Users\*\.terraform\*` | Cloud Engineers | Process execution from user profile |
| Visual Studio | `C:\Program Files\Microsoft Visual Studio\*` | Developers | Compiler behavior flagged |

**Tuning:** These tools are managed via CrowdStrike **Machine Learning Exclusions** and **IOA Exclusions** applied to the `Meridian-Developers` and `Meridian-IT-Admins` host groups. If a new tool generates FPs, submit a CrowdStrike exclusion request via ServiceNow.

**Caution:** Always verify the process path matches exactly. Attackers commonly rename malicious binaries to match legitimate tool names (e.g., `python.exe` in `C:\Users\Public\`). A `python.exe` running from a non-standard path is **NOT** a false positive.

### 3.2 Vulnerability Scanning

**Alert:** Multiple CrowdStrike and Splunk correlation alerts

**Pattern:** Scheduled vulnerability scans from Tenable.io generate alerts for:
- Port scanning behavior
- Authentication attempts (credentialed scans)
- Web application testing (XSS/SQLi payloads in logs)

**Known scanner IPs:**
- `10.128.50.10` — Internal Tenable scanner (corporate network)
- `10.128.50.11` — Internal Tenable scanner (DMZ)
- `10.50.50.10` — Cloud Tenable scanner (AWS VPC)
- `44.238.0.0/16` — Tenable.io cloud scanners (external)

**Scan windows:**
- Weekly full scan: Saturday 02:00-08:00 ET
- Daily differential: 03:00-04:00 ET
- Ad-hoc scans: Announced in `#soc-general` with ticket number

**Tuning:** Scanner IPs are in the `soc_fp_scanners.csv` lookup in Splunk. Correlation rules reference this lookup to suppress scanner-sourced alerts during scan windows.

### 3.3 Authorized Penetration Testing

**Alert:** Various — depends on engagement scope

**Pattern:** Meridian conducts annual penetration tests (typically Q2) and ad-hoc red team exercises. During authorized testing:

1. The SOC Manager will announce the test in `#soc-general` and `#soc-incidents`
2. Tester IP ranges and timeframes are documented in a ServiceNow ticket
3. A temporary suppression list is added to Splunk

**Important:** Even during authorized tests, P1 alerts should still be triaged normally. Only suppress alerts that match the documented scope (IP ranges, timeframe, techniques).

## 4. Authentication False Positives

### 4.1 Service Account Noise

**Alert:** `SOC-CORR-AUTH-001: Brute Force Detection`

**Pattern:** Several service accounts generate high volumes of authentication events that trigger brute force alerts:

| Service Account | Source System | Expected Behavior |
|----------------|--------------|-------------------|
| `svc_splunk_forwarder` | Splunk universal forwarders | Auth from all endpoints (~2000 hosts) |
| `svc_crowdstrike` | CrowdStrike sensor updates | Auth from CS management server (10.128.10.50) |
| `svc_backup_agent` | Commvault backup | Auth to file servers nightly (01:00-04:00 ET) |
| `svc_monitoring` | SolarWinds | SNMP/WMI polling every 5 minutes across all servers |
| `svc_adconnect` | Azure AD Connect | Syncing every 30 minutes from 10.128.5.100 |
| `svc_patching` | SCCM/MECM | Auth to endpoints during patch windows (Tue/Wed) |
| `svc_sql_reporting` | SQL Server Reporting Services | Auth to database servers hourly |

**Tuning:** Service accounts are in the `soc_fp_svc_accounts.csv` lookup. The brute force correlation rule (`SOC-CORR-AUTH-001`) excludes these accounts but monitors them separately with higher thresholds:

```spl
index=auth sourcetype=windows:security EventCode=4625
| search user="svc_*"
| lookup soc_fp_svc_accounts.csv user OUTPUT expected_src, expected_threshold
| where src_ip != expected_src OR count > expected_threshold
| table _time, user, src_ip, expected_src, count, expected_threshold
```

> **See:** [Tool Guide: Splunk (SOC-TG-004)](04-tool-guide-splunk.md) — Section 3.4 for service account anomaly detection queries.

### 4.2 VPN Reconnection Storms

**Alert:** `SOC-CORR-AUTH-002: Impossible Travel`

**Pattern:** When the Cisco AnyConnect VPN gateway performs maintenance or failover, hundreds of users reconnect simultaneously from their home IPs. This triggers impossible travel alerts because the previous login was from a corporate IP and the new login is from a residential IP within minutes.

**Tuning:** The impossible travel rule includes a 30-minute grace period after known VPN gateway maintenance windows. If an unplanned failover occurs, manually add a suppression window:

1. Update `soc_fp_vpn_maintenance.csv` with the outage window
2. Note the ServiceNow incident number for the VPN outage
3. Bulk-close triggered alerts referencing the VPN outage ticket

### 4.3 Shared Workstation Authentication

**Alert:** `SOC-CORR-AUTH-003: Multiple Users Same Source`

**Pattern:** Shared workstations in the following locations generate alerts for multiple users authenticating from the same IP:

- Trading floor (10.128.100.0/24) — shared Bloomberg terminals
- Branch teller stations (various branch IPs) — shift changes
- Conference rooms (10.128.200.0/24) — hot-desking
- ATM management consoles (172.20.5.0/24) — operator access

**Tuning:** These subnets are in the `soc_fp_shared_workstations.csv` lookup and are excluded from the multi-user-same-source rule.

## 5. AWS and Cloud False Positives

### 5.1 Terraform and Infrastructure as Code

**Alert:** `SOC-CORR-CLOUD-002: IAM Policy Change` and `SOC-CORR-CLOUD-003: Security Group Modified`

**Pattern:** Terraform deployments via the CI/CD pipeline generate a high volume of IAM and security group change events. These come from:

- IAM role: `meridian-terraform-deploy`
- Source IP: `10.54.20.0/24` (CI/CD subnet)
- User agent: `aws-sdk-go/1.* (terraform-provider-aws/*)`

**Tuning:** CloudTrail events from the Terraform role are filtered by the `soc_fp_cicd.csv` lookup. Changes are still logged but don't generate alerts unless the change affects production accounts and occurs outside the deployment window (Mon-Fri 09:00-17:00 ET).

### 5.2 Auto-Scaling Events

**Alert:** `SOC-CORR-CLOUD-005: New EC2 Instance Launched`

**Pattern:** Auto-scaling groups in production launch and terminate instances frequently. These are expected:

| ASG Name | Account | Normal Range |
|----------|---------|-------------|
| `asg-web-prod` | meridian-prod | 4-20 instances |
| `asg-api-prod` | meridian-prod | 6-30 instances |
| `asg-batch-prod` | meridian-prod | 0-50 instances |

**Tuning:** ASG-launched instances are identified by the `aws:autoscaling:groupName` tag and suppressed from the new instance alert.

### 5.3 GuardDuty Low-Severity Noise

**Alert:** GuardDuty findings with severity < 4.0

**Pattern:** Common low-severity findings that are generally informational:
- `Recon:EC2/PortProbeUnprotectedPort` — Internet-facing load balancers
- `UnauthorizedAccess:EC2/SSHBruteForce` — Bastion hosts (expected external access attempts)
- `Policy:IAMUser/RootCredentialUsage` — Quarterly root account audits by Cloud Security team

**Tuning:** These finding types are in the GuardDuty **Suppression Rules** with auto-archive enabled. They are still visible in Security Hub for compliance reporting.

> **See:** [Tool Guide: AWS Security (SOC-TG-005)](05-tool-guide-aws-security.md) — Section 3 for GuardDuty finding severity mapping.

## 6. Network False Positives

### 6.1 Backup and Replication Traffic

**Alert:** `SOC-CORR-NET-003: Large Outbound Data Transfer`

**Pattern:** Nightly backup replication to the DR site generates large outbound transfers:
- Source: `10.128.30.0/24` (backup infrastructure)
- Destination: `10.200.30.0/24` (DR site via MPLS)
- Window: 22:00-06:00 ET daily
- Volume: 500GB-2TB nightly

**Tuning:** Backup subnets are excluded from the data exfiltration rule during the backup window.

### 6.2 Software Update Traffic

**Alert:** `SOC-CORR-NET-001: C2 Beaconing Detected`

**Pattern:** Software update mechanisms can mimic C2 beaconing due to regular polling intervals:
- CrowdStrike sensor updates: every 5 min to `*.crowdstrike.com`
- SCCM client check-in: every 60 min to `10.128.10.20`
- Splunk forwarder heartbeat: every 30 sec to `10.128.10.30`

**Tuning:** Known update destinations are in the `soc_fp_update_servers.csv` lookup and excluded from beaconing detection.

## 7. Tuning Request Process

If you identify a new false positive pattern not documented here:

1. **Do not** modify detection rules directly
2. Document the pattern in a ServiceNow ticket (category: `Security > Detection Engineering`)
3. Include:
   - Alert rule ID that triggered
   - At least 5 examples of the FP with timestamps
   - Proposed tuning approach (if known)
   - Risk assessment: what would we miss if we suppress this pattern?
4. Tag Mike O'Brien as assignee

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md) for the full change management workflow for detection rules.

## 8. False Positive Metrics

The Detection Engineering team tracks the following metrics quarterly:

| Metric | Q3 2025 | Q4 2025 (Target) |
|--------|---------|-------------------|
| Overall FP rate (all alerts) | 34% | < 25% |
| Email security FP rate | 28% | < 20% |
| Endpoint security FP rate | 41% | < 30% |
| Authentication FP rate | 38% | < 25% |
| Cloud security FP rate | 22% | < 15% |
| Network security FP rate | 19% | < 15% |

**Goal:** Reduce the overall false positive rate to below 25% by Q1 2026 through systematic tuning and rule refinement.

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact Mike O'Brien (mike.obrien@meridianbank.com) or Sarah Mitchell (sarah.mitchell@meridianbank.com).*
