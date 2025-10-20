# Inj3ctStop — Next-Gen LLM Safety Stack

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-live-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blueviolet.svg)](https://github.com/cveye/Inj3ctStop/pulls)
[![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)](#)
[![GitHub stars](https://img.shields.io/github/stars/cveye/Inj3ctStop?style=social)](https://github.com/cveye/Inj3ctStop/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/cveye/Inj3ctStop/main)](https://github.com/cveye/Inj3ctStop/commits/main)

---

**Stop prompt injections. Ship safer LLM apps.**

Inj3ctStop is a lightweight, defensive playground for experimenting with **prompt injection attacks** and **layered mitigation patterns**.  
The goal: build a **“next-gen LLM safety stack”** through iterative experiments.

All experiments use **simulated inputs** for learning and research. This repo is educational and defensive only — it does **not** contain real jailbreak payloads.

---

## 📚 Experiments

[![What's New](https://img.shields.io/badge/What's%20New-v4%20--%20Signature--Heurestics%20Proactive%20Defense-brightgreen.svg)](https://github.com/cveye/Inj3ctStop/tree/main/experiments/v4-signature-heuristic)

### 🔹 v1 — Simple Filters & Scoped Prompts
- Shows why naive wrappers and regex sanitization fail 🚨
- Demonstrates how **scoped prompts + verification** perform better ✅
- Uses **DistilGPT2** as a lightweight LLM model
- [See code](experiments/v1-simple-filters)

### 🔹 v2 — Chained Guards Pipeline
- Introduces a **multi-layer defense stack**
- Layers include:
  1. Regex prefilter (block obvious bad inputs)
  2. Semantic embedding check (MiniLM)
  3. LLM self-check (DistilGPT2, perplexity/keywords)
  4. Sandbox post-process (redacts sensitive values)
- Provides:
  - Flask web demo (`/demo`)
  - Benchmark runner with `attack_corpus.json`
  - Unit tests per guard and end-to-end
- [See code](experiments/v2-chained-guards)

### v3 — Context-Aware Injection Detection (Memory Makes Prompt Injections Dangerous)

- Adds short-term session memory (last N turns) and a context guard that compares the new prompt against recent history using MiniLM embeddings.
- Flags two classes:
    - `explicit_override` → phrases like “ignore previous”, “forget earlier”, “reset rules”.
    - `context_shift` → sudden semantic drift from the recent user turn (low similarity).
- Memory toggle in the demo UI (/v3exp) so you can see how outcomes change with/without context.

- [See code](experiments/v3-context-aware)

### v4 — When heuristics meet signatures: catching obfuscated prompt injections

*Treat prompt injections like malware.*


### 🧠 Highlights
- **Signature Guard:** Regex-based detections with severity & category (override, delete, exfil, secret).  
- **Heuristic Guard:** Behavioral scoring — entropy + DistilGPT-2 perplexity + length.  
- **Fusion Engine:** Weighted combination → unified risk score in [0 … 1].  
- **Normalization:** Detects *leet-speak* like `I9gn0r3 pr3v10us` → `ignore previous`.  
- **Threat Meter UI:** Green ✅ → Yellow ⚠️ → Red 🚩 based on final risk.  

---

## 🚀 Quickstart

Clone and run an experiment with latest-v3:

```bash
git clone https://github.com/cveye/Inj3ctStop.git
cd Inj3ctStop/experiments/v4-signature-heuristic

make install
make run

# then open http://localhost:8084/sigheu
```


![alt text](resources/sc-5.jpg)

[See here for more of v4](experiments/v4-signature-heuristic)

## 📊 Roadmap
- v1: ✅ Simple filters + scoped prompts

- v2: ✅ Chained guards pipeline

- v3: ✅ Context-aware detection (memory + context guard)
- v4: ✅ Signature + heuristic engine (IDS-style rules + entropy/keyword scores)

- Vn: 🔄 More to come ....

## 🤝 Contributing
Contributions, ideas, issues, and PRs are welcome!
Please keep submissions defensive and educational.

## 📄 License

MIT — see [LICENSE](LICENSE).

## ⚖️ Ethical Use

This project is intended **for defensive research and educational purposes only**.  
It does **not** contain real jailbreak payloads or exploits — only simulated examples for testing.  

Please **do not use this project to build or share offensive tools**.  
The goal of Inj3ctStop is to **understand, demonstrate, and improve defenses** against prompt injection attacks,  
so that the community can build safer LLM applications.