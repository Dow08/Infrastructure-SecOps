#!/usr/bin/env python3
"""
Build Nova Syndicate ODP presentation from Jedha template.
Creates 10 slides with structure only (text placeholders).
"""

import zipfile
import shutil
import os
import re
import xml.etree.ElementTree as ET
from copy import deepcopy

TEMPLATE = r"Z:\NOVA SYNDICATE V2\TEMPLATE SLIDES - jedha Dorian.P.odp"
OUTPUT = r"Z:\NOVA SYNDICATE V2\livrables\08_presentation_slides\Nova_Syndicate_Soutenance.odp"
TEMP_DIR = r"Z:\NOVA SYNDICATE V2\livrables\08_presentation_slides\_temp_odp"

# ── Step 1: Copy template as base ──
print("[1/5] Copying template...")
shutil.copy2(TEMPLATE, OUTPUT)

# ── Step 2: Read content.xml ──
print("[2/5] Reading content.xml...")
with zipfile.ZipFile(OUTPUT, 'r') as zin:
    content_xml = zin.read('content.xml').decode('utf-8')
    all_files = zin.namelist()
    # Read all other files into memory
    archive_contents = {}
    for name in all_files:
        archive_contents[name] = zin.read(name)

# ── Step 3: Parse and extract slide templates ──
print("[3/5] Parsing slides...")

# We need to work with raw XML string manipulation because
# the ODP XML has complex namespaces that ET struggles with.
# Strategy: find each <draw:page ...>...</draw:page> block

def extract_pages(xml_str):
    """Extract individual draw:page elements as strings."""
    pages = []
    pattern = r'(<draw:page\s[^>]*draw:name="[^"]*".*?</draw:page>)'
    # Use DOTALL so . matches newlines
    matches = re.findall(pattern, xml_str, re.DOTALL)
    return matches

def get_page_name(page_xml):
    m = re.search(r'draw:name="([^"]*)"', page_xml)
    return m.group(1) if m else "unknown"

def get_style_name(page_xml):
    m = re.search(r'draw:style-name="([^"]*)"', page_xml)
    return m.group(1) if m else "unknown"

def get_master_page(page_xml):
    m = re.search(r'draw:master-page-name="([^"]*)"', page_xml)
    return m.group(1) if m else "unknown"

pages = extract_pages(content_xml)
print(f"   Found {len(pages)} template slides")

for i, p in enumerate(pages):
    name = get_page_name(p)
    style = get_style_name(p)
    master = get_master_page(p)
    print(f"   Slide {i+1}: name={name}, style={style}, master={master}")

# ── Step 4: Build 10 slides ──
print("[4/5] Building 10 presentation slides...")

# Template slide indices (0-based):
# 0 = page1 (title, turquoise bg, dp1) - TITLE + Subtitle + logo + image
# 1 = page2 (section title, light blue bg, dp3) - Section Title + logo
# 2 = page3 (bullet points, white bg, dp4) - Title + 3 bullet points + logo + bar
# 3 = Text  (text + bullets, white bg, dp4) - Text block left + bullets right + logo
# 4 = page5 (graph/image, white bg, dp4) - Title + image + legend + logo + bar
# 5 = page6 (citation, dark blue bg, dp5) - Citation + author + logo
# 6 = page7 (thanks, cyan bg, dp6) - Thanks text + logo + image

def replace_text_in_spans(page_xml, replacements):
    """Replace text content within text:span elements.
    replacements is a list of (old_text, new_text) tuples applied in order."""
    result = page_xml
    for old, new in replacements:
        result = result.replace(old, new)
    return result

def set_page_name(page_xml, new_name):
    """Change the draw:name attribute of a page."""
    return re.sub(
        r'(draw:name=")[^"]*(")',
        lambda m: m.group(1) + new_name + m.group(2),
        page_xml,
        count=1
    )

def set_notes_page_number(page_xml, num):
    """Update the notes page number."""
    return re.sub(
        r'draw:page-number="\d+"',
        f'draw:page-number="{num}"',
        page_xml
    )

# Clone template slides for our 10 slides:
# Slide 1  (Page de garde)       -> based on page1 (template 0)
# Slide 2  (Contexte)            -> based on page3 (template 2) - bullet layout
# Slide 3  (Architecture)        -> based on page5 (template 4) - graph/image layout
# Slide 4  (Stack technique)     -> based on page3 (template 2) - bullet layout
# Slide 5  (Deploiement & IaC)   -> based on page3 (template 2) - bullet layout
# Slide 6  (Securite DiD)        -> based on page3 (template 2) - bullet layout
# Slide 7  (POC & Preuves)       -> based on page5 (template 4) - graph/image layout
# Slide 8  (PCA/PRA Conformite)  -> based on Text  (template 3) - two-column layout
# Slide 9  (Etude economique)    -> based on page3 (template 2) - bullet layout
# Slide 10 (Conclusion & Q&A)    -> based on page7 (template 6) - closing layout

slide_configs = [
    {
        "name": "slide1",
        "template_idx": 0,  # page1 - title
        "replacements": [
            ("TITLE", "Nova Syndicate"),
            ("Subtitle", "Infrastructure Réseau Sécurisée"),
        ]
    },
    {
        "name": "slide2",
        "template_idx": 2,  # page3 - bullets
        "replacements": [
            ("Title", "Contexte et Objectifs"),
            ("Bullet point 1", "BricoPro (e-commerce) — 2 sites : Lyon + Marseille"),
            ("Bullet point 2", "Infrastructure complète, segmentée, sécurisée"),
            ("Bullet point 3", "Conforme ISO 27001 · ANSSI · NIST"),
        ]
    },
    {
        "name": "slide3",
        "template_idx": 4,  # page5 - graph/image
        "replacements": [
            ("Title or Graph", "Architecture Cible"),
            ("Legend", "Hub &amp; Spoke · Defense in Depth · 12 VMs · IPsec AES-256"),
        ]
    },
    {
        "name": "slide4",
        "template_idx": 2,  # page3 - bullets
        "replacements": [
            ("Title", "Stack Technique"),
            ("Bullet point 1", "Proxmox VE 9 · OPNsense · Samba 4 AD · MariaDB"),
            ("Bullet point 2", "Wazuh SIEM · Suricata IDS · Prometheus · Grafana"),
            ("Bullet point 3", "Terraform + Ansible (10 playbooks) · CI/CD DevSecOps"),
        ]
    },
    {
        "name": "slide5",
        "template_idx": 2,  # page3 - bullets
        "replacements": [
            ("Title", "Déploiement et Infrastructure-as-Code"),
            ("Bullet point 1", "Terraform : 12 VMs + bridges + VLANs sur Proxmox"),
            ("Bullet point 2", "Ansible : 10 playbooks idempotents (site.yml)"),
            ("Bullet point 3", "Redéploiement complet en 45 min · Reproductible · DR"),
        ]
    },
    {
        "name": "slide6",
        "template_idx": 2,  # page3 - bullets
        "replacements": [
            ("Title", "Defense in Depth — 5 Couches"),
            ("Bullet point 1", "1. Périmètre (OPNsense + Suricata 5 865 règles)"),
            ("Bullet point 2", "2. Segmentation (5 VLANs) + 3. Hardening (Fail2ban)"),
            ("Bullet point 3", "4. Détection (Wazuh SIEM) + 5. Audit (Loki + Grafana)"),
        ]
    },
    {
        "name": "slide7",
        "template_idx": 4,  # page5 - graph/image
        "replacements": [
            ("Title or Graph", "Preuves de Fonctionnement (POC)"),
            ("Legend", "25 incidents documentés · Symptôme → Cause racine → Fix → Apprentissage"),
        ]
    },
    {
        "name": "slide8",
        "template_idx": 2,  # page3 - bullets (simpler, avoids Text layout repeat bug)
        "replacements": [
            ("Title", "PCA/PRA et Conformité"),
            ("Bullet point 1", "PCA : 17 risques cotés · RTO/RPO · BIA sur 11 services"),
            ("Bullet point 2", "PRA : 5 scénarios · Sauvegarde 3-2-1 · Marseille = repli"),
            ("Bullet point 3", "ISO 27001 · ANSSI · NIST · MITRE ATT&amp;CK · RGPD"),
        ]
    },
    {
        "name": "slide9",
        "template_idx": 2,  # page3 - bullets
        "replacements": [
            ("Title", "Étude Économique — TCO 3 ans"),
            ("Bullet point 1", "A. Propriétaire (VMware+MS) : 173 042 €"),
            ("Bullet point 2", "B. Open-source on-premise : 38 730 €  ← RETENUE"),
            ("Bullet point 3", "C. Cloud public (AWS) : 95 200 €  |  −78% vs A"),
        ]
    },
    {
        "name": "slide10",
        "template_idx": 6,  # page7 - closing
        "replacements": [
            ("Thanks!", "Questions ?"),
            ("See you in the next course", "Dorian Poncelet — github.com/Dow08"),
        ]
    },
]

new_pages = []
for i, config in enumerate(slide_configs):
    page = pages[config["template_idx"]]
    # Set unique page name
    page = set_page_name(page, config["name"])
    # Set notes page number
    page = set_notes_page_number(page, i + 1)
    # Apply text replacements
    for old, new in config["replacements"]:
        page = page.replace(old, new)
    new_pages.append(page)
    print(f"   Slide {i+1}: {config['name']} (from template {config['template_idx']})")

# ── Step 5: Rebuild content.xml and write ODP ──
print("[5/5] Writing final ODP...")

# Find the body section and replace all pages
# The pages are between <office:body><office:presentation> ... </office:presentation></office:body>
pres_start = content_xml.find('<office:presentation')
pres_end = content_xml.find('</office:presentation>') + len('</office:presentation>')

# Get the presentation opening tag
pres_tag_end = content_xml.find('>', pres_start) + 1
pres_opening = content_xml[pres_start:pres_tag_end]

# Build new presentation section
new_presentation = pres_opening + "\n"
for page in new_pages:
    new_presentation += page + "\n"
new_presentation += "</office:presentation>"

# Replace in content
new_content = content_xml[:pres_start] + new_presentation + content_xml[pres_end:]

# Write new ODP
with zipfile.ZipFile(OUTPUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for name in all_files:
        if name == 'content.xml':
            zout.writestr(name, new_content.encode('utf-8'))
        else:
            zout.writestr(name, archive_contents[name])

print(f"\nDone! ODP created: {OUTPUT}")
print(f"File size: {os.path.getsize(OUTPUT):,} bytes")
print("\n10 slides created:")
for i, config in enumerate(slide_configs):
    print(f"  {i+1}. {config['name']}: {config['replacements'][0][1] if config['replacements'] else '?'}")
