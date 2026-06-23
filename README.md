# 🔬 ResearchMind

**ResearchMind** is a multi-agent AI research assistant built with [LangChain](https://www.langchain.com/) / [LangGraph](https://www.langchain.com/langgraph) and [Streamlit](https://streamlit.io/). Give it a topic, and four specialized agents work together — searching the web, scraping deeper content, drafting a report, and critiquing the result — to produce a polished, ready-to-download research report.

---

## ✨ Features

- **Multi-agent pipeline** — four distinct agents/chains run in sequence, each with a clear responsibility
- **Live pipeline visualization** — see each agent's status (waiting / running / done) update in real time
- **Polished UI** — custom dark, glassmorphic Streamlit theme with smooth animations
- **Markdown report rendering** — the final report and critic feedback render as native, styled markdown
- **One-click download** — export the generated report as a `.md` file
- **Raw output inspection** — expandable panels show the raw search and scraping results for transparency

---

## 🧠 How It Works

ResearchMind runs a four-stage pipeline for every topic you submit:

| Step | Agent / Chain | Responsibility |
|------|----------------|-----------------|
| 01 | **Search Agent** | Searches the web for recent, reliable information about the topic |
| 02 | **Reader Agent** | Picks the most relevant result and scrapes it for deeper, detailed content |
| 03 | **Writer Chain** | Synthesizes the search + scraped content into a full research report |
| 04 | **Critic Chain** | Reviews the report and provides structured feedback/scoring |

Each step's output is passed as context into the next, so the final report is grounded in real, freshly retrieved information rather than the model's parametric memory alone.

---

## 📁 Project Structure

```
.
├── app.py          # Streamlit UI — layout, styling, and pipeline orchestration
├── agents.py       # Agent/chain definitions (search agent, reader agent, writer chain, critic chain)
└── README.md       # You are here
```

### `app.py`
Handles the entire user-facing experience:
- Custom CSS theming (fonts, colors, animations, panels)
- Topic input and pipeline trigger
- Step-by-step pipeline status cards
- Rendering of final report, critic feedback, and raw intermediate outputs
- Markdown download button

### `agents.py`
Expected to expose:
- `build_search_agent()` — returns a LangChain/LangGraph agent capable of web search
- `build_reader_agent()` — returns an agent capable of fetching and parsing a URL's content
- `writer_chain` — a chain that drafts the report from combined research context
- `critic_chain` — a chain that reviews and scores the drafted report

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Install dependencies
```bash
pip install streamlit langchain langgraph langchain-openai
```
> Adjust this list based on the actual imports/providers used inside `agents.py` (e.g. if you're using Anthropic, Tavily, or another search/LLM provider, install those packages too).

### 3. Set up environment variables
Create a `.env` file (or export variables in your shell) with the API keys required by your agents, for example:
```bash
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🖥️ Usage

1. Enter a research topic in the **Research Topic** field (e.g. *"Quantum computing breakthroughs in 2025"*).
2. Click **⚡ Run Research Pipeline**.
3. Watch the pipeline panel update as each agent completes its step.
4. Review the **Final Research Report** and **Critic Feedback** once the run finishes.
5. Optionally expand the raw **Search Results** and **Scraped Content** panels to see what the agents found.
6. Download the final report as a Markdown file using the **⬇ Download Report (.md)** button.

---

## 🎨 Tech Stack

- **Streamlit** — UI framework
- **LangChain / LangGraph** — agent orchestration
- **Custom CSS** — Syne, DM Sans, and DM Mono fonts with a dark, gradient-accented theme

---

## 🛠️ Customization

- **Styling** — all UI styling lives in the `st.markdown(...)` CSS block at the top of `app.py`; colors, fonts, and animations can be tweaked there.
- **Pipeline steps** — to add, remove, or reorder agents, update both the `agents.py` definitions and the `step_card(...)` calls / pipeline execution block in `app.py`.
- **Example topics** — the suggested topic chips can be edited in the `examples` list inside `app.py`.

---

## 📄 License

Add your preferred license here (e.g. MIT, Apache 2.0).

---

## 🙌 Acknowledgements

Built with LangChain's multi-agent tooling and Streamlit's rapid app framework.
