# DocMind AI — AI-Assisted Document Workflow Prototype

DocMind AI is a Streamlit-based document assistant prototype. It supports multi-format document reading and analysis scenarios such as PDF / Word / Excel processing, document comparison, and AI-assisted summarisation.

## Positioning

This is best presented as an **AI-assisted workflow prototype**, not as a hand-coded software engineering project.

Recommended wording:

> I identified the document workflow pain points, designed the usage scenario and interaction flow, and used AI tools to generate and iterate the Streamlit/Python implementation. My main contribution was problem framing, workflow design, prompt-based iteration, testing, and business-oriented presentation.

## Core Functions

- Upload and analyse PDF / Word / Excel files
- Compare document versions
- Generate AI-assisted summaries and responses
- Streamlit web interface
- Mobile-responsive UI
- API-key based AI integration

## Tech Stack

Python, Streamlit, OpenAI-compatible API, pdfplumber, python-docx, openpyxl, reportlab.

## Run Locally

```bash
cd projects/01_docmind_ai
python -m venv .venv
source .venv/bin/activate   # macOS/Linux/Ubuntu
# Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -r requirements.txt
streamlit run app.py
```

## Notes

- Do not commit real API keys.
- Use Streamlit secrets or environment variables for deployment.
- This project should be explained from a business workflow perspective rather than deep backend engineering.


---

## 中文展示定位（当前升级版补充）

**项目名称：** 智能文档处理工具 DocMind

本项目保留原版操作方式：双击 `run_windows.bat` 后会自动创建虚拟环境、安装依赖，并在本地浏览器打开 Streamlit。若页面侧边栏提供 API Key 输入框，请先输入 Key 并点击“应用/Apply”后再使用 AI 生成功能。

**注意：** 不要把 API Key 提交到 GitHub；部署公网 Demo 时建议使用 Streamlit Secrets。
