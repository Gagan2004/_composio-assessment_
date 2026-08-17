# Composio App Ecosystem Research & Verification Pipeline

> **Composio AI Product Ops Take-Home Assignment Case Study**  
> An automated direct AI research agent pipeline analyzing 100 SaaS & developer platforms across 10 categories to evaluate auth paradigms, developer gating, API surface breadth, MCP readiness, and agent toolkit buildability.

---

## ⚡ Quickstart (TL;DR)

Run the entire pipeline and view the interactive dashboard in 3 simple steps:

```bash
# 1. Install dependencies
pip install google-genai google-generativeai

# 2. Run the AI Research Pipeline & Embed dataset into index.html
python src/verifier.py
python src/embed_html.py

# 3. Open index.html in your browser!
```

---

## 📋 Prerequisites & Setup

### Requirements
- **Python**: Version 3.9 or higher
- **Browser**: Any modern web browser (Chrome, Edge, Firefox, Safari)

### API Key Configuration (`.env`)

Create a `.env` file in the project root containing your Gemini API key(s):

```env
# Single Key Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# OR Multi-Key Configuration (Multiplies RPM throughput)
GEMINI_API_KEY_1=your_first_gemini_key
GEMINI_API_KEY_2=your_second_gemini_key
GEMINI_API_KEY_3=your_third_gemini_key
```

---

## 🚀 How to Run the Project

### Step 1: Run the AI Research & Verification Agent
Executes `src/verifier.py` to ingest 100 raw app records from `data/apps_raw.json`, perform concurrent live scraping, and run Gemini 2.5 Flash structured inference:

```bash
python src/verifier.py
```

**What happens under the hood:**
- **Concurrent Scraping**: 15 parallel workers ping and scrape live developer documentation URLs (`https://<website_hint>`).
- **Signal Trimming**: Scans keywords and trims HTML payloads into $\le 3\text{ KB}$ signal-rich excerpts (~97% token reduction).
- **Multi-Key Inference**: Rotates queries across all active `.env` keys in round-robin order.
- **Quota Failover**: If Gemini API rate limits occur (429), `synthesize_heuristic_fallback()` synthesizes inferred attributes from scraped HTML signals.
- **Output**: Generates `data/apps_pass2_verified.json` and a 25-app stratified review sample `data/verification_sample.json`.

---

### Step 2: Embed Verified Data into `index.html`
Executes `src/embed_html.py` to embed `data/apps_pass2_verified.json` directly into `index.html`:

```bash
python src/embed_html.py
```

**Why this is needed:**
- Enables `index.html` to run **100% standalone** via `file://` (double-clicking the file) without hitting browser CORS restrictions.
- **Idempotent**: Safe to re-run multiple times — automatically strips previous embeds before re-injecting fresh data.

---

### Step 3: Open the Interactive Case Study Dashboard

#### Option A: Direct File Launch (No server needed!)
Simply double-click [index.html](file:///c:/Users/gagan/OneDrive/projects/composio/index.html) or open it directly in your browser.

#### Option B: Local HTTP Server
```bash
python -m http.server 8000
# Then open http://localhost:8000 in your browser
```

---

## 📁 Project Directory Layout

```
composio-app-research/
├── index.html                   # Standalone Interactive Case Study & Dashboard
├── README.md                    # Quickstart guide & user instructions
├── DRY_RUN_ARCHITECTURE_AUDIT.md# Comprehensive system execution dry run & audit
├── .env                         # Gemini API key(s) configuration file
├── data/
│   ├── apps_raw.json            # 100 raw input app seeds across 10 categories
│   ├── apps_pass2_verified.json # Master verified dataset output (100 apps + telemetry)
│   └── verification_sample.json # 25-App stratified human review sample
└── src/
    ├── verifier.py              # Direct AI Research & Verification Agent Pipeline
    └── embed_html.py            # Idempotent dataset embedder for standalone index.html
```

---

## 📊 Summary of Ecosystem Research Findings

| Category / Dimension | Key Pattern Discovered | Strategic Takeaway for Composio |
| :--- | :--- | :--- |
| **Authentication** | **46% OAuth2**, **41% API Keys**, **13% Basic/Custom** | Build multi-tenant OAuth refresh token management for B2B SaaS; use instant API keys for Dev/AI tools. |
| **Developer Gating** | **81% Self-Serve**, **19% Enterprise Gated** | Immediate green light for 81 tools; 19 tools require partner agreements or enterprise sales accounts. |
| **Toolkit Readiness** | **79% Ready Today**, **10% Workaround Required**, **11% Blocked** | 79 tools can be converted to Composio agent toolkits immediately without external friction. |
| **Top Blockers** | **Enterprise Sales Gates (11%)**, **App Review Forms (5%)** | Prioritize Tier 1 instant self-serve tools (Linear, Supabase, Firecrawl) while BD leads outreach on Tier 3 (DealCloud, PitchBook). |

---

## 🛠️ Architecture Highlights & Technical Details

1. **Adaptive Scraping Escalation**: Fast 15KB scan $\to$ deep 100KB payload escalation for JS-rendered documentation portals.
2. **Gemini Key Rotator**: Thread-safe round-robin API key rotator multiplies request throughput while enforcing concurrency limits.
3. **Keyword Excerpt Scoring**: Extracts top keyword-dense paragraphs to minimize LLM token costs.
4. **Schema Contract Validation**: Runs cross-field consistency checks (`validate_schema_and_rules()`) on every app record.

---

## 📄 License & Presentation

This repository is submitted as part of the **Composio AI Product Ops Assignment**.  
All code and UI components are available under the Apache 2.0 License.
