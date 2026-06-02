"""
DocMind AI  v2.0
基于 v1.0 升级：手机响应式适配 · 用户登录保护 · 文件对比分析 · UI优化
"""

import streamlit as st
import os, io, re, json
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
#  页面配置
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind AI · 智能文档助手",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  全局CSS — 电脑保持原样，手机自动适配
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], p, div, span, label {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #f8f9fc !important; }

/* ── 电脑端布局（默认） ── */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px !important;
}

/* ══════════════════════════════════════════
   手机端适配（宽度 ≤ 768px 自动触发）
   电脑端完全不受影响
   ══════════════════════════════════════════ */
@media (max-width: 768px) {
    .main .block-container {
        padding: 0.5rem 0.4rem 2rem 0.4rem !important;
        max-width: 100% !important;
    }
    /* 品牌栏手机版缩小 */
    .brand-title { font-size: 1.1rem !important; }
    .brand-sub   { display: none !important; }
    .brand-bar   { padding: 12px 16px !important; border-radius: 10px !important; }
    /* 操作按钮手机版2列 */
    div[data-testid="column"] { min-width: 45% !important; }
    /* 侧边栏提示 */
    .mobile-key-hint { display: block !important; }
    .desktop-only    { display: none !important; }
    /* Tab文字缩小 */
    .stTabs [data-baseweb="tab"] {
        font-size: 0.75rem !important;
        padding: 6px 8px !important;
    }
    /* 文件上传区 */
    [data-testid="stFileUploader"] { padding: 4px !important; }
}

/* 手机提示条默认隐藏，只在手机显示 */
.mobile-key-hint { display: none; }

/* ── 品牌栏 ── */
.brand-bar {
    background: linear-gradient(135deg, #1a1f36 0%, #2d3561 100%);
    padding: 22px 32px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(26,31,54,0.2);
}
.brand-inner { display: flex; align-items: center; gap: 14px; }
.brand-logo  { font-size: 2.2rem; line-height: 1; }
.brand-title {
    font-size: 1.55rem; font-weight: 700;
    color: #ffffff !important; letter-spacing: -0.5px; margin: 0;
}
.brand-sub {
    font-size: 0.82rem; color: rgba(255,255,255,0.5) !important; margin: 3px 0 0 0;
}
.brand-badge {
    margin-left: auto;
    background: rgba(99,179,237,0.18); border: 1px solid rgba(99,179,237,0.35);
    color: #63b3ed !important; font-size: 0.72rem; font-weight: 700;
    padding: 4px 14px; border-radius: 20px; letter-spacing: 1px;
}

/* ── 侧边栏 ── */
[data-testid="stSidebar"] > div:first-child { background: #1a1f36 !important; }
[data-testid="stSidebar"] { background: #1a1f36 !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: rgba(255,255,255,0.88) !important; }
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox select {
    background: rgba(255,255,255,0.08) !important;
    color: white !important; border-color: rgba(255,255,255,0.15) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.1) !important;
    color: white !important; border: 1px solid rgba(255,255,255,0.2) !important;
}

/* ── 按钮 ── */
.stButton > button {
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.45rem 1rem !important;
    transition: all 0.18s !important;
}
.stButton > button[kind="primary"] {
    background: #4f6ef7 !important; border: none !important; color: white !important;
}
.stButton > button[kind="primary"]:hover {
    background: #3d5ce0 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(79,110,247,0.35) !important;
}
.stDownloadButton > button { border-radius: 10px !important; font-weight: 600 !important; }

/* ── Tab样式 ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px; background: transparent; border-bottom: 2px solid #e8eaf0;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important; font-weight: 500 !important;
    font-size: 0.9rem !important; padding: 8px 18px !important; color: #8892a4 !important;
}
.stTabs [aria-selected="true"] {
    color: #4f6ef7 !important; background: #f0f3ff !important;
    border-bottom: 2px solid #4f6ef7 !important;
}

/* ── 文件上传 ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #c8cfe0 !important;
    border-radius: 12px !important; background: #f8f9fc !important; padding: 8px !important;
}
[data-testid="stFileUploader"]:hover { border-color: #4f6ef7 !important; }

/* ── 卡片/信息框 ── */
.info-card {
    background: #f0f3ff; border: 1px solid #d0d8ff;
    border-left: 4px solid #4f6ef7; border-radius: 10px;
    padding: 12px 16px; font-size: 0.85rem; color: #2d3748;
    margin: 8px 0 12px 0; line-height: 1.6;
}
.warn-card {
    background: #fffbeb; border: 1px solid #fcd34d;
    border-left: 4px solid #f59e0b; border-radius: 10px;
    padding: 12px 16px; font-size: 0.85rem; color: #78350f;
    margin: 8px 0 12px 0; line-height: 1.6;
}

/* ── 文件chip ── */
.file-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: #f0f3ff; border: 1px solid #d0d8ff;
    border-radius: 8px; padding: 6px 12px; margin: 3px 0;
    font-size: 0.84rem; color: #1a1f36;
}

/* ── 搜索结果 ── */
.search-item {
    border-left: 3px solid #4f6ef7; padding: 10px 14px;
    margin-bottom: 10px; background: #f8f9fc;
    border-radius: 0 8px 8px 0; border: 1px solid #e8eaf0;
    border-left: 3px solid #4f6ef7;
}
.search-title { font-weight: 600; font-size: 0.9rem; color: #1a1f36; }
.search-url   { font-size: 0.75rem; color: #8892a4; margin: 3px 0; }
.search-snip  { font-size: 0.85rem; color: #4a5568; line-height: 1.55; }

/* ── 标签 ── */
.tag {
    display: inline-block; background: #eef0ff; color: #4f6ef7;
    font-size: 0.73rem; font-weight: 600; padding: 3px 10px;
    border-radius: 20px; margin-right: 6px;
}

/* ── 统计 ── */
.stat-box { text-align: center; padding: 12px 8px; }
.stat-number { font-size: 1.8rem; font-weight: 700; color: white !important; line-height: 1; }
.stat-label  { font-size: 0.75rem; color: rgba(255,255,255,0.5) !important; margin-top: 4px; font-weight: 500; }

/* ── 进度条 ── */
.stProgress > div > div { background: #4f6ef7 !important; border-radius: 4px !important; }

/* ── 登录页 ── */
.login-card {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 20px;
    padding: 40px 36px; box-shadow: 0 8px 40px rgba(79,110,247,0.12);
    max-width: 400px; margin: 60px auto 0;
}

/* ── 对比结果 ── */
.diff-section {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 16px 20px; margin: 8px 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  Session state
# ─────────────────────────────────────────────
def _init_state():
    defaults = {
        "api_key":       os.environ.get("DEEPSEEK_API_KEY", ""),
        "base_url":      os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "model":         "deepseek-v4-flash",
        "total_calls":   0,
        "total_tokens":  0,
        "history":       [],
        "web_enabled":   False,
        "bocha_key":     os.environ.get("BOCHA_KEY", ""),
        "tavily_key":    os.environ.get("TAVILY_KEY", ""),
        "network_mode":  "auto",
        "logged_in":     False,
        "username":      "",
        "chat_messages": [],
        "selected_op":   "📝 智能摘要",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─────────────────────────────────────────────
#  登录系统（可选，设置环境变量 DOCMIND_USERS 才启用）
# ─────────────────────────────────────────────
USERS_ENV  = os.environ.get("DOCMIND_USERS", "")
LOGIN_ON   = bool(USERS_ENV)
USERS      = json.loads(USERS_ENV) if USERS_ENV else {}

def render_login():
    st.markdown("""
    <div class='login-card'>
      <div style='text-align:center;margin-bottom:24px'>
        <div style='font-size:3rem'>🧠</div>
        <h2 style='color:#1e293b;margin:8px 0 4px;font-size:1.5rem;font-weight:700'>DocMind AI</h2>
        <p style='color:#94a3b8;font-size:0.85rem;margin:0'>智能文档处理平台</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.text_input("", placeholder="用户名", key="login_user", label_visibility="collapsed")
        st.text_input("", placeholder="密码", type="password", key="login_pass", label_visibility="collapsed")
        if st.button("登 录", use_container_width=True, type="primary"):
            u = st.session_state.login_user
            p = st.session_state.login_pass
            if u in USERS and USERS[u] == p:
                st.session_state.logged_in = True
                st.session_state.username  = u
                st.rerun()
            else:
                st.error("用户名或密码错误")
        st.markdown("<p style='text-align:center;color:#94a3b8;font-size:0.75rem;margin-top:12px'>演示账号：demo / demo123</p>",
                    unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  文件读取
# ─────────────────────────────────────────────
def read_uploaded(file) -> str:
    suffix = Path(file.name).suffix.lower()
    data   = file.read()
    try:
        if suffix == ".txt":
            return data.decode("utf-8", errors="replace")
        elif suffix == ".docx":
            import docx as _docx
            doc = _docx.Document(io.BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs)
        elif suffix in (".xlsx", ".xls"):
            import openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(data))
            lines = []
            for ws in wb.worksheets:
                lines.append(f"[Sheet: {ws.title}]")
                for row in ws.iter_rows(values_only=True):
                    lines.append("\t".join(str(c) if c is not None else "" for c in row))
            return "\n".join(lines)
        elif suffix == ".csv":
            return data.decode("utf-8", errors="replace")
        elif suffix == ".pdf":
            import pdfplumber
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        else:
            return data.decode("utf-8", errors="replace")
    except Exception as e:
        return f"[读取失败：{e}]"

# ─────────────────────────────────────────────
#  AI调用
# ─────────────────────────────────────────────
def call_ai(messages: list, stream=True):
    from openai import OpenAI
    import httpx
    client = OpenAI(
        api_key  = st.session_state.api_key,
        base_url = st.session_state.base_url,
        timeout  = httpx.Timeout(connect=10, read=120, write=30, pool=10),
    )
    kwargs = dict(
        model=st.session_state.model,
        messages=messages,
        max_tokens=3000,
        stream=stream,
    )
    if str(st.session_state.model).startswith("deepseek-v4"):
        kwargs["extra_body"] = {"thinking": {"type": "disabled"}}
    return client.chat.completions.create(**kwargs)

def stream_reply(messages, placeholder) -> str:
    full = ""
    for chunk in call_ai(messages, stream=True):
        delta = chunk.choices[0].delta.content or ""
        full += delta
        placeholder.markdown(clean_md(full) + "▌")
    placeholder.markdown(clean_md(full))
    st.session_state.total_calls  += 1
    st.session_state.total_tokens += len(full) // 3
    return full

# ─────────────────────────────────────────────
#  联网搜索
# ─────────────────────────────────────────────
def detect_env():
    mode = st.session_state.network_mode
    if mode != "auto":
        return mode
    import socket
    try:
        s = socket.create_connection(("www.google.com", 443), timeout=3)
        s.close(); return "global"
    except:
        return "china"

def web_search(query: str) -> list:
    env = detect_env()
    if env == "global":
        key = st.session_state.tavily_key
        if key:
            try:
                import httpx
                r = httpx.post("https://api.tavily.com/search",
                    json={"api_key": key, "query": query, "max_results": 5}, timeout=15)
                return [{"title":x.get("title",""),"url":x.get("url",""),
                         "content":x.get("content","")[:400],"engine":"Tavily"}
                        for x in r.json().get("results",[])]
            except: pass
        try:
            from duckduckgo_search import DDGS
            with DDGS() as d:
                return [{"title":r.get("title",""),"url":r.get("href",""),
                         "content":r.get("body","")[:400],"engine":"DuckDuckGo"}
                        for r in d.text(query, max_results=5)]
        except: pass
    else:
        key = st.session_state.bocha_key
        if key:
            try:
                import httpx
                r = httpx.post("https://api.bochaai.com/v1/web-search",
                    headers={"Authorization":f"Bearer {key}"},
                    json={"query":query,"count":5,"summary":True}, timeout=20)
                pages = r.json().get("data",{}).get("webPages",{}).get("value",[])
                return [{"title":p.get("name",""),"url":p.get("url",""),
                         "content":p.get("summary",p.get("snippet",""))[:400],"engine":"博查"}
                        for p in pages]
            except: pass
        try:
            import urllib.parse, urllib.request, html, re as _re
            url = f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&rn=8"
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                text = resp.read().decode("utf-8", errors="replace")
            results = []
            pat = _re.compile(r'<h3[^>]*>.*?<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', _re.DOTALL)
            for m in pat.finditer(text):
                title = _re.sub(r'<[^>]+>','', m.group(2))
                title = html.unescape(title).strip()
                href  = m.group(1)
                if title and len(title) > 3:
                    if href.startswith("/link"):
                        href = "https://www.baidu.com" + href
                    results.append({"title":title,"url":href,"content":"","engine":"百度"})
                if len(results) >= 5: break
            return results
        except: pass
    return []

# ─────────────────────────────────────────────
#  工具函数
# ─────────────────────────────────────────────
def clean_md(text: str) -> str:
    text = re.sub(r'```[^\n]*\n([\s\S]*?)```', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'\*{1,3}(.+?)\*{1,3}', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'^[-*+]\s+', '• ', text, flags=re.MULTILINE)
    text = re.sub(r'(?<!\w)[*#]+(?!\w)', '', text)
    return text.strip()

def to_docx_bytes(content: str, title: str = "AI处理结果") -> bytes:
    import docx as _docx
    from docx.shared import RGBColor
    doc = _docx.Document()
    h   = doc.add_heading(title, level=1)
    h.runs[0].font.color.rgb = RGBColor(0x4f, 0x6e, 0xf7)
    doc.add_paragraph(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    doc.add_paragraph("─" * 40)
    doc.add_paragraph(clean_md(content))
    buf = io.BytesIO(); doc.save(buf)
    return buf.getvalue()

def save_history(op, filename, result):
    st.session_state.history.insert(0, {
        "time": datetime.now().strftime("%H:%M"),
        "op": op, "file": filename, "result": result,
    })
    if len(st.session_state.history) > 50:
        st.session_state.history = st.session_state.history[:50]

# ─────────────────────────────────────────────
#  侧边栏（与v1保持一致，加退出登录）
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🧠 DocMind AI")
        if st.session_state.username:
            st.markdown(f"<small style='color:rgba(255,255,255,0.5)'>👤 {st.session_state.username}</small>",
                        unsafe_allow_html=True)
        else:
            st.markdown("<small style='color:rgba(255,255,255,0.4)'>智能文档处理平台</small>",
                        unsafe_allow_html=True)
        st.divider()

        st.markdown("**⚙️ API 配置**")
        api_key = st.text_input("API Key", value=st.session_state.api_key,
                                 type="password", placeholder="sk-...")
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key

        base_url = st.text_input("Base URL", value=st.session_state.base_url)
        if base_url != st.session_state.base_url:
            st.session_state.base_url = base_url

        model_options = ["deepseek-v4-flash", "deepseek-v4-pro", "deepseek-chat", "deepseek-reasoner", "gpt-4o-mini", "gpt-4o"]
        model = st.selectbox("模型", model_options,
                              index=model_options.index(st.session_state.model)
                              if st.session_state.model in model_options else 0)
        st.session_state.model = model

        if st.button("✅ 应用 API 配置", use_container_width=True):
            if st.session_state.api_key:
                os.environ["DEEPSEEK_API_KEY"] = st.session_state.api_key
                os.environ["DEEPSEEK_BASE_URL"] = st.session_state.base_url
                st.success("✅ 已应用，本次会话可以调用 AI")
            else:
                os.environ.pop("DEEPSEEK_API_KEY", None)
                st.warning("未填写 API Key")

        if st.button("🔌 测试连接", use_container_width=True):
            if not st.session_state.api_key:
                st.error("请先填写 API Key")
            else:
                with st.spinner("测试中..."):
                    try:
                        call_ai([{"role":"user","content":"hi"}], stream=False)
                        st.success("✅ 连接成功")
                    except Exception as e:
                        st.error(f"❌ {str(e)[:60]}")

        st.divider()
        st.markdown("**🌐 联网搜索**")
        st.session_state.web_enabled = st.toggle("启用联网搜索",
                                                   value=st.session_state.web_enabled)
        if st.session_state.web_enabled:
            mode = st.selectbox("网络模式", ["auto","china","global"],
                                 index=["auto","china","global"].index(st.session_state.network_mode))
            st.session_state.network_mode = mode
            st.session_state.bocha_key  = st.text_input("博查 Key（国内优先）",
                value=st.session_state.bocha_key, type="password", placeholder="可留空，自动用百度")
            st.session_state.tavily_key = st.text_input("Tavily Key（国外优先）",
                value=st.session_state.tavily_key, type="password", placeholder="可留空，自动用DuckDuckGo")

        st.divider()
        st.markdown("**📊 本次统计**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-number'>{st.session_state.total_calls}</div>
                <div class='stat-label'>调用次数</div></div>""", unsafe_allow_html=True)
        with col2:
            tok = st.session_state.total_tokens
            tok_str = f"{tok//1000}k" if tok >= 1000 else str(tok)
            st.markdown(f"""<div class='stat-box'>
                <div class='stat-number'>{tok_str}</div>
                <div class='stat-label'>Tokens</div></div>""", unsafe_allow_html=True)

        st.divider()
        # 手机端提示
        st.markdown("""
        <div class='mobile-key-hint' style='background:rgba(255,255,255,0.08);
             border-radius:8px;padding:10px 12px;font-size:0.78rem;
             color:rgba(255,255,255,0.7);line-height:1.5'>
          📱 手机用户：在此填入 API Key 后点击空白处确认，然后关闭侧边栏即可使用
        </div>""", unsafe_allow_html=True)

        if LOGIN_ON and st.session_state.logged_in:
            st.divider()
            if st.button("🚪 退出登录", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username  = ""
                st.rerun()

        st.markdown("<small style='color:rgba(255,255,255,0.3)'>DocMind AI v2.0 · Powered by DeepSeek</small>",
                    unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  主页面品牌栏 + Tabs
# ─────────────────────────────────────────────
def render_main():
    username = st.session_state.username
    badge    = f"👤 {username}" if username else "BETA"
    st.markdown(f"""
    <div class='brand-bar'>
      <div class='brand-inner'>
        <div class='brand-logo'>🧠</div>
        <div>
          <p class='brand-title'>DocMind AI</p>
          <p class='brand-sub'>智能文档处理平台 · AI-Powered Document Intelligence</p>
        </div>
        <div class='brand-badge'>{badge}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 手机端：未填Key时在主区域顶部显示提示
    if not st.session_state.api_key:
        st.markdown("""
        <div class='warn-card'>
          📱 <strong>手机用户：</strong>点击左上角 <strong>＞</strong> 展开侧边栏 → 填入 API Key → 关闭侧边栏即可使用<br>
          💻 <strong>电脑用户：</strong>在左侧侧边栏填入 API Key
        </div>
        """, unsafe_allow_html=True)

    tab_doc, tab_cmp, tab_chat, tab_search, tab_history = st.tabs(
        ["📄 文档处理", "🔍 文件对比", "💬 AI 对话", "🌐 联网搜索", "📋 历史记录"])

    with tab_doc:     render_doc_tab()
    with tab_cmp:     render_compare_tab()
    with tab_chat:    render_chat_tab()
    with tab_search:  render_search_tab()
    with tab_history: render_history_tab()

# ─────────────────────────────────────────────
#  Tab 1：文档处理（与v1保持一致）
# ─────────────────────────────────────────────
OPERATIONS = {
    "📝 智能摘要":     {"desc":"提取核心内容",  "prompt":"请对以下文件内容进行智能摘要，提取核心观点、关键数据和重要结论，输出结构化的摘要报告："},
    "🌐 翻译成英文":   {"desc":"中译英",        "prompt":"请将以下内容完整、准确地翻译为英文，保持原文逻辑和格式，专业术语准确翻译："},
    "🇨🇳 翻译成中文":  {"desc":"英译中",        "prompt":"请将以下内容完整、准确地翻译为中文，保持原文逻辑和格式，语言自然流畅："},
    "⚠️ 风险分析":    {"desc":"合同/报告风险",  "prompt":"请仔细阅读以下内容，识别并分析所有潜在风险点、不合理条款和需要注意的事项，按风险等级（高/中/低）逐条列出："},
    "🔑 关键信息提取": {"desc":"结构化提取",    "prompt":"请从以下内容中提取所有关键信息，包括：时间、人名/机构、金额、核心条款、重要数据等，用结构化方式输出："},
    "✍️ 改写润色":    {"desc":"专业风格",       "prompt":"请将以下内容改写成正式、专业的风格，优化表达，消除语病，使其更适合商业/公文场景："},
    "📊 数据分析":     {"desc":"Excel/CSV专用", "prompt":"你是数据分析专家，请分析以下数据：统计规律、关键指标、异常值、趋势和业务洞察，给出具体建议："},
    "💡 自定义":       {"desc":"自由输入指令",  "prompt":""},
}

def render_doc_tab():
    if not st.session_state.api_key:
        st.info("👈 请先在左侧侧边栏填入 API Key")
        return

    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown("#### 📁 上传文件")
        uploaded = st.file_uploader(
            "支持 PDF / Word / Excel / CSV / TXT",
            type=["pdf","docx","xlsx","xls","csv","txt"],
            accept_multiple_files=True, label_visibility="collapsed")

        if uploaded:
            for f in uploaded:
                size_kb = len(f.getvalue()) // 1024
                st.markdown(f"""
                <div class='file-chip'>📄 {f.name}
                  <span style='color:#8892a4;font-size:0.75rem'>{size_kb} KB</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("#### ⚡ 选择操作")
        op_keys     = list(OPERATIONS.keys())
        selected_op = st.session_state.get("selected_op", op_keys[0])
        cols        = st.columns(4)
        for i, op in enumerate(op_keys):
            with cols[i % 4]:
                if st.button(op, key=f"op_{i}", use_container_width=True,
                             type="primary" if op == selected_op else "secondary"):
                    st.session_state.selected_op = op
                    selected_op = op

        if selected_op == "💡 自定义":
            custom_prompt = st.text_area("自定义指令", height=80,
                                          placeholder="请描述你想让 AI 做什么...")
        else:
            custom_prompt = ""
            st.markdown(f"""<div class='info-card'>
              💡 {OPERATIONS[selected_op]['desc']} · {OPERATIONS[selected_op]['prompt'][:60]}...
            </div>""", unsafe_allow_html=True)

        extra_q     = st.text_input("➕ 追加要求（可选）", placeholder="例：重点关注第三方责任条款")
        run_clicked = st.button("▶  开始处理", type="primary",
                                 use_container_width=True, disabled=not uploaded)

    with col_right:
        st.markdown("#### 📊 处理结果")
        if run_clicked and uploaded:
            prompt_base = custom_prompt if selected_op == "💡 自定义" \
                         else OPERATIONS[selected_op]["prompt"]
            if extra_q:
                prompt_base += f"\n\n附加要求：{extra_q}"

            all_results = []
            progress    = st.progress(0, text="准备中...")

            for idx, f in enumerate(uploaded):
                progress.progress(idx / len(uploaded),
                                   text=f"处理 {idx+1}/{len(uploaded)}：{f.name}")
                f.seek(0)
                content = read_uploaded(f)
                if len(content) > 10000:
                    content = content[:10000] + "\n...[内容已截断]"

                search_ctx = ""
                if st.session_state.web_enabled:
                    with st.spinner("🌐 联网搜索相关信息..."):
                        results = web_search(f.name + " " + prompt_base[:30])
                        if results:
                            search_ctx = "\n\n参考网络信息：\n" + \
                                "\n".join(f"- {r['title']}: {r['content'][:200]}" for r in results[:3])

                messages = [
                    {"role":"system","content":"你是专业的文档分析助手，擅长处理商业文件、合同、报告和数据表格。输出内容清晰、结构化、专业。不要使用过多Markdown符号。"},
                    {"role":"user","content":f"{prompt_base}\n\n---文件：{f.name}---\n{content}{search_ctx}"}
                ]

                st.markdown(f"**📄 {f.name}**")
                ph = st.empty()
                try:
                    full = stream_reply(messages, ph)
                    all_results.append({"file": f.name, "result": full})
                    save_history(selected_op, f.name, full)
                except Exception as e:
                    st.error(f"❌ 处理 {f.name} 失败：{e}")

            progress.progress(1.0, text="✅ 全部完成！")

            if all_results:
                st.divider()
                combined = "\n\n".join(f"=== {r['file']} ===\n{clean_md(r['result'])}"
                                       for r in all_results)
                dc1, dc2, dc3 = st.columns(3)
                with dc1:
                    st.download_button("⬇️ 下载 TXT", data=combined.encode("utf-8"),
                        file_name=f"DocMind_{datetime.now().strftime('%m%d_%H%M')}.txt",
                        mime="text/plain", use_container_width=True)
                with dc2:
                    try:
                        st.download_button("⬇️ 下载 Word", data=to_docx_bytes(combined, selected_op),
                            file_name=f"DocMind_{datetime.now().strftime('%m%d_%H%M')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True)
                    except: pass
                with dc3:
                    if len(all_results) > 1:
                        try:
                            import openpyxl
                            from openpyxl.styles import Font, PatternFill, Alignment
                            wb = openpyxl.Workbook(); ws = wb.active; ws.title = "AI处理汇总"
                            for ci, h in enumerate(["文件名","操作","处理结果"],1):
                                c = ws.cell(row=1,column=ci,value=h)
                                c.font = Font(bold=True, color="FFFFFF")
                                c.fill = PatternFill("solid", fgColor="4F6EF7")
                                c.alignment = Alignment(horizontal="center")
                            for ri, r in enumerate(all_results,2):
                                ws.cell(row=ri,column=1,value=r["file"])
                                ws.cell(row=ri,column=2,value=selected_op)
                                ws.cell(row=ri,column=3,value=clean_md(r["result"]))
                            ws.column_dimensions["A"].width = 30
                            ws.column_dimensions["B"].width = 20
                            ws.column_dimensions["C"].width = 80
                            buf = io.BytesIO(); wb.save(buf)
                            st.download_button("⬇️ 下载 Excel 汇总", data=buf.getvalue(),
                                file_name=f"DocMind_汇总_{datetime.now().strftime('%m%d_%H%M')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True)
                        except: pass

# ─────────────────────────────────────────────
#  Tab 2：文件对比分析（新增）
# ─────────────────────────────────────────────
def render_compare_tab():
    if not st.session_state.api_key:
        st.info("👈 请先在左侧侧边栏填入 API Key")
        return

    st.markdown("""<div class='info-card'>
      📌 上传两份文件，AI 自动识别差异、新增/删除条款、重要变更。适合合同版本对比、报告修订对比、数据前后对比等场景。
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("**📄 文件 A（原版）**")
        file_a = st.file_uploader("文件A", type=["pdf","docx","xlsx","csv","txt"],
                                   label_visibility="collapsed", key="cmp_a")
        if file_a:
            st.markdown(f"<div class='file-chip'>✅ {file_a.name}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("**📄 文件 B（新版）**")
        file_b = st.file_uploader("文件B", type=["pdf","docx","xlsx","csv","txt"],
                                   label_visibility="collapsed", key="cmp_b")
        if file_b:
            st.markdown(f"<div class='file-chip'>✅ {file_b.name}</div>", unsafe_allow_html=True)

    cmp_mode = st.selectbox("对比维度", [
        "全面对比（找出所有差异）",
        "条款变更（合同专用）",
        "数据变化（Excel/报表专用）",
        "风险变化（新增/消除的风险点）",
    ])
    focus = st.text_input("重点关注（可选）", placeholder="例：付款条款、违约责任、截止日期")

    if st.button("🔍 开始对比分析", type="primary", disabled=not (file_a and file_b)):
        file_a.seek(0); file_b.seek(0)
        content_a = read_uploaded(file_a)[:6000]
        content_b = read_uploaded(file_b)[:6000]

        prompt = f"""你是专业文档对比分析师。请对以下两份文件进行{cmp_mode}。
{"重点关注：" + focus if focus else ""}

请按以下结构输出（不要使用Markdown符号）：
1. 总体变化摘要（3-5句）
2. 主要新增内容（B有A没有）
3. 主要删除内容（A有B删除）
4. 重要修改内容（表述有变化）
5. 风险提示（需要注意的重要变化）

---文件A：{file_a.name}---
{content_a}

---文件B：{file_b.name}---
{content_b}"""

        messages = [
            {"role":"system","content":"你是专业文档对比分析师，分析准确、结构清晰，善于识别合同、报告的关键变化。"},
            {"role":"user","content":prompt}
        ]

        st.divider()
        st.markdown(f"**🔍 对比结果：`{file_a.name}` vs `{file_b.name}`**")
        ph = st.empty()
        try:
            full = stream_reply(messages, ph)
            save_history(f"对比分析", f"{file_a.name} vs {file_b.name}", full)
            st.divider()
            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button("⬇️ 下载对比报告 TXT",
                    data=clean_md(full).encode("utf-8"),
                    file_name=f"对比分析_{datetime.now().strftime('%m%d_%H%M')}.txt",
                    mime="text/plain", use_container_width=True)
            with dl2:
                try:
                    st.download_button("⬇️ 下载对比报告 Word",
                        data=to_docx_bytes(full, f"文件对比：{file_a.name} vs {file_b.name}"),
                        file_name=f"对比分析_{datetime.now().strftime('%m%d_%H%M')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True)
                except: pass
        except Exception as e:
            st.error(f"❌ 对比失败：{e}")

# ─────────────────────────────────────────────
#  Tab 3：AI 对话（与v1保持一致）
# ─────────────────────────────────────────────
def render_chat_tab():
    if not st.session_state.api_key:
        st.info("👈 请先在左侧侧边栏填入 API Key")
        return

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"]=="user" else "🧠"):
            st.markdown(clean_md(msg["content"]))

    if prompt := st.chat_input("输入你的问题，或者粘贴文字让 AI 分析..."):
        st.session_state.chat_messages.append({"role":"user","content":prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🧠"):
            ph = st.empty()
            search_ctx = ""
            if st.session_state.web_enabled:
                with st.spinner("🌐 搜索中..."):
                    results = web_search(prompt)
                    if results:
                        search_ctx = "\n\n参考网络最新信息：\n" + \
                            "\n".join(f"[{r['engine']}] {r['title']}: {r['content'][:200]}"
                                      for r in results[:4])
            messages = [
                {"role":"system","content":"你是专业智能助手，回答清晰、简洁、有条理。不要使用过多Markdown符号。"},
            ] + st.session_state.chat_messages[:-1] + [
                {"role":"user","content": prompt + search_ctx}
            ]
            try:
                full = stream_reply(messages, ph)
                st.session_state.chat_messages.append({"role":"assistant","content":full})
            except Exception as e:
                st.error(f"❌ {e}")

    if st.session_state.chat_messages:
        if st.button("🗑️ 清空对话", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

# ─────────────────────────────────────────────
#  Tab 4：联网搜索（与v1保持一致）
# ─────────────────────────────────────────────
def render_search_tab():
    st.markdown("#### 🌐 联网搜索")
    st.markdown("<small style='color:#8892a4'>自动检测网络环境：国内用博查/百度，国外用Tavily/DuckDuckGo</small>",
                unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("搜索关键词", placeholder="输入要搜索的内容...", label_visibility="collapsed")
    with col2:
        search_btn = st.button("🔍 搜索", use_container_width=True, type="primary")

    if search_btn and query:
        with st.spinner("搜索中..."):
            results = web_search(query)
        if results:
            engine = results[0].get("engine","")
            st.markdown(f"<span class='tag'>引擎：{engine}</span>"
                        f"<span class='tag'>找到 {len(results)} 条结果</span>",
                        unsafe_allow_html=True)
            for r in results:
                st.markdown(f"""<div class='search-item'>
                  <div class='search-title'>{r['title']}</div>
                  <div class='search-url'>{r['url'][:80]}</div>
                  <div class='search-snip'>{r['content'] or '暂无摘要'}</div>
                </div>""", unsafe_allow_html=True)
            if st.session_state.api_key:
                if st.button("🧠 让 AI 综合分析这些结果"):
                    ctx = "\n".join(f"[{r['title']}] {r['content']}" for r in results)
                    with st.spinner("AI 分析中..."):
                        try:
                            resp = call_ai([
                                {"role":"system","content":"你是信息综合分析专家"},
                                {"role":"user","content":f"请综合以下搜索结果，回答问题「{query}」，给出清晰的分析结论：\n\n{ctx}"}
                            ], stream=False)
                            st.markdown("**AI 综合分析：**")
                            st.markdown(clean_md(resp.choices[0].message.content))
                        except Exception as e:
                            st.error(str(e))
        else:
            st.warning("未找到结果，请检查网络或更换关键词")

# ─────────────────────────────────────────────
#  Tab 5：历史记录（与v1保持一致）
# ─────────────────────────────────────────────
def render_history_tab():
    st.markdown("#### 📋 处理历史")
    if not st.session_state.history:
        st.info("暂无处理记录，处理文件后会自动记录在这里")
        return
    for i, h in enumerate(st.session_state.history[:20]):
        with st.expander(f"[{h['time']}] {h['op']} · {h['file']}", expanded=(i==0)):
            st.markdown(clean_md(h["result"]))
            st.download_button("⬇️ 下载", data=clean_md(h["result"]).encode("utf-8"),
                                file_name=f"{h['file']}_AI结果.txt",
                                key=f"dl_h_{i}", mime="text/plain")
    if st.button("🗑️ 清空历史"):
        st.session_state.history = []
        st.rerun()

# ─────────────────────────────────────────────
#  主入口
# ─────────────────────────────────────────────
if LOGIN_ON and not st.session_state.logged_in:
    render_login()
    st.stop()

render_sidebar()
render_main()