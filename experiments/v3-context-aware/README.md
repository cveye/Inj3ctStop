# v3 — Context-Aware Injection Detection

**Why this matters:** most prompt filters are stateless. When your app keeps chat history, attackers can use *late injections* (e.g., “ignore previous instructions”) that only make sense **relative to context**.

## What’s new
- **Session memory** (last N turns)
- **Context guard**: compares the new prompt vs. the conversation history using MiniLM embeddings and simple override heuristics
- **Demo UI** with “Enable memory 🧠” + visible history

## Run
```bash
make install
make run
# open http://localhost:8080/demo