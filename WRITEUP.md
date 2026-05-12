# AI Blog Agent - Build Notes

A short build log on a side project: a multi-agent system that drafts blog posts grounded in my own notes, using Google's Agent Development Kit (ADK) for orchestration and OpenAI's GPT-4o-mini as the underlying model.

Repo layout: `blog-writer/` for the agent code, `internal-data/` for the personal notes the RAG layer reads from.

## What I wanted

The annoying part of writing for me isn't generating sentences - generic LLM output already does that, badly. The annoying part is:

1. Pulling together the structure for a post.
2. Remembering things I've already thought or written about a topic in older notes.
3. Keeping the voice consistent with what I'd actually write.

So the goal wasn't "AI writes blog posts." It was: take a topic, search the web for anything new I should know, ground the draft in my own prior notes, and hand me a first draft I can edit - not a generic SEO piece I'd throw away.

## How it's wired - Architecture

The system is a small set of cooperating agents orchestrated by ADK rather than one big prompt. The intended flow:

```
User prompt
   |
Web search (DuckDuckGo) + RAG retrieval (LlamaIndex over internal-data/)
   |
Planner  -> outline
   |
Writer   -> draft
   |
Editor   -> refined draft
```

- **Planner** - turns the topic + retrieved context into a structured outline.
- **Writer** - drafts each section against the outline.
- **Editor** - passes over the draft for clarity, structure, and voice.

All three agents call OpenAI's `gpt-4o-mini` through `litellm`, so the underlying model can be swapped without rewriting agent code. RAG is built with `llama-index` using OpenAI embeddings over the `internal-data/` corpus.

| Component     | Choice                                  |
| ------------- | --------------------------------------- |
| Orchestration | Google ADK                              |
| LLM           | OpenAI GPT-4o-mini (via LiteLLM)        |
| RAG           | LlamaIndex + OpenAI embeddings          |
| Web search    | DuckDuckGo                              |
| Runtime       | Python 3.12, `uv` for dependencies      |

## Key decisions
 
**1. ADK over LangGraph / CrewAI:** Wanted to learn its multi-agent abstractions. Tradeoff: smaller community, less mature than LangChain.
 
**2. GPT-4o-mini, not Gemini:** Roughly an order of magnitude cheaper than full 4o and fast enough for the loop. Weaker reasoning, and - as it turned out - the source of the main pain point below.
 
**3. Pairing ADK with OpenAI:** ADK is built first-class for Gemini. Tool-calling and agent handoffs through LiteLLM are noticeably less reliable than I'd expect natively. Right call for learning, wrong call for reliability.
 
**4. LiteLLM wrapper:** One extra dependency in exchange for swappable models - flip OpenAI to Anthropic to a local model with a string change.
 
**5. DuckDuckGo for search:** No API key. Trades reliability and result quality for zero setup. I'd swap to Tavily the moment this stops being a personal toy.
 
**6. LlamaIndex RAG over context-stuffing:** Overkill for my current corpus size, but I wanted hands-on practice with chunking + embeddings, and it stops scaling with the corpus.
 
**7. Multi-agent over single-agent-with-multi-prompts:** A single agent doing everything in one loop conflates planning and drafting. Separating them costs more LLM calls but produces noticeably more coherent outlines.
 
## What broke
 
- **Agent handoffs were unreliable:** The writer agent often didn't auto-trigger after the planner finished. The flow only completed cleanly when I steered it with explicit prompts at each step. Lesson: agents need explicit orchestration, not just well-written prompts.
- **Tool compatibility varies by LLM:** Tool-calling that works for one provider misbehaves on another, even through LiteLLM. ADK's tool layer is clearly tuned for Gemini.
- **Orchestration is harder than prompting:** I expected prompt engineering to be the main work. It wasn't - getting agents to reliably pass control and context between each other was.
- **RAG mattered more than I expected:** Even with a small `internal-data/` corpus, retrieval-grounded drafts read noticeably less like generic LLM filler.

## What I'd change
 
1. **Make the workflow deterministic:** Wire planner -> writer -> editor as an explicit pipeline in code instead of relying on framework orchestration. Less "agentic," more reliable.
2. **Try Gemini for the agent layer:** Pair the framework with the model it's built for and see whether the handoff issues disappear.
3. **Build a small eval harness:** Ten fixed topics scored on factuality, structure, and voice match - currently I judge output by reading it.
4. **Structured Pydantic outputs at every handoff:** Make broken outlines fail loudly instead of silently.
5. **Capture my own edits as a feedback signal:** The diff between agent draft and my final version is the most useful signal for the next iteration - right now it just disappears.

## Stack

Python 3.12, Google ADK, OpenAI GPT-4o-mini via `litellm`, LlamaIndex + OpenAI embeddings for RAG, DuckDuckGo for web search, `uv` for dependency management.
