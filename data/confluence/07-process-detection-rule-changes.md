# Process: Detection and Correlation Rule Change Management

| Field          | Value                                                    |
|----------------|----------------------------------------------------------|
| **Document ID**   | SOC-PROC-007                                          |
| **Title**         | Detection Rule Change Management Process              |
| **Author**        | Mike O'Brien                                           |
| **Last Updated**  | 2025-09-22                                             |
| **Status**        | Active                                                 |
| **Review Cycle**  | Annual                                                 |
| **Classification**| Internal — Meridian National Bank                       |

---

## 1. Purpose

This document defines the change management process for creating, modifying, disabling, or retiring detection and correlation rules in Meridian National Bank's security monitoring infrastructure. This includes Splunk correlation searches, CrowdStrike custom IOAs, Proofpoint email rules, and AWS GuardDuty custom threat lists.

All rule changes must follow this process to ensure proper review, testing, documentation, and rollback capability.

## 2. Scope

This process applies to:
- Splunk correlation searches and alerts (prefix: `SOC-CORR-*`)
- Splunk saved searches used for detection (prefix: `SOC-DET-*`)
- CrowdStrike Falcon custom Indicators of Attack (IOAs)
- CrowdStrike Falcon custom indicators (IOCs)
- Proofpoint email filtering rules and blocklists
- AWS GuardDuty custom threat lists and suppression rules
- Palo Alto IPS custom signatures and exception rules
- Any automated detection logic that generates SOC alerts

## 3. Roles and Responsibilities

| Role | Responsibility |
|------|---------------|
| **Requestor** (any SOC analyst) | Submit change request with justification |
| **Detection Engineer** (Mike O'Brien) | Review, implement, and test rule changes |
| **Peer Reviewer** (Tier 2+ analyst) | Review logic, assess impact, approve or request changes |
| **SOC Manager** (David Chen) | Final approval for high-risk changes, sign-off on rule retirement |
| **Splunk Admin** (Infrastructure team) | Deploy changes to production Splunk environment |

## 4. Change Categories

### 4.1 Standard Change (Low Risk)

Changes with minimal risk of disruption to SOC operations:
- Tuning an existing rule's threshold (e.g., adjusting failed login count from 5 to 10)
- Adding entries to an existing allowlist or blocklist
- Updating an IOC feed with new indicators
- Minor SPL syntax corrections

**Approval:** Peer Reviewer only
**Testing:** Verify in Splunk search (ad-hoc) before saving

### 4.2 Normal Change (Medium Risk)

Changes that may affect alert volume or detection coverage:
- Creating a new correlation rule
- Modifying the logic of an existing correlation rule
- Disabling a rule temporarily (>24 hours)
- Changing alert routing (e.g., adding PagerDuty notification)
- Adding or modifying a CrowdStrike custom IOA

**Approval:** Peer Reviewer + Detection Engineer
**Testing:** Run in staging Splunk instance for 24 hours minimum

### 4.3 Emergency Change (High Risk / Urgent)

Changes required to address an active incident or critical false positive:
- Creating a rule during an active P1/P2 incident
- Disabling a rule that is generating massive false positive volume
- Blocking a newly discovered threat via custom IOC

**Approval:** SOC Manager verbal approval (documented retroactively)
**Testing:** Deploy immediately, monitor for 4 hours, create follow-up ticket for formal review

### 4.4 Rule Retirement

Permanently disabling and removing a detection rule:
- Rule has been replaced by a more effective detection
- Rule generates false positives that cannot be tuned
- The threat the rule detects is no longer relevant

**Approval:** Detection Engineer + SOC Manager
**Documentation:** Update the rule catalog and document the retirement rationale

## 5. Change Request Process

### 5.1 Submit Request

Create a ServiceNow ticket with category `Security > Detection Engineering` and include:

```
=== Detection Rule Change Request ===

Requestor: [Your Name]
Date: [YYYY-MM-DD]
Change Category: [Standard / Normal / Emergency]

Rule ID: [e.g., SOC-CORR-AUTH-001, or "NEW" for new rules]
Rule Name: [Descriptive name]
Platform: [Splunk / CrowdStrike / Proofpoint / AWS / Palo Alto]

Change Description:
[Detailed description of the proposed change]

Justification:
[Why is this change needed? Reference ticket numbers, incident IDs, or false positive patterns]

MITRE ATT&CK Mapping:
  Tactic: [e.g., Initial Access]
  Technique: [e.g., T1566 - Phishing]
  Sub-technique: [e.g., T1566.001 - Spearphishing Attachment]

Expected Impact:
  - Alert volume change: [Increase / Decrease / No change]
  - Estimated daily alert count: [Number]
  - Detection coverage impact: [New coverage / Improved / Reduced]

Rollback Plan:
[How to revert this change if it causes problems]
```

### 5.2 Peer Review

The assigned peer reviewer must:

1. Verify the SPL query or detection logic is syntactically correct
2. Run the query against the last 7 days of data to assess volume
3. Check for overlap with existing rules (avoid duplicate detections)
4. Verify the MITRE ATT&CK mapping is accurate
5. Assess false positive potential based on known patterns

> **See:** [Knowledge Base: False Positives (SOC-KB-008)](08-knowledge-base-false-positives.md) for documented false positive patterns that should be considered during review.

6. Add review comments to the ServiceNow ticket
7. Approve, request changes, or escalate to SOC Manager

### 5.3 Testing

#### Splunk Rules

1. Deploy the rule to the **staging search head** (`splunk-sh-staging.meridian.internal`)
2. Run the search over historical data (minimum 7 days) and document:
   - Total alert count
   - Alert distribution by hour/day
   - Sample of triggered alerts (minimum 10)
   - True positive vs false positive assessment for sampled alerts
3. If the rule generates more than 50 alerts/day, discuss tuning with the Detection Engineer

#### CrowdStrike Custom IOAs

1. Test in the **Staging** prevention policy group first
2. Monitor for 48 hours in detect-only mode
3. Review all triggered detections before enabling prevention

#### Proofpoint Rules

1. Test using the Proofpoint **Policy Route** sandbox
2. Review matched emails for 24 hours before promoting to production

### 5.4 Deployment

1. Detection Engineer deploys the change to production
2. Set the rule to **alert-only** mode for the first 24 hours (no automated response)
3. Monitor alert volume and quality during the burn-in period
4. If satisfactory, enable full response actions (e.g., PagerDuty page, auto-containment)
5. Update the rule catalog spreadsheet: `SharePoint > SOC > Detection Rule Catalog.xlsx`

### 5.5 Post-Deployment Review

After 7 days in production:

1. Review alert volume and true/false positive ratio
2. Document tuning adjustments if needed
3. Close the ServiceNow change ticket with:
   - Final alert volume metrics
   - True positive rate
   - Any follow-up actions

## 6. Rule Naming Convention

All rules must follow this naming convention:

```
SOC-{TYPE}-{CATEGORY}-{NUMBER}: {Descriptive Name}
```

| Component | Values |
|-----------|--------|
| TYPE | `CORR` (correlation), `DET` (detection), `HUNT` (threat hunt) |
| CATEGORY | `AUTH` (authentication), `EMAIL` (email security), `MAL` (malware), `NET` (network), `CLOUD` (cloud), `IAM` (identity), `DLP` (data loss), `INSIDER` (insider threat) |
| NUMBER | Three-digit sequential number |

**Examples:**
- `SOC-CORR-AUTH-001: Brute Force — Failed Logins > 10 in 5 Minutes`
- `SOC-CORR-EMAIL-003: Phishing — Suspicious Attachment Delivered`
- `SOC-DET-MAL-001: EDR — CrowdStrike Critical Severity Alert`
- `SOC-HUNT-NET-002: Beaconing — Low Interval Variance Outbound`

## 7. Rule Documentation Requirements

Every active detection rule must have the following documented in the rule catalog:

| Field | Required | Description |
|-------|----------|-------------|
| Rule ID | Yes | Unique identifier per naming convention |
| Rule Name | Yes | Descriptive name |
| Platform | Yes | Splunk, CrowdStrike, etc. |
| MITRE ATT&CK | Yes | Tactic and technique mapping |
| SPL / Logic | Yes | The actual detection query or logic |
| Data Sources | Yes | Required sourcetypes and indexes |
| Threshold | Yes | Alert trigger conditions |
| Alert Routing | Yes | Where alerts are sent |
| Owner | Yes | Detection Engineer responsible |
| Created Date | Yes | When the rule was first deployed |
| Last Modified | Yes | When the rule was last changed |
| FP Rate | Yes | Estimated false positive rate (updated quarterly) |
| Runbook Reference | No | Link to investigation runbook |

## 8. Quarterly Rule Health Review

Every quarter, the Detection Engineering team conducts a review of all active rules:

1. Pull alert volume and TP/FP metrics for each rule from the last 90 days
2. Identify rules with >30% false positive rate for tuning
3. Identify rules with zero triggers for relevance assessment
4. Review MITRE ATT&CK coverage gaps
5. Prioritize new rule development based on threat landscape
6. Present findings to SOC Manager for prioritization

> **See:** [Tool Guide: Splunk (SOC-TG-004)](04-tool-guide-splunk.md) for queries used to pull rule health metrics.

## 9. Emergency Rule Disable Procedure

If a rule is causing operational disruption (e.g., generating thousands of false positives):

1. **Immediately** disable the rule in the relevant platform
2. Notify the SOC Manager and Detection Engineer via Slack `#soc-general`
3. Document the disable action in ServiceNow with:
   - Rule ID
   - Reason for emergency disable
   - Approximate alert volume before disable
   - Time of disable
4. Create a follow-up ticket for rule tuning or retirement
5. The rule must be reviewed within 5 business days before re-enabling

---

*Document maintained by the Meridian Cyber Defense Center. For questions, contact Mike O'Brien (mike.obrien@meridianbank.com) or post in Slack #soc-general.*
