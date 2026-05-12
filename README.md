# AI Blog Agent
 
A multi-agent system that drafts blog posts grounded in my own notes - using Google ADK for orchestration, OpenAI GPT-4o-mini as the model, and LlamaIndex for retrieval over a personal corpus.
 
## Why I built this
 
I write occasionally, and the bottleneck is never generating sentences - LLMs already do that, badly. The bottleneck is the work *around* the writing: pulling together a structure, remembering what I've already thought about a topic, and keeping the voice consistent with how I'd actually write.
 
I wanted to see how far I could get by treating that as an agent orchestration problem rather than a prompting problem. Instead of one big "write me a blog post" call, the system splits the work across three agents - a planner, a writer, and an editor - and gives them tools (web search + retrieval over my own notes) so the drafts aren't generic LLM filler.
 
It's also the project I used to learn Google's Agent Development Kit hands-on, which turned out to be the most interesting and most painful part. Notes on what worked and what didn't are in [WRITEUP.md](./WRITEUP.md).
 
## How it works
 
```
User prompt
   |
Web search (DuckDuckGo) + RAG retrieval (LlamaIndex)
   |
Planner -> outline
   |
Writer  -> draft
   |
Editor  -> refined draft
```
 
- **Planner** turns a topic into a structured outline using retrieved context.
- **Writer** drafts each section against the outline.
- **Editor** passes over the draft for clarity, structure, and voice.
The `internal-data/` folder holds the personal notes that the RAG layer indexes - that's what keeps drafts in my voice instead of a generic one.
 
## Stack
 
| Component     | Choice                              |
| ------------- | ----------------------------------- |
| Orchestration | Google ADK                          |
| LLM           | OpenAI GPT-4o-mini (via LiteLLM)    |
| RAG           | LlamaIndex + OpenAI embeddings      |
| Web search    | DuckDuckGo                          |
| Runtime       | Python 3.12, `uv` for dependencies  |
 
## Running it locally
 
```bash
# Install dependencies
uv sync
 
# Set your OpenAI API key
export OPENAI_API_KEY=sk-...
 
# Run the agent
uv run python -m blog_writer
```
 
Drop your own notes as `.md` or `.txt` files into `internal-data/` to ground the drafts in your own writing.
 
## Read more
 
- [WRITEUP.md](./WRITEUP.md) - design decisions, tradeoffs, what broke, and what I'd do differently.
 