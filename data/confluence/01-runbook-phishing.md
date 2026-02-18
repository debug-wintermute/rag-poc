# Runbook: Phishing Email Incident Response

| Field          | Value                                      |
|----------------|--------------------------------------------|
| **Document ID**   | SOC-RB-001                              |
| **Title**         | Phishing Email Incident Response Runbook |
| **Author**        | Sarah Mitchell                           |
| **Last Updated**  | 2025-11-14                               |
| **Status**        | Active                                   |
| **Review Cycle**  | Quarterly                                |
| **Classification**| Internal — Meridian National Bank        |

---

## 1. Purpose

This runbook provides step-by-step instructions for Meridian SOC analysts to triage, investigate, contain, and remediate phishing email incidents targeting Meridian National Bank employees and customers. It covers both commodity phishing and targeted spear-phishing campaigns.

## 2. Scope

This procedure applies to:
- Phishing emails reported via the **Report Phish** button in Outlook
- Proofpoint TAP alerts for delivered malicious emails
- Alerts from Splunk correlation rules (e.g., `SOC-CORR-EMAIL-001` through `SOC-CORR-EMAIL-014`)
- Escalations from the help desk regarding suspicious emails

## 3. Severity Classification

| Scenario | Severity | SLA Response |
|----------|----------|--------------|
| Mass commodity phishing, no clicks | P4 | 4 hours |
| Phishing with credential harvesting link, < 5 clicks | P3 | 2 hours |
| Spear-phishing targeting executives or finance | P2 | 30 minutes |
| Confirmed credential compromise or BEC | P1 | 15 minutes |
| Phishing with malware payload delivered and executed | P1 | 15 minutes |

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) for full severity definitions and escalation matrix.

## 4. Required Tools and Access

- **Proofpoint TAP Console** — Email threat analysis and quarantine
- **Splunk** — Log correlation and mailbox activity search
- **Microsoft 365 Admin Center** — Mailbox search and purge
- **CrowdStrike Falcon** — Endpoint investigation if payload executed
- **ServiceNow** — Incident ticketing (category: `Security > Phishing`)
- **VirusTotal / URLhaus** — IOC enrichment

## 5. Triage Procedure

### 5.1 Initial Assessment

1. Open the alert in Splunk or Proofpoint TAP dashboard.
2. Identify the following attributes:
   - Sender address and sending IP
   - Subject line
   - Recipients (count and department distribution)
   - Whether the email contains URLs, attachments, or both
   - Delivery status (delivered, quarantined, blocked)
3. Check if this matches a known false positive pattern.

> **See:** [Knowledge Base: False Positives (SOC-KB-008)](08-knowledge-base-false-positives.md) — Section 2 covers common email security false positives including marketing platforms and legitimate bulk senders.

### 5.2 Splunk Queries for Email Investigation

Search for all recipients of a suspicious email by subject and sender:

```spl
index=email sourcetype=proofpoint:tap
| search sender="*@suspicious-domain.com" subject="*Invoice*"
| stats count by recipient, action, messageTime
| sort -messageTime
```

Check if any recipient clicked a URL in the email:

```spl
index=email sourcetype=proofpoint:tap:clicks
| search sender="*@suspicious-domain.com"
| table _time, recipient, url, clickTime, userAgent
| sort -clickTime
```

Search for email forwarding rules that may indicate compromise:

```spl
index=o365 sourcetype=ms:o365:management
| search Operation="New-InboxRule" OR Operation="Set-InboxRule"
| where like(Parameters, "%ForwardTo%") OR like(Parameters, "%RedirectTo%")
| table _time, UserId, Operation, Parameters
```

> **See:** [Tool Guide: Splunk (SOC-TG-004)](04-tool-guide-splunk.md) for the full library of email-related SPL queries.

### 5.3 IOC Enrichment

1. Extract all URLs and domains from the email body and headers.
2. Check each against:
   - **VirusTotal** — Look for detection ratio > 3/70
   - **URLhaus** — Check for known malware distribution
   - **Proofpoint TAP Forensics** — Automated sandbox results
   - **Internal IOC feed** — `index=threat_intel sourcetype=ioc_feed`
3. Extract attachment hashes (MD5, SHA256) and query:

```spl
index=threat_intel sourcetype=ioc_feed
| search ioc_type="hash" ioc_value="<SHA256_HASH>"
| table ioc_value, ioc_source, threat_actor, first_seen
```

4. Document all IOCs in the ServiceNow ticket under the **Indicators** tab.

## 6. Containment Actions

### 6.1 Email Quarantine and Purge

If the email is confirmed malicious and was delivered to user mailboxes:

1. **Proofpoint TAP**: Use the **Search and Destroy** feature:
   - Navigate to **Forensics > Search**
   - Enter the sender, subject, or message ID
   - Select all matching messages → **Quarantine**

2. **Microsoft 365 Compliance Center** (if Proofpoint purge is insufficient):
   - Open **Content Search** in the M365 Compliance portal
   - Create a new search with the following KQL:

```
from:<sender@malicious-domain.com> AND subject:"<subject line>" AND received:2025-11-01..2025-11-14
```

   - Review results, then run **Purge** action (soft delete or hard delete as appropriate).

3. Log the purge action in ServiceNow with the count of messages removed.

### 6.2 Block Sender and Domain

1. Add the sender domain to the Proofpoint blocklist:
   - **Email Protection > Blocklist > Domains**
   - Add entry with expiration (default: 30 days)

2. If the sending IP is identifiable, submit a firewall block request:
   - Palo Alto: Create a request in ServiceNow (category: `Network > Firewall Rule`)
   - Include source IP, direction (inbound), and justification

### 6.3 Credential Reset (If Applicable)

If any user clicked a credential harvesting link and submitted credentials:

1. Force password reset via Active Directory:
   - Contact the Identity team via Slack `#iam-ops` or ServiceNow
2. Revoke all active sessions for the affected user:
   - Azure AD: **Users > [User] > Revoke Sessions**
   - On-prem AD: Reset the user's `krbtgt` ticket if Kerberos compromise suspected
3. Enable enhanced monitoring for the affected account for 72 hours:

```spl
index=auth sourcetype=windows:security OR sourcetype=azure:ad
| search user="<affected_user>"
| stats count by action, src_ip, dest, app
| where count > 5
```

## 7. User Notification

Send the following notification to users who received the phishing email:

> **Subject:** Security Notice — Suspicious Email Removed
>
> Dear [Employee Name],
>
> Our security team has identified a suspicious email that was delivered to your mailbox. The email has been quarantined and removed. The email appeared to come from [sender] with the subject line "[subject]".
>
> **If you clicked any links or opened any attachments in this email, please contact the IT Security team immediately at ext. 4422 or via Slack #security-help.**
>
> If you did not interact with the email, no further action is required.
>
> Thank you for your vigilance.
> — Meridian Cyber Defense Center

## 8. Escalation Triggers

Escalate to **P1** and notify the SOC Manager immediately if:

- More than 50 employees received the phishing email
- Any executive (VP and above) clicked a malicious link
- The email contains a malware payload that executed (pivot to [Malware Runbook SOC-RB-002](02-runbook-malware.md))
- Evidence of Business Email Compromise (BEC) or wire fraud attempt
- The phishing campaign is part of a targeted attack against Meridian

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) for the full escalation matrix and CISO notification criteria.

## 9. Post-Incident Actions

1. Update the ServiceNow ticket with:
   - Full timeline of events
   - List of all IOCs identified
   - Count of affected users
   - Containment actions taken
2. Submit IOCs to the threat intelligence team for feed inclusion.
3. If the incident was P2 or higher, schedule a Post-Incident Review.

> **See:** [Post-Incident Review Template (SOC-PIR-010)](10-post-incident-review-example.md) for the PIR format and scheduling process.

4. Update Proofpoint rules and Splunk correlation rules if a detection gap was identified.

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md) for the change management workflow.

## 10. Common Phishing Indicators

| Indicator | Example |
|-----------|---------|
| Lookalike domain | `merid1anbank.com`, `meridian-bank-secure.com` |
| Urgency language | "Your account will be locked in 24 hours" |
| Mismatched reply-to | From: support@meridianbank.com, Reply-To: support@gmail.com |
| Suspicious attachment | `.html`, `.iso`, `.one`, `.zip` with password |
| URL shortener | `bit.ly`, `tinyurl.com` in corporate email |
| Display name spoofing | "James Kowalski" <random@external-domain.com> |

## 11. Metrics and Reporting

Track the following metrics monthly in the SOC dashboard:

- Total phishing emails reported by users
- Total phishing emails caught by Proofpoint (pre-delivery)
- Mean time to contain (MTTC) for phishing incidents
- Click-through rate on phishing simulations
- Repeat clickers by department

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact Sarah Mitchell (sarah.mitchell@meridianbank.com) or post in Slack #soc-general.*
