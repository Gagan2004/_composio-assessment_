"""
src/embed_html.py
Embeds data/apps_pass2_verified.json and data/verification_sample.json directly into index.html
so the Case Study works standalone via file:// or http://.

Idempotency: Safe to run multiple times — detects a previous injection via the
COMPOSIO_EMBED_START / COMPOSIO_EMBED_END delimiters and strips it before re-injecting.
Post-write validation confirms the first app name is present in the output file.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
VERIFIED_FILE = os.path.join(BASE_DIR, "data", "apps_pass2_verified.json")
SAMPLE_FILE = os.path.join(BASE_DIR, "data", "verification_sample.json")
HTML_FILE = os.path.join(BASE_DIR, "index.html")

# Explicit delimiters that survive re-runs — placed inside the JS <script> block.
EMBED_START_MARKER = "/* COMPOSIO_EMBED_START */"
EMBED_END_MARKER   = "/* COMPOSIO_EMBED_END */"

with open(VERIFIED_FILE, "r", encoding="utf-8") as f:
    verified_data = json.load(f)

with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
    sample_data = json.load(f)

with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

# ── Build the replacement script block ───────────────────────────────────────
embedded_script = f"""{EMBED_START_MARKER}
    let appDataset = {json.dumps(verified_data["apps"])};
    let pipelineTelemetry = {json.dumps(verified_data.get("telemetry", {}))};
    let auditSample = {json.dumps(sample_data["audit_sample"])};
    let currentCategory = 'all';

    async function loadData() {{
      try {{
        const res = await fetch('data/apps_pass2_verified.json');
        if (res.ok) {{
          const data = await res.json();
          appDataset = data.apps;
          pipelineTelemetry = data.telemetry || pipelineTelemetry;
        }}
        const resSample = await fetch('data/verification_sample.json');
        if (resSample.ok) {{
          const dataSample = await resSample.json();
          auditSample = dataSample.audit_sample;
        }}
      }} catch (err) {{
        console.log("Using embedded dataset fallback.");
      }}
      renderTable(appDataset);
      renderSampleTable(auditSample);
      initCharts();
    }}
    {EMBED_END_MARKER}"""

# ── Idempotency & Injection ───────────────────────────────────────────────────
if EMBED_START_MARKER in html_content and EMBED_END_MARKER in html_content:
    start_idx = html_content.find(EMBED_START_MARKER)
    end_idx = html_content.find(EMBED_END_MARKER) + len(EMBED_END_MARKER)
    new_html = html_content[:start_idx] + embedded_script.strip() + html_content[end_idx:]
elif "let appDataset =" in html_content:
    start_idx = html_content.find("let appDataset =")
    end_idx = html_content.find("window.onload = loadData;")
    new_html = html_content[:start_idx] + embedded_script.strip() + "\n\n    " + html_content[end_idx:]
else:
    print("[ERROR] Could not find script anchor markers in index.html.")
    exit(1)

with open(HTML_FILE, "w", encoding="utf-8") as f:
    f.write(new_html)

# ── Post-write validation ─────────────────────────────────────────────────
with open(HTML_FILE, "r", encoding="utf-8") as f:
    written = f.read()

first_app_name = verified_data["apps"][0]["name"]
if first_app_name in written and EMBED_START_MARKER in written:
    print(f"[SUCCESS] Embed verified OK — '{first_app_name}' found in index.html ({len(verified_data['apps'])} apps embedded).")
else:
    print("[VALIDATION FAILED] Embedded data not detected in written file — check markers in index.html.")
