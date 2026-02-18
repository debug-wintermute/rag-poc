# Post-Incident Review: PIR Template and Example

| Field          | Value                                                |
|----------------|------------------------------------------------------|
| **Document ID**   | SOC-PIR-010                                       |
| **Title**         | Post-Incident Review Template with Example        |
| **Author**        | David Chen                                         |
| **Last Updated**  | 2025-11-30                                         |
| **Status**        | Active                                             |
| **Review Cycle**  | Annual                                             |
| **Classification**| Internal — Meridian National Bank                   |

---

## 1. Purpose

This document provides the standard Post-Incident Review (PIR) template used by the Meridian Cyber Defense Center and includes a completed example for reference. PIRs are required for all P1 incidents and P2 incidents at the SOC Manager's discretion.

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) — Section 2 for severity definitions that determine PIR requirements.

## 2. PIR Process

### 2.1 Scheduling

- **P1 incidents:** PIR must be scheduled within 3 business days of incident closure
- **P2 incidents:** PIR must be scheduled within 5 business days of incident closure
- PIR meetings are 60-90 minutes and include all analysts involved in the incident
- The SOC Manager or Incident Lead facilitates the meeting
- Meeting notes are documented in the PIR template below and stored in Confluence

### 2.2 Attendees

| Role | Required | Optional |
|------|----------|----------|
| Incident Lead | Yes | — |
| All responding analysts | Yes | — |
| SOC Manager | Yes | — |
| Detection Engineer | Yes | — |
| CISO | — | P1 only |
| Affected system owners | — | As needed |
| Legal & Compliance | — | If regulatory reporting involved |

### 2.3 Ground Rules

- **Blameless culture:** Focus on systems and processes, not individuals
- **Timeline-driven:** Walk through events chronologically
- **Action-oriented:** Every finding must have a concrete action item with an owner
- **Documented:** All discussions captured in writing, not just verbal

---

## 3. PIR Template

```
===============================================================
POST-INCIDENT REVIEW
===============================================================

PIR ID:           PIR-YYYY-NNN
Incident ID:      INC-YYYY-NNNNN
Incident Title:   [Brief description]
Severity:         [P1 / P2]
PIR Date:         [YYYY-MM-DD]
Facilitator:      [Name]
Scribe:           [Name]

---------------------------------------------------------------
INCIDENT SUMMARY
---------------------------------------------------------------
[2-3 paragraph summary of what happened, impact, and resolution]

---------------------------------------------------------------
TIMELINE
---------------------------------------------------------------
| Time (ET)  | Event                              | Source     |
|------------|-------------------------------------|------------|
| YYYY-MM-DD HH:MM | [Event description]         | [Tool/Log] |

---------------------------------------------------------------
ROOT CAUSE ANALYSIS
---------------------------------------------------------------
[Analysis of the root cause, contributing factors]

---------------------------------------------------------------
WHAT WENT WELL
---------------------------------------------------------------
- [Item 1]
- [Item 2]

---------------------------------------------------------------
WHAT COULD BE IMPROVED
---------------------------------------------------------------
- [Item 1]
- [Item 2]

---------------------------------------------------------------
DETECTION GAP ANALYSIS
---------------------------------------------------------------
[Were there detection gaps? What was missed?]

---------------------------------------------------------------
ACTION ITEMS
---------------------------------------------------------------
| # | Action | Owner | Priority | Due Date | Status |
|---|--------|-------|----------|----------|--------|

---------------------------------------------------------------
METRICS
---------------------------------------------------------------
Time to Detect (TTD):    [Duration]
Time to Respond (TTR):   [Duration]
Time to Contain (TTC):   [Duration]
Time to Remediate:       [Duration]
Total Incident Duration: [Duration]
---------------------------------------------------------------
```

---

## 4. Example PIR: QakBot Malware via Phishing Campaign

```
===============================================================
POST-INCIDENT REVIEW
===============================================================

PIR ID:           PIR-2025-042
Incident ID:      INC-2025-01087
Incident Title:   QakBot Malware Delivery via Targeted Phishing
Severity:         P1
PIR Date:         2025-10-18
Facilitator:      David Chen
Scribe:           Sarah Mitchell
```

### 4.1 Incident Summary

On October 14, 2025, Meridian National Bank was targeted by a phishing campaign delivering QakBot malware via password-protected ZIP attachments. The campaign specifically targeted the Finance and Treasury departments using compromised email accounts from a legitimate Meridian vendor (Whitfield & Associates, an external auditing firm).

Twelve employees received the phishing email. Three employees opened the attachment and executed the embedded JavaScript dropper, resulting in QakBot installation on their workstations. One of the infected workstations (WKST-FIN-015, belonging to Senior Accountant Rebecca Torres) was used to perform reconnaissance of the internal network, including enumeration of Active Directory and file share access.

The infection was detected 47 minutes after the first execution by CrowdStrike Falcon, which flagged the QakBot process injection behavior. The SOC contained all three infected hosts within 23 minutes of the initial CrowdStrike alert. No lateral movement beyond the initial three workstations was confirmed, and no data exfiltration was detected.

### 4.2 Timeline

| Time (ET) | Event | Source |
|-----------|-------|--------|
| 2025-10-14 09:12 | Phishing emails sent from compromised Whitfield & Associates account (j.whitfield@whitfieldassoc.com) | Proofpoint TAP |
| 2025-10-14 09:15 | Proofpoint delivers 12 emails (classified as "clean" due to trusted sender domain) | Proofpoint TAP |
| 2025-10-14 09:23 | Rebecca Torres (WKST-FIN-015) opens ZIP and executes JS dropper | CrowdStrike |
| 2025-10-14 09:28 | Michael Park (WKST-FIN-022) opens ZIP and executes JS dropper | CrowdStrike |
| 2025-10-14 09:41 | Jennifer Liu (WKST-TREAS-008) opens ZIP and executes JS dropper | CrowdStrike |
| 2025-10-14 09:45 | QakBot establishes C2 connection from WKST-FIN-015 to 185.234.72.19:443 | Palo Alto |
| 2025-10-14 09:52 | QakBot begins AD enumeration from WKST-FIN-015 (net group, nltest commands) | CrowdStrike |
| 2025-10-14 10:00 | **CrowdStrike alert: "ProcessInjection" on WKST-FIN-015 (Severity: Critical)** | CrowdStrike |
| 2025-10-14 10:02 | Alert appears in Splunk and `#soc-alerts` | Splunk |
| 2025-10-14 10:03 | Tier 1 analyst Priya Sharma begins triage | ServiceNow |
| 2025-10-14 10:07 | Priya escalates to Tier 2 (Sarah Mitchell) — identifies QakBot IOCs | ServiceNow |
| 2025-10-14 10:10 | Sarah elevates to P1 and notifies SOC Manager | PagerDuty |
| 2025-10-14 10:12 | Raj Patel joins as Incident Lead | Slack |
| 2025-10-14 10:15 | WKST-FIN-015 isolated via CrowdStrike | CrowdStrike |
| 2025-10-14 10:17 | Splunk search identifies WKST-FIN-022 and WKST-TREAS-008 as additional infected hosts | Splunk |
| 2025-10-14 10:20 | WKST-FIN-022 and WKST-TREAS-008 isolated via CrowdStrike | CrowdStrike |
| 2025-10-14 10:23 | **All three hosts contained** | CrowdStrike |
| 2025-10-14 10:25 | C2 IP (185.234.72.19) blocked at Palo Alto perimeter firewall | Palo Alto |
| 2025-10-14 10:30 | C2 domain (update-service-cdn[.]com) added to DNS sinkhole | Infoblox |
| 2025-10-14 10:35 | All three user accounts disabled and passwords reset | Active Directory |
| 2025-10-14 10:40 | Proofpoint quarantine search removes remaining unread copies of phishing email | Proofpoint |
| 2025-10-14 10:45 | David Chen notifies CISO James Kowalski | Email/Phone |
| 2025-10-14 11:00 | Sarah sends user notification to all 12 recipients | Email |
| 2025-10-14 11:30 | Raj begins forensic analysis on isolated hosts via CrowdStrike RTR | CrowdStrike |
| 2025-10-14 14:00 | Forensic analysis complete — no lateral movement confirmed, no data exfiltration | ServiceNow |
| 2025-10-14 15:00 | Vendor (Whitfield & Associates) notified of compromised email account | Email |
| 2025-10-15 09:00 | Three workstations reimaged and returned to users | Desktop Eng |
| 2025-10-15 11:00 | Incident closed as contained and remediated | ServiceNow |

### 4.3 Root Cause Analysis

**Primary cause:** Proofpoint TAP did not flag the phishing email because the sender domain (`whitfieldassoc.com`) was in Meridian's trusted sender list. The vendor's email account had been compromised via credential theft (confirmed by Whitfield's IT team on 10/15).

**Contributing factors:**
1. Trusted sender allowlist in Proofpoint bypasses URL and attachment sandboxing
2. Password-protected ZIP attachments cannot be scanned by email security tools
3. Three users executed the JavaScript dropper despite security awareness training
4. The phishing email used a legitimate ongoing audit engagement as context, making it highly convincing

### 4.4 What Went Well

- CrowdStrike Falcon detected the QakBot process injection within 47 minutes of initial execution
- Tier 1 analyst (Priya Sharma) correctly identified the IOCs as QakBot and escalated promptly
- All three infected hosts were contained within 23 minutes of the initial alert
- Forensic analysis confirmed no lateral movement or data exfiltration
- Cross-team communication via Slack `#soc-incidents` was effective
- Vendor notification was completed within 24 hours

### 4.5 What Could Be Improved

- **47-minute detection gap:** QakBot was active for 47 minutes before CrowdStrike flagged it. During this time, it established C2 and began reconnaissance.
- **Trusted sender bypass:** The Proofpoint trusted sender list bypasses critical security controls. This list has 247 entries and has not been reviewed since Q1 2025.
- **No alerting on password-protected ZIPs:** There is no correlation rule for password-protected ZIP attachments delivered to high-risk departments (Finance, Treasury).
- **User behavior:** Three out of twelve recipients executed the attachment (25% click rate), despite all three having completed security awareness training within the last 6 months.

### 4.6 Detection Gap Analysis

| Gap | Current State | Desired State | MITRE ATT&CK |
|-----|--------------|---------------|---------------|
| Trusted sender email scanning | Trusted senders bypass sandboxing | Sandbox all attachments regardless of sender reputation | T1566.001 |
| Password-protected attachment alerting | No alert for password-protected archives | Alert on password-protected archives to Finance/Treasury | T1566.001 |
| QakBot C2 domain detection | Relied on CrowdStrike behavioral detection | Add known QakBot C2 infrastructure to DNS threat feed | T1071.001 |
| AD enumeration alerting | No alert for `net group` / `nltest` from workstations | Alert on AD discovery commands from non-admin workstations | T1087.002 |

> **See:** [Phishing Runbook (SOC-RB-001)](01-runbook-phishing.md) and [Malware Runbook (SOC-RB-002)](02-runbook-malware.md) — Recommend updating both runbooks with QakBot-specific indicators.

### 4.7 Action Items

| # | Action | Owner | Priority | Due Date | Status |
|---|--------|-------|----------|----------|--------|
| 1 | Review and prune Proofpoint trusted sender list (247 entries) | Sarah Mitchell | High | 2025-11-01 | Complete |
| 2 | Create Splunk correlation rule for password-protected ZIP attachments to Finance/Treasury | Mike O'Brien | High | 2025-10-28 | Complete |
| 3 | Add QakBot C2 infrastructure to DNS threat feed | Raj Patel | High | 2025-10-21 | Complete |
| 4 | Create correlation rule for AD enumeration commands from non-admin workstations | Mike O'Brien | Medium | 2025-11-15 | Complete |
| 5 | Conduct targeted phishing simulation for Finance and Treasury departments | Sarah Mitchell | Medium | 2025-11-30 | In Progress |
| 6 | Evaluate Proofpoint policy to sandbox attachments from trusted senders | Mike O'Brien | High | 2025-11-15 | Complete |
| 7 | Request Whitfield & Associates provide their incident investigation report | David Chen | Medium | 2025-11-01 | Complete |
| 8 | Update phishing runbook with QakBot-specific IOCs and procedures | Sarah Mitchell | Low | 2025-12-01 | Pending |
| 9 | Brief the CISO on trusted sender risk and remediation plan | David Chen | High | 2025-10-21 | Complete |
| 10 | File SAR with FinCEN (precautionary — no confirmed financial impact) | Legal & Compliance | High | 2025-11-14 | Complete |

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md) — Action items 2, 3, 4, and 6 were implemented via the rule change process.

### 4.8 Metrics

| Metric | Value | SLA Target | Met? |
|--------|-------|------------|------|
| Time to Detect (TTD) | 47 minutes | 15 minutes | No |
| Time to Respond (TTR) | 50 minutes (first alert to triage) | 15 minutes | No |
| Time to Contain (TTC) | 23 minutes (from triage start) | 1 hour | Yes |
| Time to Remediate | 23 hours (reimage next day) | 24 hours | Yes |
| Total Incident Duration | 26 hours | — | — |

**Note:** TTD exceeded the P1 SLA because the initial infection was not detected by email security controls. The 47-minute gap represents the time between malware execution and CrowdStrike behavioral detection. TTR is measured from the CrowdStrike alert; from that point, the team responded within 3 minutes.

### 4.9 Lessons Learned

1. **Trusted sender lists create blind spots.** Vendor email compromise is increasingly common, and trusted sender lists effectively disable security controls for the most targeted attack vector.

2. **Password-protected archives remain a significant evasion technique.** Email security tools cannot inspect encrypted content. Behavioral detection (EDR) is the last line of defense.

3. **The team's containment speed was excellent.** Despite the detection gap, the SOC contained all three hosts within 23 minutes of the first alert, preventing any lateral movement or data exfiltration.

4. **Cross-functional response coordination worked well.** The escalation from Tier 1 → Tier 2 → Tier 3 → SOC Manager → CISO happened smoothly within the defined escalation procedure.

5. **Supply chain compromise is a growing risk.** Trusted vendors should be treated with the same skepticism as unknown senders for attachment and URL analysis.

---

## 5. PIR Follow-Up Process

After the PIR meeting:

1. The scribe publishes the completed PIR to Confluence within 2 business days
2. Action items are created as individual ServiceNow tickets and tracked to completion
3. The SOC Manager reviews action item status weekly until all items are closed
4. Detection rule changes follow the standard change management process

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md)

5. The PIR is referenced in the monthly CISO report for P1 incidents
6. Lessons learned are incorporated into the next security awareness training cycle

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact David Chen (david.chen@meridianbank.com).*
