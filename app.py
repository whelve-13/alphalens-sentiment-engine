import json
import re
from openai import OpenAI
from pypdf import PdfReader
import streamlit as st

# Configure full-width page layout
st.set_page_config(
    page_title="AlphaLens // Vengeance Terminal",
    layout="wide",
    page_icon="📐",
    initial_sidebar_state="expanded",
)

# Vengeance UI Dark Theme Styling
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

    /* Global canvas */
    .stApp {
        background-color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
        color: #ededed !important;
    }

    /* Left Sidebar navigation styling */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a !important;
        border-right: 1px solid #1f1f1f !important;
    }
    
    .nav-header {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        color: #707070;
        letter-spacing: 0.08em;
        margin: 18px 0 8px 0;
    }

    .nav-item {
        display: block;
        padding: 6px 10px;
        border-radius: 6px;
        color: #a1a1a1;
        font-size: 13px;
        text-decoration: none;
        margin-bottom: 2px;
        background: transparent;
        transition: all 0.15s ease;
    }
    .nav-item.active {
        background-color: #1a1a1a;
        color: #ffffff;
        font-weight: 500;
        border-left: 2px solid #ffffff;
    }

    /* Input areas */
    .stTextArea textarea {
        background-color: #0a0a0a !important;
        border: 1px solid #262626 !important;
        border-radius: 8px !important;
        color: #ededed !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
    }
    .stTextArea textarea:focus {
        border-color: #525252 !important;
        box-shadow: 0 0 0 1px #525252 !important;
    }

    /* Action Buttons */
    .stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: -0.01em !important;
        padding: 0.55rem 1rem !important;
        transition: opacity 0.2s ease !important;
    }
    .stButton > button:hover {
        opacity: 0.85 !important;
    }

    /* Cards & Containers */
    .vengeance-card {
        background: #0a0a0a;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .badge-tag {
        display: inline-block;
        background: #171717;
        color: #a3a3a3;
        font-size: 11px;
        font-family: 'JetBrains Mono', monospace;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #262626;
        margin-right: 6px;
    }

    /* Table of contents column */
    .toc-title {
        font-size: 11px;
        font-weight: 600;
        color: #737373;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 12px;
    }
    .toc-link {
        font-size: 12px;
        color: #a3a3a3;
        margin-bottom: 8px;
        padding-left: 8px;
        border-left: 1px solid #262626;
    }
    .toc-link.active {
        color: #ffffff;
        border-left: 1px solid #ffffff;
        font-weight: 500;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------- SIDEBAR (LEFT PANE) -----------------
with st.sidebar:
  st.markdown("### 📐 Vengeance // AlphaLens")
  api_key = st.text_input(
      "NVIDIA API Key", value="", type="password"
  )
  model_name = "nvidia/nemotron-3-super-120b-a12b"

  st.markdown('<div class="nav-header">Workspace</div>', unsafe_allow_html=True)
  st.markdown(
      '<div class="nav-item active">● Sentiment Analyzer</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="nav-item">○ SEC Edgar Pipeline</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="nav-item">○ Multi-Quarter Compare</div>',
      unsafe_allow_html=True,
  )

  st.markdown('<div class="nav-header">Filing Data</div>', unsafe_allow_html=True)
  st.markdown(
      '<div class="nav-item">10-K Annual Reports</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="nav-item">10-Q Earnings Transcripts</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="nav-item">Guidance Revisions</div>', unsafe_allow_html=True
  )

# ----------------- MAIN LAYOUT: CENTER & RIGHT PANES -----------------
center_col, right_col = st.columns([2.6, 1.1])

with center_col:
  # Title / Breadcrumbs
  st.markdown(
      '<span class="badge-tag">ENGINE: NEMOTRON-3</span><span'
      ' class="badge-tag">DOCS LAYOUT</span>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "# Sentiment & Earnings Radar\n"
      "Synthesize forward guidance nuance, catalysts, and underlying balance"
      " sheet friction."
  )
  st.caption("AlphaLens Copilot • 1 min read • Built on NVIDIA Open Models")

  st.markdown("---")

  input_method = st.radio(
      "Select Ingestion Pipeline:",
      ["Raw Transcript / Commentary", "Upload Filing (PDF)"],
      horizontal=True,
  )

  raw_text = ""
  if input_method == "Raw Transcript / Commentary":
    raw_text = st.text_area(
        "Financial transcript segment:",
        height=220,
        placeholder="Paste management remarks, analyst Q&A notes, or earnings guidance...",
    )
  else:
    uploaded_file = st.file_uploader("Filing PDF", type=["pdf"])
    if uploaded_file:
      reader = PdfReader(uploaded_file)
      for page in reader.pages[:6]:
        raw_text += (page.extract_text() or "") + "\n"
      st.success(f"Parsed {len(raw_text)} characters.")

  execute = st.button("RUN INTELLIGENCE ANALYSIS")

  if execute:
    if not api_key:
      st.error("Provide a valid API key in the configuration panel.")
    elif not raw_text.strip():
      st.warning("Please supply financial text to parse.")
    else:
      with st.spinner("Processing vectors via NVIDIA Nemotron..."):
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1", api_key=api_key
        )

        prompt = f"""
You are a quantitative equity research analyst. Analyze this financial text and return strictly valid JSON:
{{
  "sentiment_score": 0.58,
  "market_sentiment": "Bullish",
  "confidence_rating": "High",
  "executive_summary": "Two sentences summarizing key operational trajectory and outlook.",
  "catalysts": ["catalyst 1", "catalyst 2"],
  "risk_factors": ["risk factor 1", "risk factor 2"]
}}

Return ONLY raw JSON without markdown formatting.

Text:
{raw_text[:3500]}
"""
        try:
          response = client.chat.completions.create(
              model=model_name,
              messages=[
                  {
                      "role": "system",
                      "content": "You are a quantitative telemetry generator.",
                  },
                  {"role": "user", "content": prompt},
              ],
              temperature=0.1,
              max_tokens=1500,
          )

          msg = response.choices[0].message
          raw_output = msg.content or getattr(msg, "reasoning_content", "")

          start_idx = raw_output.find("{")
          end_idx = raw_output.rfind("}")
          clean_str = (
              raw_output[start_idx : end_idx + 1]
              if start_idx != -1 and end_idx != -1
              else raw_output
          )
          clean_str = re.sub(r"[\r\n\t]+", " ", clean_str)
          data = json.loads(clean_str)

          # Store in session state for right pane reactivity
          st.session_state["analysis_data"] = data

        except Exception as e:
          st.error(f"Inference error: {e}")

  # Display center report cards if data exists
  if "analysis_data" in st.session_state:
    data = st.session_state["analysis_data"]

    st.markdown("### Executive Summary")
    st.markdown(
        f'<div class="vengeance-card">{data.get("executive_summary", "")}</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
      st.markdown("### Growth Drivers")
      for cat in data.get("catalysts", []):
        st.markdown(
            f'<div class="vengeance-card" style="border-left: 2px solid'
            f' #22c55e;">+ {cat}</div>',
            unsafe_allow_html=True,
        )
    with c2:
      st.markdown("### Risk Headwinds")
      for risk in data.get("risk_factors", []):
        st.markdown(
            f'<div class="vengeance-card" style="border-left: 2px solid'
            f' #ef4444;">- {risk}</div>',
            unsafe_allow_html=True,
        )

# ----------------- RIGHT PANE (TOC & TELEMETRY) -----------------
with right_col:
  st.markdown('<div class="toc-title">ON THIS REPORT</div>', unsafe_allow_html=True)
  st.markdown(
      '<div class="toc-link active">Overview & Input</div>', unsafe_allow_html=True
  )
  st.markdown(
      '<div class="toc-link">Executive Summary</div>', unsafe_allow_html=True
  )
  st.markdown('<div class="toc-link">Growth Drivers</div>', unsafe_allow_html=True)
  st.markdown('<div class="toc-link">Risk Headwinds</div>', unsafe_allow_html=True)

  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      '<div class="toc-title">LIVE TELEMETRY</div>', unsafe_allow_html=True
  )

  if "analysis_data" in st.session_state:
    data = st.session_state["analysis_data"]
    score = float(data.get("sentiment_score", 0.0))
    stance = data.get("market_sentiment", "Neutral")
    confidence = data.get("confidence_rating", "Medium")

    st.markdown(
        f"""
        <div class="vengeance-card">
            <div style="font-size:11px; color:#737373;">SENTIMENT INDEX</div>
            <div style="font-size:24px; font-weight:700; color:#ffffff; font-family:'JetBrains Mono';">{score:+.2f}</div>
            <div style="font-size:11px; color:#737373; margin-top:8px;">STANCE BIAS</div>
            <div style="font-size:15px; font-weight:600; color:{'#22c55e' if 'bull' in stance.lower() else '#ef4444'};">{stance.upper()}</div>
            <div style="font-size:11px; color:#737373; margin-top:8px;">CONFIDENCE</div>
            <div style="font-size:13px; color:#ededed;">{confidence}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """
        <div class="vengeance-card" style="color: #737373; font-size: 12px;">
            Awaiting transcript ingestion...
        </div>
        """,
        unsafe_allow_html=True,
    )
