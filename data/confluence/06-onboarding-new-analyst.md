# SOC Analyst Onboarding: First-Week Checklist and Training Plan

| Field          | Value                                            |
|----------------|--------------------------------------------------|
| **Document ID**   | SOC-OB-006                                    |
| **Title**         | New Analyst Onboarding Guide                  |
| **Author**        | Sarah Mitchell                                 |
| **Last Updated**  | 2025-10-15                                     |
| **Status**        | Active                                         |
| **Review Cycle**  | Semi-Annual                                    |
| **Classification**| Internal — Meridian National Bank               |

---

## 1. Purpose

This document provides a structured onboarding plan for new analysts joining the Meridian Cyber Defense Center (CDC). It covers access provisioning, tool setup, mandatory training, and the shadow shift schedule for the first two weeks.

## 2. Before Day One — Manager Preparation

The SOC Manager or designated onboarding buddy should complete the following before the new analyst's start date:

- [ ] Submit ServiceNow access requests (see Section 4 below)
- [ ] Assign an onboarding buddy (Tier 2 analyst)
- [ ] Schedule shadow shifts for weeks 1-2
- [ ] Add the new analyst to Slack channels
- [ ] Prepare workstation with required software
- [ ] Schedule introductory meetings with key team members

## 3. Day One Checklist

| Time | Activity | Owner |
|------|----------|-------|
| 09:00 | Welcome meeting with SOC Manager (David Chen) | Manager |
| 09:30 | HR onboarding and badge activation | HR |
| 10:00 | Workstation setup and VPN configuration | IT Support |
| 10:30 | Slack channel overview and introductions | Buddy |
| 11:00 | Tour of the SOC floor and physical security briefing | Buddy |
| 11:30 | Overview of Meridian's business and banking operations | Manager |
| 12:00 | Lunch with team | Team |
| 13:00 | Tool access verification (see Section 4) | Buddy |
| 14:00 | Splunk orientation — navigating the interface | Buddy |
| 15:00 | CrowdStrike Falcon orientation — reading detections | Buddy |
| 16:00 | Review SOC documentation structure on Confluence | Buddy |
| 16:30 | End-of-day check-in with buddy | Buddy |

## 4. Access Provisioning

Submit the following ServiceNow requests on the new analyst's first day (or ideally 3 business days before start date):

| System | Access Level | ServiceNow Category | Approver |
|--------|-------------|---------------------|----------|
| Splunk | `soc-analyst` role | `Access > Splunk` | SOC Manager |
| CrowdStrike Falcon | `Falcon Analyst` | `Access > CrowdStrike` | SOC Manager |
| Proofpoint TAP | Read-only | `Access > Email Security` | SOC Manager |
| ServiceNow (ITSM) | `soc-ticket-create` | `Access > ServiceNow` | SOC Manager |
| Palo Alto Panorama | Read-only | `Access > Network Security` | Network Security Lead |
| AWS Console | `SOC-ReadOnly` role | `Access > AWS` | Cloud Security (Lisa Tran) |
| PagerDuty | Team member | `Access > PagerDuty` | SOC Manager |
| CyberArk | `SOC-SharedCredentials` safe | `Access > CyberArk` | SOC Manager |
| VirusTotal Enterprise | Shared API access | Shared via CyberArk | N/A |
| Microsoft 365 Admin | `Security Reader` | `Access > M365` | SOC Manager |

### 4.1 Slack Channels to Join

| Channel | Purpose |
|---------|---------|
| `#soc-general` | General SOC discussion and announcements |
| `#soc-alerts` | Automated alert notifications from Splunk/PagerDuty |
| `#soc-incidents` | Active incident coordination (P1/P2) |
| `#soc-training` | Training resources and discussion |
| `#soc-cloud-security` | AWS and Azure security discussions |
| `#security-help` | End-user security questions and reports |
| `#iam-ops` | Identity and access management team |
| `#threat-intel` | Threat intelligence sharing |

## 5. Required Reading — First Week

New analysts must read and acknowledge the following documents during their first week. Check off each document as you complete it:

### 5.1 Core Runbooks

- [ ] [Phishing Email Incident Response Runbook (SOC-RB-001)](01-runbook-phishing.md)
- [ ] [Malware Detection and Containment Runbook (SOC-RB-002)](02-runbook-malware.md)

### 5.2 Processes and Procedures

- [ ] [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md) — **Critical: memorize severity definitions and SLAs**
- [ ] [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md)

### 5.3 Tool Guides

- [ ] [Splunk Query Reference (SOC-TG-004)](04-tool-guide-splunk.md)
- [ ] [AWS Security Tooling Guide (SOC-TG-005)](05-tool-guide-aws-security.md)

### 5.4 Reference Materials

- [ ] [Knowledge Base: False Positives (SOC-KB-008)](08-knowledge-base-false-positives.md)
- [ ] [Team Roles and On-Call (SOC-TEAM-009)](09-team-roles-oncall.md)
- [ ] [Post-Incident Review Example (SOC-PIR-010)](10-post-incident-review-example.md)

> **Tip:** Don't try to memorize everything. Focus on understanding the escalation procedure and knowing where to find information quickly. You'll build muscle memory through shadow shifts.

## 6. Training Modules

### 6.1 Week 1 — Foundations

| Day | Module | Format | Duration | Instructor |
|-----|--------|--------|----------|------------|
| Mon | SOC Overview and Mission | Presentation | 1 hour | David Chen |
| Mon | Splunk Basics | Hands-on lab | 2 hours | Mike O'Brien |
| Tue | Incident Triage Fundamentals | Presentation + exercise | 2 hours | Sarah Mitchell |
| Tue | CrowdStrike Falcon Navigation | Hands-on lab | 2 hours | Raj Patel |
| Wed | Phishing Investigation Walkthrough | Shadowed exercise | 3 hours | Buddy |
| Thu | Malware Alert Triage Walkthrough | Shadowed exercise | 3 hours | Buddy |
| Fri | Network Fundamentals for SOC | Presentation | 2 hours | Network Security |

### 6.2 Week 2 — Applied Skills

| Day | Module | Format | Duration | Instructor |
|-----|--------|--------|----------|------------|
| Mon | Splunk Advanced Queries | Hands-on lab | 3 hours | Mike O'Brien |
| Tue | Email Security Deep Dive (Proofpoint) | Hands-on lab | 2 hours | Sarah Mitchell |
| Wed | AWS Security Basics | Hands-on lab | 2 hours | Lisa Tran |
| Thu | Threat Intelligence and IOC Analysis | Presentation + lab | 3 hours | Raj Patel |
| Fri | Practice Scenarios (CTF-style exercises) | Hands-on | Full day | Team |

### 6.3 External Training (Complete within first 90 days)

| Course | Platform | Priority |
|--------|----------|----------|
| Splunk Fundamentals 1 | Splunk Education | Required |
| CrowdStrike Falcon for Analysts | CrowdStrike University | Required |
| SANS SEC401: Security Essentials | SANS OnDemand | Recommended |
| AWS Security Fundamentals | AWS Skill Builder | Required (if cloud rotation) |
| MITRE ATT&CK Framework | MITRE training | Recommended |

## 7. Shadow Shift Schedule

During weeks 1-2, new analysts observe and assist experienced analysts during live shifts. The goal is to build confidence with tools and processes before handling alerts independently.

### 7.1 Shadow Shift Rules

1. The new analyst observes the buddy handling live alerts
2. The buddy explains their thought process for each triage decision
3. By day 3, the new analyst should attempt triage with the buddy observing
4. The new analyst should not make containment decisions independently during shadow period
5. Questions are encouraged — there are no bad questions in the SOC

### 7.2 Shadow Shift Progression

| Week | Activity | Independence Level |
|------|----------|-------------------|
| Week 1 | Observe buddy handling alerts | Observer only |
| Week 2 | Triage alerts with buddy oversight | Guided |
| Week 3 | Handle P4/P3 alerts independently, P2+ with backup | Semi-independent |
| Week 4 | Full shift with on-call buddy available | Independent with safety net |
| Week 5+ | Standard analyst rotation | Independent |

## 8. Key Contacts

| Role | Name | Reach Out For |
|------|------|---------------|
| SOC Manager | David Chen | Career questions, team concerns, access issues |
| Lead Analyst | Sarah Mitchell | Triage questions, process clarification |
| Tier 3 / Threat Hunt | Raj Patel | Complex investigations, malware analysis |
| Cloud Security | Lisa Tran | AWS/Azure questions |
| Detection Engineering | Mike O'Brien | Splunk queries, rule tuning |
| Your Onboarding Buddy | (Assigned by manager) | Everything — your first point of contact |

> **See:** [Team Roles and On-Call (SOC-TEAM-009)](09-team-roles-oncall.md) for the complete team directory and on-call rotation.

## 9. 30/60/90 Day Milestones

### 30 Days
- [ ] Complete all required reading
- [ ] Pass Splunk Fundamentals 1 assessment
- [ ] Handle P4 alerts independently
- [ ] Participate in at least one tabletop exercise

### 60 Days
- [ ] Handle P3 alerts independently
- [ ] Complete CrowdStrike Falcon certification
- [ ] Participate in on-call rotation (with senior backup)
- [ ] Contribute to at least one Post-Incident Review

### 90 Days
- [ ] Handle P2 alerts with minimal oversight
- [ ] Complete AWS Security Fundamentals (if applicable)
- [ ] Join the on-call rotation independently
- [ ] Present a "lessons learned" to the team from a notable investigation

## 10. Frequently Asked Questions

**Q: What do I do if I'm unsure about an alert?**
A: Ask your buddy or the shift lead. Escalating uncertainty is always better than closing a real alert as a false positive. Use the escalation procedure severity definitions to guide your decision.

**Q: Can I make changes to Splunk dashboards or alerts?**
A: Not during your first 90 days. Propose changes to Mike O'Brien via the detection rule change process.

> **See:** [Detection Rule Change Process (SOC-PROC-007)](07-process-detection-rule-changes.md)

**Q: How do I handle a P1 incident?**
A: Immediately notify the shift lead and SOC Manager. Do not attempt to contain a P1 alone during your first 90 days.

> **See:** [Escalation Procedure (SOC-PROC-003)](03-escalation-procedure.md)

**Q: Where do I find the on-call schedule?**
A: PagerDuty is the source of truth, but the schedule is also documented in the team roles page.

> **See:** [Team Roles and On-Call (SOC-TEAM-009)](09-team-roles-oncall.md)

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact Sarah Mitchell (sarah.mitchell@meridianbank.com) or post in Slack #soc-training.*
