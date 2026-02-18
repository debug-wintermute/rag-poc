# SOC Team Structure, Roles, Responsibilities, and On-Call Rotation

| Field          | Value                                              |
|----------------|----------------------------------------------------|
| **Document ID**   | SOC-TEAM-009                                    |
| **Title**         | Team Roles and On-Call Rotation                 |
| **Author**        | David Chen                                       |
| **Last Updated**  | 2025-12-01                                       |
| **Status**        | Active                                           |
| **Review Cycle**  | Quarterly                                        |
| **Classification**| Internal — Meridian National Bank                 |

---

## 1. Purpose

This document describes the organizational structure, roles, and responsibilities of the Meridian Cyber Defense Center (CDC), including the on-call rotation schedule, shift handoff procedures, and escalation contacts. It serves as the authoritative reference for team operations.

## 2. Organization Chart

```
                    James Kowalski
                        CISO
                          |
                    David Chen
                    SOC Manager
                          |
        ┌─────────────────┼─────────────────┐
        │                 │                 │
  Sarah Mitchell     Raj Patel        Lisa Tran
  Lead Analyst     Tier 3 / Hunt    Cloud Security
   (Shift Lead)                      Engineer
        │
  ┌─────┼─────────┐
  │     │         │
 T1    T1        T1
Analysts  Analysts  Analysts
(Day)   (Swing)  (Night)
```

**Detection Engineering** (Mike O'Brien) reports to David Chen and works closely with all tiers.

## 3. Team Roster

| Name | Role | Tier | Shift | Start Date | Certifications |
|------|------|------|-------|------------|---------------|
| David Chen | SOC Manager | Management | Business hours | 2019-03-15 | CISSP, CISM, GSOM |
| Sarah Mitchell | Lead Analyst / Shift Lead | Tier 2 | Day (08:00-16:00) | 2020-06-01 | GCIH, GCIA, CEH |
| Raj Patel | Threat Hunter / Incident Lead | Tier 3 | Day (08:00-16:00) | 2018-11-01 | GCFA, GREM, OSCP |
| Lisa Tran | Cloud Security Engineer | Tier 3 | Day (08:00-16:00) | 2021-01-15 | AWS Security Specialty, CCSP |
| Mike O'Brien | Detection Engineer | Tier 2 | Day (08:00-16:00) | 2020-09-01 | Splunk Certified Admin, GCIA |
| Priya Sharma | SOC Analyst | Tier 1 | Day (08:00-16:00) | 2024-02-01 | Security+, CySA+ |
| James Forsythe | SOC Analyst | Tier 1 | Day (08:00-16:00) | 2024-08-15 | Security+, Splunk Core User |
| Anika Washington | SOC Analyst | Tier 2 | Swing (16:00-00:00) | 2022-05-01 | GCIH, CEH |
| Carlos Mendez | SOC Analyst | Tier 1 | Swing (16:00-00:00) | 2023-11-01 | Security+, CySA+ |
| Emily Zheng | SOC Analyst | Tier 1 | Night (00:00-08:00) | 2023-06-15 | Security+, AWS Cloud Practitioner |
| Tomás Rivera | SOC Analyst | Tier 1 | Night (00:00-08:00) | 2024-04-01 | Security+ |

## 4. Role Definitions

### 4.1 Tier 1 — SOC Analyst

**Primary responsibility:** First-line alert triage and initial investigation.

| Responsibility | Details |
|---------------|---------|
| Alert triage | Monitor Splunk dashboards and `#soc-alerts`, triage incoming alerts |
| Initial investigation | Perform basic IOC lookups, check false positive knowledge base |
| Ticket creation | Create ServiceNow tickets for all confirmed or suspected incidents |
| Escalation | Escalate P3+ to Tier 2 within SLA timelines |
| Documentation | Document investigation steps and findings in tickets |
| Shift handoff | Complete handoff report at end of shift |

**Tier 1 analysts should NOT:**
- Contain hosts or disable accounts without Tier 2 approval
- Modify detection rules or Splunk searches
- Contact external parties (law enforcement, vendors, customers)
- Handle P1 incidents without Tier 2/3 supervision

### 4.2 Tier 2 — Senior Analyst / Shift Lead

**Primary responsibility:** Deep investigation, containment decisions, and shift leadership.

| Responsibility | Details |
|---------------|---------|
| Investigation | Conduct in-depth analysis of escalated incidents |
| Containment | Authorize and execute containment actions (host isolation, account disable) |
| Mentorship | Guide Tier 1 analysts on triage decisions |
| Shift management | Oversee shift operations, manage workload distribution |
| Escalation | Escalate P1/P2 to SOC Manager and Tier 3 |
| Reporting | Prepare shift summary reports |
| Rule review | Peer review detection rule changes |

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md) for the peer review workflow.

### 4.3 Tier 3 — Threat Hunter / Incident Lead

**Primary responsibility:** Advanced threat hunting, leading complex investigations, and malware analysis.

| Responsibility | Details |
|---------------|---------|
| Threat hunting | Proactive hypothesis-driven hunting across telemetry |
| Incident lead | Lead P1/P2 incident response as Incident Commander |
| Malware analysis | Reverse engineer malware samples when needed |
| Forensics | Conduct host and network forensics |
| Threat intel | Consume and produce actionable threat intelligence |
| Training | Develop and deliver training for Tier 1/2 analysts |

### 4.4 Cloud Security Engineer

**Primary responsibility:** AWS and Azure security monitoring, cloud incident response.

| Responsibility | Details |
|---------------|---------|
| Cloud monitoring | Triage GuardDuty, Security Hub, and Macie findings |
| Cloud IR | Lead containment and investigation for cloud incidents |
| IAM review | Review and respond to IAM anomaly alerts |
| Architecture | Advise on cloud security architecture and controls |
| Tooling | Maintain cloud security tooling and integrations |

> **See:** [Tool Guide: AWS Security (SOC-TG-005)](05-tool-guide-aws-security.md) for cloud-specific investigation procedures.

### 4.5 Detection Engineer

**Primary responsibility:** Build, tune, and maintain detection and correlation rules.

| Responsibility | Details |
|---------------|---------|
| Rule development | Create new detection rules based on threat intelligence and gaps |
| Rule tuning | Reduce false positives through systematic tuning |
| Splunk management | Maintain SOC Splunk app, dashboards, and saved searches |
| Metrics | Track and report on detection quality metrics |
| Integration | Build and maintain tool integrations (SOAR, enrichment) |
| Documentation | Maintain the rule catalog and false positive knowledge base |

> **See:** [Knowledge Base: False Positives (SOC-KB-008)](08-knowledge-base-false-positives.md) for the current false positive documentation.

### 4.6 SOC Manager

**Primary responsibility:** Team leadership, strategic planning, and executive reporting.

| Responsibility | Details |
|---------------|---------|
| Team management | Hiring, performance reviews, career development |
| Incident oversight | Final decision authority on incident severity and response |
| Executive reporting | Weekly CISO briefing, monthly board security metrics |
| Budget | Manage SOC tool and training budget |
| Process | Define and improve SOC processes and procedures |
| Vendor management | Manage relationships with security tool vendors |

## 5. Shift Schedule

### 5.1 Standard Shifts

| Shift | Hours (ET) | Days | Minimum Staffing |
|-------|-----------|------|-----------------|
| Day | 08:00 - 16:00 | Mon - Fri | 2 Tier 1 + 1 Tier 2 |
| Swing | 16:00 - 00:00 | Mon - Fri | 1 Tier 1 + 1 Tier 2 |
| Night | 00:00 - 08:00 | Mon - Fri | 1 Tier 1 (Tier 2 on-call) |
| Weekend Day | 08:00 - 20:00 | Sat - Sun | 1 Tier 1 (Tier 2 on-call) |
| Weekend Night | 20:00 - 08:00 | Sat - Sun | 1 Tier 1 (Tier 2 on-call) |

### 5.2 Shift Handoff Procedure

At the end of each shift, the outgoing analyst must:

1. Complete the **Shift Handoff Report** in ServiceNow:
   - Open incidents and their current status
   - Pending actions and follow-ups
   - Notable alerts that need continued monitoring
   - Any system issues (tool outages, degraded performance)

2. Post a summary in Slack `#soc-general`:

```
=== Shift Handoff: Day → Swing ===
Date: 2025-12-01
Outgoing: Sarah Mitchell, Priya Sharma
Incoming: Anika Washington, Carlos Mendez

Open Incidents:
- INC-2025-1142 (P2): Malware infection on WKST-FIN-042, host isolated, awaiting forensics
- INC-2025-1143 (P3): Phishing campaign targeting HR, 3 clicks, credentials reset

Pending Actions:
- INC-2025-1142: Raj to analyze malware sample tomorrow AM
- Check Proofpoint quarantine for additional phishing emails matching INC-2025-1143

System Status:
- All tools operational
- Splunk indexer cluster: green
```

3. Conduct a 15-minute verbal handoff with the incoming shift (in-person or via Teams).

## 6. On-Call Rotation

### 6.1 On-Call Schedule (Q1 2026)

The on-call rotation covers after-hours, weekends, and holidays. On-call analysts are reachable via PagerDuty.

| Week | Primary On-Call (Tier 2) | Secondary On-Call (Tier 3) |
|------|-------------------------|---------------------------|
| Jan 6-12 | Sarah Mitchell | Raj Patel |
| Jan 13-19 | Anika Washington | Lisa Tran |
| Jan 20-26 | Mike O'Brien | Raj Patel |
| Jan 27 - Feb 2 | Sarah Mitchell | Lisa Tran |
| Feb 3-9 | Anika Washington | Raj Patel |
| Feb 10-16 | Mike O'Brien | Lisa Tran |
| Feb 17-23 | Sarah Mitchell | Raj Patel |
| Feb 24 - Mar 2 | Anika Washington | Lisa Tran |
| Mar 3-9 | Mike O'Brien | Raj Patel |
| Mar 10-16 | Sarah Mitchell | Lisa Tran |
| Mar 17-23 | Anika Washington | Raj Patel |
| Mar 24-31 | Mike O'Brien | Lisa Tran |

### 6.2 On-Call Responsibilities

- Respond to PagerDuty pages within **15 minutes**
- Triage and handle P1/P2 alerts escalated by the on-shift analyst
- Be available for phone consultation for P3 alerts
- Ensure laptop and VPN access are available at all times
- Hand off any active incidents to the incoming on-call at rotation time (Monday 08:00 ET)

### 6.3 On-Call Compensation

- On-call premium: $500/week for primary, $300/week for secondary
- Incident response: 1.5x hourly rate for time spent actively responding
- Call-out minimum: 1 hour minimum for any after-hours page

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) — Section 3.4 for the after-hours escalation path.

## 7. PTO and Coverage Rules

1. **Minimum notice:** 2 weeks for planned PTO
2. **On-call swaps:** Must be arranged directly with another qualified analyst and documented in PagerDuty
3. **Minimum staffing:** At least one Tier 1 analyst must be present on every shift
4. **Holiday blackout:** No PTO approved for the SOC during the two weeks surrounding major banking operations periods (quarter-end, year-end)
5. **Emergency coverage:** SOC Manager will fill coverage gaps if no swap is possible
6. **Training PTO:** Up to 5 days/year for security conferences and training (separate from regular PTO)

## 8. Communication Escalation Matrix

| Urgency | Method | Expected Response |
|---------|--------|-------------------|
| Routine | Slack `#soc-general` | Within 4 hours |
| Urgent | Slack DM + mention | Within 30 minutes |
| Emergency | PagerDuty page | Within 15 minutes |
| Critical (P1) | PagerDuty + phone call | Within 5 minutes |

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) for the full incident escalation matrix.

## 9. Training and Development

### 9.1 Certification Path

| Current Level | Target Certifications | Timeline |
|--------------|----------------------|----------|
| Tier 1 (entry) | Security+, CySA+, Splunk Core User | First 6 months |
| Tier 1 (experienced) | GCIH, CEH, Splunk Certified Admin | 6-18 months |
| Tier 2 | GCIH, GCIA, one cloud cert | 1-3 years |
| Tier 3 | GCFA, GREM, OSCP | 2-5 years |

### 9.2 Training Budget

Each analyst receives $5,000/year for training and certifications. SANS courses may receive additional funding with SOC Manager approval.

> **See:** [Onboarding Guide (SOC-OB-006)](06-onboarding-new-analyst.md) for the new analyst training curriculum.

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact David Chen (david.chen@meridianbank.com).*
