# TECHNOLOGY WATCH REPORT
## Open-Source SIEM/XDR Adoption in Small and Medium Enterprises (SMEs)
### Focus: Wazuh — Trends and Outlook 2025-2026

---

**Document Reference**: NS-2026-005
**Author**: [Name] — Technical Lead, Consulting Mission
**Project Context**: Nova Syndicate IT Modernization
**Date**: May 2026
**Language**: English
**Format**: Technology Watch Report
**Length**: 3 pages

---

## EXECUTIVE SUMMARY

The Security Information and Event Management (SIEM) market is undergoing a profound transformation in 2025-2026, driven by three converging trends: the **convergence of SIEM and XDR (Extended Detection and Response)** capabilities, the **growing adoption of open-source alternatives** in cost-sensitive segments, and the **mainstreaming of AI-augmented threat detection**. Wazuh, an open-source unified XDR/SIEM platform, has emerged as one of the most adopted security platforms in SMEs and mid-market organizations.

This report examines Wazuh's positioning in this evolving landscape, with specific relevance to the Nova Syndicate infrastructure modernization project. It identifies why open-source SIEM is increasingly viable for SMEs, and outlines the strategic implications for organizations facing tight budgets but strong compliance requirements (such as Nova Syndicate operating in the medical, aerospace, and defense supply chains).

---

## 1. CONTEXT: THE SIEM MARKET LANDSCAPE IN 2025-2026

### 1.1 Market evolution

According to Gartner's 2024 Magic Quadrant for SIEM, the global SIEM market is projected to grow from $5.7 billion in 2024 to $8.2 billion by 2026 (CAGR ~20%). This growth is fueled by:

- The expansion of **regulatory compliance frameworks** (GDPR, NIS2 Directive, DORA, ISO 27001).
- The increasing **attack surface** of hybrid infrastructures (on-premises + cloud).
- The **shortage of cybersecurity talent**, driving demand for automation.
- The accelerating adoption of **MITRE ATT&CK** as a common detection framework.

### 1.2 The convergence of SIEM and XDR

A defining trend of 2025-2026 is the **convergence of SIEM (log aggregation and correlation) with XDR (endpoint detection and response)**. Traditional SIEM vendors (Splunk, IBM QRadar, Microsoft Sentinel) are integrating endpoint telemetry, while XDR vendors (CrowdStrike, SentinelOne) are absorbing SIEM functions.

This convergence reduces tool sprawl but typically increases per-seat licensing costs. For SMEs operating with constrained budgets, this trend creates a strong incentive to evaluate **converged open-source platforms** like Wazuh, which natively combine SIEM, EDR, and File Integrity Monitoring (FIM) within a single agent.

### 1.3 The open-source SIEM segment

Once limited to large-scale "build vs. buy" deliberations, open-source SIEM is now a viable choice for SMEs due to:

- **Hardware cost reduction**: VM resources required for SIEM workloads are increasingly affordable.
- **Documentation maturity**: open-source projects now provide enterprise-grade documentation.
- **Community ecosystems**: pre-built integrations cover most common applications.
- **Hybrid deployment models**: Wazuh, ELK, and Graylog support both fully self-hosted and managed-service options.

---

## 2. WAZUH: PLATFORM OVERVIEW

### 2.1 Architecture

Wazuh is a **unified open-source XDR/SIEM platform** released under the GPL v2 license. Its architecture comprises three core components:

```
+------------------+      +-----------------+      +------------------+
|   Wazuh Agents   |  ->  |  Wazuh Manager  |  ->  |  Wazuh Indexer   |
|  (endpoints)     |      |  (correlation)  |      |  (OpenSearch)    |
+------------------+      +-----------------+      +------------------+
                                                            |
                                                            v
                                                  +------------------+
                                                  |  Wazuh Dashboard |
                                                  |  (visualization) |
                                                  +------------------+
```

- **Agents** (~50 MB RAM each) deployed on Windows/Linux/macOS endpoints.
- **Manager** correlates events, applies rules, generates alerts.
- **Indexer** (based on OpenSearch, formerly Elasticsearch fork) stores events.
- **Dashboard** provides visualization, search, and reporting.

### 2.2 Core capabilities

- **Log data collection and correlation** (SIEM functions).
- **File Integrity Monitoring (FIM)** to detect unauthorized changes.
- **Configuration assessment** against CIS benchmarks.
- **Vulnerability detection** against CVE databases.
- **Active response** (automated remediation actions).
- **Cloud workload protection** (AWS, Azure, GCP integrations).
- **Container security** (Docker, Kubernetes).
- **Compliance reporting** (PCI DSS, GDPR, HIPAA, NIST 800-53, MITRE ATT&CK).

### 2.3 Differentiators

Compared to competitors, Wazuh offers:

| Feature | Wazuh | Splunk Enterprise | ELK + Beats | Microsoft Sentinel |
|---------|-------|---------------------|-------------|---------------------|
| License cost | Free (GPL) | $22,000+/year (50 GB/day) | Free (open-source) but components only | $2-4/GB ingested |
| Built-in SIEM rules | 5,000+ | 1,000+ | Requires custom | 200+ analytics rules |
| EDR / Endpoint agent | Native | Add-on | Requires Beats + Osquery | Defender for Endpoint (separate) |
| Compliance mapping | PCI/GDPR/HIPAA/MITRE | Add-on apps | Manual configuration | Native |
| Cloud integrations | AWS/Azure/GCP | All major | All major | Azure-native |
| MITRE ATT&CK coverage | Built-in tagging | Built-in | Manual mapping | Built-in |
| Average install time | < 1 day | 1-2 weeks | 2-4 weeks | < 1 day (cloud) |

---

## 3. ADOPTION TRENDS IN SMES (2025-2026)

### 3.1 Quantitative indicators

According to public Wazuh statistics (Wazuh public usage data, Sysdig 2024 Open Source Security Report):

- **+15 million deployed agents** worldwide as of late 2024 (vs ~10 M in 2022).
- **Adoption in 50+ countries**.
- **Top sectors**: financial services (24%), healthcare (18%), technology/SaaS (16%), public sector (12%), industry/logistics (10%).
- **Median deployment size in SMEs**: 50-500 endpoints.

### 3.2 Drivers of SME adoption

Multiple factors converge to make Wazuh particularly attractive to SMEs in 2025-2026:

1. **Budget pressure**: with median IT security budgets in European SMEs ranging from €15,000 to €50,000/year (CESIN 2024 survey), commercial SIEM licenses (Splunk, QRadar) are out of reach.
2. **Regulatory acceleration**: NIS2 Directive (effective October 2024) extends cybersecurity obligations to a much wider scope of European SMEs.
3. **Cyber-insurance requirements**: insurers increasingly require demonstrable SIEM/EDR capabilities, regardless of organization size.
4. **Sovereignty concerns**: European SMEs in regulated sectors (defense, healthcare) increasingly favor solutions whose code can be audited and self-hosted on-premises.

### 3.3 Common deployment patterns

- **Single-server deployment** (all components on one VM): typical for SMEs <100 endpoints.
- **Distributed deployment** (separate Manager / Indexer / Dashboard): mid-market 100-1000 endpoints.
- **Multi-cluster**: large organizations 1000+ endpoints.

For Nova Syndicate (85 employees, ~10 production VMs), a **single-server deployment** is appropriate, hosted on a dedicated VM with 4 GB RAM and 50 GB disk.

---

## 4. KEY TRENDS AND OUTLOOK 2025-2026

### 4.1 AI-augmented threat detection

Wazuh 4.7+ (released Q4 2024) introduces enhanced anomaly detection capabilities through statistical baselines and unsupervised machine learning models. Trends anticipated for 2026:

- Integration with **OpenAI / Anthropic models** for natural-language alert summarization.
- **Automatic playbook generation** based on attack patterns.
- **Predictive threat scoring** combining vulnerability scan + behavioral baseline.

### 4.2 MITRE ATT&CK as universal taxonomy

The MITRE ATT&CK framework has become the de facto reference for adversary tactics. Wazuh has fully integrated ATT&CK tagging since version 4.4 (2023). In 2025-2026:

- All Wazuh alerts now reference an ATT&CK technique.
- Compliance reports automatically generated against ATT&CK coverage.
- Threat hunting based on ATT&CK Sub-techniques.

### 4.3 Cloud-native architectures

The trend toward containerized and cloud-native deployments is mirrored in Wazuh's roadmap:

- Helm charts for Kubernetes deployment.
- Native integration with cloud-native logging (AWS CloudTrail, Azure Monitor, GCP Cloud Logging).
- Sidecar agents for ephemeral workloads.

### 4.4 Threat intelligence enrichment

Wazuh 4.8 (early 2025) added enriched threat intelligence integration:

- VirusTotal API.
- AbuseIPDB.
- MISP (Malware Information Sharing Platform).
- Custom STIX/TAXII feeds.

---

## 5. RELEVANCE TO NOVA SYNDICATE PROJECT

### 5.1 Match with project requirements

The Nova Syndicate infrastructure (medical, aerospace, defense distribution) imposes:

- **Strong traceability** of access and changes (regulatory).
- **Incident detection capability** for sensitive data.
- **Cost containment** within SME budget bounds.
- **Sovereignty / auditability** of the security stack.

Wazuh addresses all four requirements:

| Requirement | Wazuh Response |
|-------------|----------------|
| Centralized logging | Manager + Indexer + Agent on all VMs |
| Real-time alerting | Email and webhook alerts, integration with email server |
| Compliance reporting | Native templates (PCI DSS, GDPR, HIPAA) |
| Cost | 0 € licensing (only hardware/operational costs) |
| Auditability | Open source — entire codebase reviewable |

### 5.2 Implementation considerations

For the Nova Syndicate deployment:

- **Hardware**: 4 GB RAM, 2 vCPUs, 50 GB disk for single-server Wazuh.
- **Agents**: deployed on all VMs (DC, web, DB, file, mail, bastion, backup, honeypot).
- **Network design**: dual-interface Wazuh-01 (eth0 for management/SERVERS collection, eth1 on dedicated bridge for DMZ/Quarantine collection).
- **Retention**: 12 months minimum for regulatory compliance (medical/defense).
- **Alert integration**: SMTP forwarding to internal Mail-01.

### 5.3 Identified limitations and mitigations

| Limitation | Mitigation |
|------------|------------|
| No 24/7 vendor support | Internal documentation + community support + paid commercial support available if needed |
| Resource consumption on small infrastructures | Tuning of agent collection rules + log rotation |
| Steeper learning curve than commercial UIs | Investment in admin training (2 days) |
| TLS certificates self-managed | Internal CA or Let's Encrypt automation |

---

## 6. CONCLUSION

Wazuh has reached a maturity level that makes it a **credible choice for SMEs facing increasing compliance pressure** without the budget for enterprise SIEM solutions. The platform's open-source nature, combined with native MITRE ATT&CK alignment and a comprehensive feature set, positions it as the **leading open-source alternative** to commercial SIEM/XDR in 2025-2026.

For Nova Syndicate, the adoption of Wazuh is strategically justified by:

- A TCO reduction of **~95 % compared to Splunk Enterprise** on a 3-year horizon.
- Full alignment with the regulatory framework imposed by the medical/aerospace/defense sectors.
- A natural fit with the rest of the open-source stack adopted (Proxmox, OPNsense, Samba).
- A capability roadmap aligned with industry trends (AI augmentation, threat intelligence, cloud-native).

The forecast for 2026-2028 indicates continued strong adoption growth in the European SME segment, with NIS2 acting as a major accelerator. Organizations adopting Wazuh today position themselves favorably for the regulatory evolution.

---

## REFERENCES

- Gartner, *Magic Quadrant for Security Information and Event Management*, 2024.
- Wazuh, *Public Documentation and Use Cases*, available at https://documentation.wazuh.com.
- ENISA, *Cybersecurity Maturity Assessment for SMEs*, 2024.
- MITRE Corporation, *ATT&CK Framework*, current version (v15), available at https://attack.mitre.org.
- European Parliament and Council, *Directive (EU) 2022/2555 (NIS2 Directive)*, 2022.
- Sysdig, *Open Source Security Report*, 2024.
- CESIN, *Baromètre de la cybersécurité des entreprises*, 9th edition, 2024.

---

**End of document — version 1.0** — May 2026

*This technology watch report is part of the Nova Syndicate IT Modernization mission deliverables. It is provided as reference material to support technological decision-making.*
