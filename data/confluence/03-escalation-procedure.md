# Escalation Procedure: Severity Classification and Notification Matrix

| Field          | Value                                             |
|----------------|---------------------------------------------------|
| **Document ID**   | SOC-PROC-003                                   |
| **Title**         | Severity Classification and Escalation Matrix  |
| **Author**        | David Chen                                     |
| **Last Updated**  | 2025-12-02                                     |
| **Status**        | Active                                         |
| **Review Cycle**  | Semi-Annual                                    |
| **Classification**| Internal — Meridian National Bank               |

---

## 1. Purpose

This document defines the severity classification system for security incidents at Meridian National Bank and establishes the escalation matrix including notification requirements, SLA targets, and regulatory reporting obligations. All SOC analysts must follow this procedure for every security incident.

## 2. Severity Definitions

### P1 — Critical

**Definition:** An active security incident that poses an immediate threat to Meridian National Bank's operations, customer data, financial assets, or regulatory standing.

**Examples:**
- Confirmed ransomware execution on any system
- Active data exfiltration of customer PII or financial data
- Compromise of SWIFT messaging system or core banking platform (FIS Horizon)
- Business Email Compromise (BEC) with confirmed fraudulent wire transfer
- Active intrusion by a known APT group
- DDoS attack impacting customer-facing banking services

**SLA:**
| Metric | Target |
|--------|--------|
| Time to Acknowledge | 5 minutes |
| Time to Respond | 15 minutes |
| Time to Contain | 1 hour |
| Status Updates | Every 30 minutes |
| Post-Incident Review | Required within 3 business days |

### P2 — High

**Definition:** A confirmed security incident with significant potential impact that requires urgent investigation and containment but is not yet causing active harm.

**Examples:**
- Malware infection on multiple endpoints (>5) without confirmed lateral movement
- Compromised privileged account (admin, service account)
- Spear-phishing campaign targeting executive team or finance department
- Unauthorized access to production database containing customer data
- Critical vulnerability exploitation detected (CVSS 9.0+)
- Suspicious insider threat activity

**SLA:**
| Metric | Target |
|--------|--------|
| Time to Acknowledge | 10 minutes |
| Time to Respond | 30 minutes |
| Time to Contain | 4 hours |
| Status Updates | Every 1 hour |
| Post-Incident Review | Required within 5 business days |

### P3 — Medium

**Definition:** A security event requiring investigation that may indicate malicious activity but has limited scope or impact.

**Examples:**
- Single endpoint malware infection (commodity malware, contained by EDR)
- Phishing email with credential harvesting link, fewer than 5 user clicks
- Brute force attack against VPN gateway (no successful authentication)
- Policy violation detected (unauthorized software installation)
- AWS GuardDuty finding of medium severity
- Single account lockout with suspicious source IP

**SLA:**
| Metric | Target |
|--------|--------|
| Time to Acknowledge | 30 minutes |
| Time to Respond | 2 hours |
| Time to Contain | 8 hours |
| Status Updates | Every 4 hours |
| Post-Incident Review | Optional (Manager discretion) |

### P4 — Low

**Definition:** A security event that requires documentation and may require minor follow-up but poses minimal immediate risk.

**Examples:**
- Blocked phishing email (no delivery to user mailbox)
- Blocked malware attempt (quarantined by endpoint protection)
- Failed authentication attempts from known scanner IPs
- Routine vulnerability scan findings
- Information request from external party (law enforcement, other bank)
- Security awareness training follow-up (user clicked simulated phish)

**SLA:**
| Metric | Target |
|--------|--------|
| Time to Acknowledge | 4 hours |
| Time to Respond | 8 hours |
| Time to Contain | N/A |
| Status Updates | Daily |
| Post-Incident Review | Not required |

## 3. Escalation Matrix

### 3.1 Internal Escalation Path

```
Tier 1 Analyst
    ↓ (if P3 or above, or if unsure)
Tier 2 Analyst / Shift Lead
    ↓ (if P2 or above)
SOC Manager (David Chen)
    ↓ (if P1)
CISO (James Kowalski)
    ↓ (if regulatory reporting required or customer impact)
Executive Crisis Team
```

### 3.2 Notification Requirements by Severity

| Role | P1 | P2 | P3 | P4 |
|------|----|----|----|----|
| Tier 1 Analyst | Investigate | Investigate | Investigate | Investigate |
| Tier 2 / Shift Lead | Notify immediately | Notify immediately | Notify within 1 hour | Daily summary |
| SOC Manager (David Chen) | Notify immediately (phone) | Notify within 15 min | Notify in shift report | Weekly summary |
| CISO (James Kowalski) | Notify within 30 min (phone) | Notify within 1 hour (email) | Not required | Not required |
| CTO / COO | Notify within 1 hour (P1 only) | Not required | Not required | Not required |
| Legal & Compliance | Notify within 2 hours (P1 only) | Case-by-case | Not required | Not required |
| Board of Directors | Notify within 24 hours if data breach | Not required | Not required | Not required |

### 3.3 Contact Directory

| Role | Name | Phone | Email | Slack |
|------|------|-------|-------|-------|
| SOC Manager | David Chen | +1 (555) 801-2200 | david.chen@meridianbank.com | @david.chen |
| Lead Analyst | Sarah Mitchell | +1 (555) 801-2201 | sarah.mitchell@meridianbank.com | @sarah.mitchell |
| Tier 3 / Threat Hunt | Raj Patel | +1 (555) 801-2202 | raj.patel@meridianbank.com | @raj.patel |
| Cloud Security | Lisa Tran | +1 (555) 801-2203 | lisa.tran@meridianbank.com | @lisa.tran |
| Detection Engineering | Mike O'Brien | +1 (555) 801-2204 | mike.obrien@meridianbank.com | @mike.obrien |
| CISO | James Kowalski | +1 (555) 801-2100 | james.kowalski@meridianbank.com | @james.kowalski |

> **See:** [Team Roles and On-Call (SOC-TEAM-009)](09-team-roles-oncall.md) for the full on-call rotation schedule and after-hours contact procedures.

### 3.4 After-Hours Escalation

- **Normal business hours (08:00 - 18:00 ET):** Follow the matrix above.
- **After hours, weekends, holidays:**
  1. Page the on-call Tier 2 analyst via PagerDuty
  2. If no response within 10 minutes, page the on-call SOC Manager
  3. For P1 incidents, **always** page both the on-call analyst and SOC Manager simultaneously
  4. The CISO can be reached via the emergency line: +1 (555) 801-9999

## 4. Regulatory Reporting Requirements

As a federally chartered bank, Meridian National Bank has specific regulatory reporting obligations for security incidents.

### 4.1 OCC Notification (12 CFR 30, Appendix B)

A Suspicious Activity Report (SAR) must be filed with the OCC within **36 hours** if:
- The incident involves actual or attempted unauthorized access to customer information
- The incident results in actual or potential misuse of customer information
- The incident affects the bank's ability to deliver services

### 4.2 FinCEN SAR Filing

File a SAR with FinCEN within **30 days** if:
- The incident involves or is related to money laundering
- The incident involves fraud exceeding $5,000
- The incident involves insider threat or employee misconduct

### 4.3 State Data Breach Notification

If customer PII is confirmed compromised:
- Notification must be sent to affected customers within **60 days** (varies by state)
- State Attorney General notifications required in many jurisdictions
- Legal & Compliance team manages this process — SOC provides the technical details

### 4.4 Federal Reserve and FDIC

- Report significant cybersecurity incidents to the Federal Reserve within **36 hours**
- Computer-security incident notification rule (effective April 2022) requires notification for incidents that could materially affect banking operations, ability to deliver services, or financial stability

## 5. CISO Notification Criteria

The CISO must be notified for any incident meeting one or more of these criteria:

1. Any P1 incident
2. Any incident involving customer data (PII, financial data)
3. Any incident involving SWIFT, core banking, or payment processing systems
4. Any incident that may require regulatory notification
5. Any incident generating media attention or customer complaints
6. Any incident involving a known APT group or nation-state actor
7. Any incident requiring engagement of external forensics firm
8. Any insider threat investigation

## 6. External Resources

### 6.1 Approved External Forensics Firms

| Firm | Contract # | Contact | Specialty |
|------|-----------|---------|-----------|
| Mandiant | MERI-IR-2024-01 | ir-hotline@mandiant.com | APT, nation-state |
| CrowdStrike Services | MERI-IR-2024-02 | services@crowdstrike.com | Endpoint forensics |
| Stroz Friedberg | MERI-IR-2024-03 | hotline@strozfriedberg.com | Insider threat, legal |

### 6.2 Law Enforcement Contacts

| Agency | Contact | When to Engage |
|--------|---------|----------------|
| FBI Cyber Division (Newark field office) | cyber.newark@fbi.gov / (555) 700-1000 | Nation-state, major fraud, ransomware > $100K |
| US Secret Service (ECTF) | ectf.newark@usss.dhs.gov | Financial fraud, BEC |
| IC3 (Internet Crime Complaint Center) | ic3.gov | All cyber incidents for reporting |

> **Note:** All law enforcement engagement must be coordinated through Legal & Compliance. SOC analysts should never contact law enforcement directly without prior approval.

## 7. Incident Severity Reclassification

Severity can be upgraded or downgraded during an investigation:

- **Upgrade:** Any analyst can upgrade severity. Notify the Tier 2 lead and SOC Manager of the upgrade.
- **Downgrade:** Only Tier 2 and above can downgrade severity. Document the rationale in the ServiceNow ticket.
- **Example:** A P3 phishing incident is upgraded to P1 when investigation reveals credential compromise and lateral movement.

## 8. Communication Channels

| Channel | Purpose |
|---------|---------|
| Slack `#soc-alerts` | Automated alert notifications |
| Slack `#soc-general` | General SOC discussion |
| Slack `#soc-incidents` | Active incident coordination (P1/P2 only) |
| PagerDuty | On-call escalation and after-hours paging |
| Bridge call: +1 (555) 801-8000 | P1 incident war room (auto-provisioned) |
| ServiceNow | Incident tracking and documentation |

> **See:** [Phishing Runbook (SOC-RB-001)](01-runbook-phishing.md) and [Malware Runbook (SOC-RB-002)](02-runbook-malware.md) for incident-specific escalation triggers.

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact David Chen (david.chen@meridianbank.com).*
