# AlphaLens // Quantitative Financial Sentiment Engine

AlphaLens is an autonomous equity research copilot designed to analyze corporate earnings calls and quarterly filings. Built with NVIDIA Nemotron open models, it extracts quantitative sentiment indices, management forward guidance nuance, expansion catalysts, and operational risks inside a high-contrast minimalist Vengeance terminal UI.

---

## ⚡ Key Capabilities
- **Quantitative Stance Index**: Computes directional sentiment scores (-1.00 to +1.00) alongside Bullish, Neutral, or Bearish classification.
- **Vengeance Terminal UI**: Minimalist, tri-pane dark architecture with live telemetry, table-of-contents tracking, and clean contrast cards.
- **Multimodal Filing Ingestion**: Supports direct commentary/transcript pasting as well as quarterly PDF financial filing extraction.
- **Powered by NVIDIA**: Utilizes `nvidia/nemotron-3-super-120b-a12b` via NVIDIA Build infrastructure for fast, structured equity analysis.

---

## 🛠️ Tech Stack
- **Framework**: Streamlit
- **LLM / Inference**: NVIDIA Nemotron-3 Super 120B (via OpenAI-compatible NVIDIA API)
- **Document Processing**: PyPDF
- **Styling**: Custom CSS (Vengeance minimalist terminal design)
- **Language**: Python 3.10+

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/whelve-13/alphalens-sentiment-engine.git](https://github.com/whelve-13/alphalens-sentiment-engine.git)
cd alphalens-sentiment-engine
