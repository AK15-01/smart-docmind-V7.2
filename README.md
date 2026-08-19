# DocMind AI

An AI-powered workspace for document processing, long-document analysis, version comparison, and intelligent Q&A, built with Python and Streamlit.

DocMind AI 是一个基于 Python 与 Streamlit 的 AI 文档处理、长文分析、文件版本对比与智能问答工作台，面向公开演示、日常文档理解与轻量批处理场景。

## Online Demo

[Open the public Streamlit demo](https://smart-docmind-v7-anson.streamlit.app/)

> The demo may use third-party AI and search services. Do not upload highly sensitive, confidential, regulated, or legally privileged material.

## Features

- Multi-format document parsing and multi-file batch processing
- No-AI basic mode with text preview, document statistics, extracted-text export, and exact Diff
- AI summarization, translation, rewriting, and custom instructions
- Structured information extraction, risk analysis, and data analysis
- Two-layer comparison: exact line Diff without AI, plus optional AI change/risk explanation
- Long-document chunking with Map-Reduce aggregation
- AI Chat with optional web-search context
- Tavily / Bocha search with DuckDuckGo / Baidu fallback
- Session-scoped processing history
- TXT, Word, and Excel result export
- Responsive Streamlit interface with optional login protection
- DeepSeek and other OpenAI-compatible APIs
- Isolated Server API and BYOK configuration modes

## Supported Formats

| Format | Notes |
| --- | --- |
| PDF | Text-layer PDFs; OCR is not included |
| DOCX | Paragraphs and tables |
| XLSX | Modern Excel workbooks |
| CSV | Tries `utf-8-sig`, `utf-8`, then `gb18030` |
| TXT | Tries the same common UTF-8/Chinese encodings |

Legacy `.xls` files are intentionally not accepted because the project uses `openpyxl`. Convert them to `.xlsx` before upload.

## Tech Stack

- Python
- Streamlit
- OpenAI Python SDK and OpenAI-compatible APIs
- DeepSeek
- `pdfplumber`
- `python-docx`
- `openpyxl`
- `defusedxml`
- `httpx`
- `ddgs`
- ReportLab

## Architecture

```text
Upload
   ↓
Parse
   ↓
Chunk / Structure
   ↓
Basic Preview / Statistics / Exact Diff
   ↓
Optional AI Processing
   ↓
Merge / Compare / Result
   ↓
Export
```

Short analysis tasks use one AI request. Longer analysis documents are split at paragraph or sentence boundaries into approximately 6,500-character blocks, with a 300-character overlap and a maximum of 10 blocks. Translation and rewriting use smaller, non-overlapping blocks of approximately 3,500 characters. If the API reports `finish_reason=length`, DocMind attempts up to two continuations and warns when output may still be incomplete. When the input limit is reached, the UI reports the actual processing range instead of silently truncating the document.

Document comparison always provides an exact line-based Diff without AI. When AI is available, long files can additionally be converted block-by-block into structured intermediate representations for a higher-level explanation of key changes and risks.

## Basic Mode and Graceful Degradation

DocMind does not require an API Key for core document work. Without AI configuration, users can still parse supported files, preview and download extracted text, inspect character/paragraph and spreadsheet statistics, export extracted text, and compare two documents with an exact Diff. AI-only actions are disabled individually.

If an AI request fails because of authentication, quota/rate limiting, timeout, network failure, unavailable model, server error, or empty output, the already parsed document and basic comparison remain available. The public UI shows a short sanitized explanation while diagnostic logs exclude API keys.

## API Configuration and Security

DocMind has two mutually exclusive AI configuration modes:

- **Server mode:** when `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` is configured on the server, the key is bound to its matching server-controlled Base URL and Model. `DEEPSEEK_MODEL` / `OPENAI_MODEL` override the provider default. The UI reveals neither the key nor Base URL and cannot change the server Base URL or Model.
- **BYOK mode:** when no server AI key exists, users can select DeepSeek/OpenAI defaults or enter an advanced OpenAI-compatible API Key, Base URL, and Model. BYOK URLs must use HTTPS and are rejected if they contain credentials or resolve to localhost, private, link-local, multicast, reserved, or metadata-service addresses. Values remain in the current Streamlit Session only and are not written to history, logs, a database, or local files by DocMind.

Search-service keys configured on the server are also kept out of editable frontend fields. Logs record operation context and sanitized error categories, not configured API keys.

## Privacy & Security

- Uploaded files are read for the current processing flow and are not deliberately persisted to disk by the application.
- Processing history is held in the current Streamlit Session and is lost when the session ends or the app restarts.
- Server API keys are not displayed in the frontend.
- API keys are never hard-coded in source code, and `.streamlit/secrets.toml` is excluded from Git.
- Server mode locks both Base URL and Model; BYOK values cannot override server configuration.
- BYOK Base URLs are validated against SSRF-sensitive hosts and IP ranges before a request is created.
- BYOK credentials are session-scoped; they are still sent to the user-selected AI provider when a request is made.
- Document text and optional search context are sent to the configured third-party AI API. Their retention and privacy policies are outside this project's control.
- The public demo is not intended for highly sensitive or confidential documents.
- Optional username/password protection is lightweight demo access control, not an enterprise identity system.

## Limitations

- Scanned or image-only PDFs cannot be parsed without a text layer; OCR is not part of this release.
- Very long documents are chunked and capped at 10 blocks to control cost and request volume.
- Application-level safeguards currently limit an individual file to 40 MB, PDFs to 300 pages, workbooks to 50 sheets / 500,000 effective cells, and CSV files to 200,000 rows. DOCX decompression and extracted-text size are also bounded.
- AI output can be incomplete or incorrect and should be reviewed by a person, especially for legal, financial, or compliance use.
- Web search depends on third-party availability, network conditions, and upstream result formats.
- DocMind assists analysis and does not replace legal, financial, medical, or other professional judgment.
- `.xls` is not supported; use `.xlsx`.
- The app keeps history in memory only and does not provide durable project storage.

## Local Development

**Supported Python: 3.10–3.14. Recommended / Production: Python 3.13.**

Windows users can double-click `run.bat`. On first run it creates `.venv`, upgrades pip, installs `requirements.txt`, and starts Streamlit. Later runs reuse the existing environment.

Command-line setup:

```bash
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m streamlit run app.py
```

Development and test dependencies are separate:

```bash
pip install -r requirements-dev.txt
pytest
```

The Streamlit Community Cloud entry point remains `app.py`.

## Deployment

The existing deployment flow remains unchanged:

```text
GitHub main
   ↓
Streamlit Community Cloud
   ↓
Automatic redeployment of the existing app
```

Push updates to the connected `main` branch; a new Streamlit App does not need to be created for each release.

## Environment Variables / Streamlit Secrets

The same names can be supplied as environment variables or top-level Streamlit Secrets. Only configure the variables you need:

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL`
- `DEEPSEEK_MODEL`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- `TAVILY_API_KEY`
- `BOCHA_API_KEY`
- `DOCMIND_USERS`
- `DOCMIND_LOG_LEVEL`

`DOCMIND_USERS` accepts a JSON object mapping usernames to passwords. Streamlit Secrets may also provide it as a TOML table/object. Keep all real credentials out of Git.

Legacy `TAVILY_KEY` and `BOCHA_KEY` names remain supported for existing deployments, but the `_API_KEY` names are preferred.

## Validation

Run the repository's offline core tests with:

```bash
pytest
python -m unittest discover -s tests -v
python -m py_compile app.py docmind_core.py
```

For a local UI smoke test:

```bash
python -m streamlit run app.py
```

## Release

**DocMind V2.2 — Stable / Graceful Degradation Release** keeps AI as an enhancement instead of a runtime prerequisite. It focuses on offline-capable document basics, safe failure handling, SSRF-resistant BYOK configuration, bounded parsing, and predictable deployment without redesigning the existing interface.

GitHub-generated source archives include tracked repository files only. For a local release archive after committing, use `git archive --format=zip --output=DocMind-V2.2.zip HEAD`; this excludes `.git` and ignored local environments such as `.venv`.
