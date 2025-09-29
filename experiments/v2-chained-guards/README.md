# v2 — Chained Guards Pipeline


This experiment implements a **multi-layer defense pipeline** that chains several defense techniques to make prompt-injection attacks harder to succeed.


Layers included (configurable):
1. **prefilter** — regex / token blacklist checks
2. **embedding_check** — semantic similarity check between user input and policy templates
3. **llm_self_check** — a verification step where an LLM (or a classifier) evaluates whether the input looks malicious
4. **sandbox_postprocess** — post-response filtering / redaction


This scaffold provides a runnable Flask demo, a benchmark runner using the v1 attack corpus, and simple tests.


---


## Quickstart


```bash
cd experiments/v2-chained-guards
make install
make run
```
## Run Benchmark

```bash
make install
python runner/run_benchmark.py --layers prefilter,embedding_check,llm_self_check,sandbox_postprocess
```
This will run the attack corpus (reused from v1/tests) and print a detection table and simple latency measurements.

## Sample output

![alt text](../../resources/log.png)

## Run Demo
After the quickstart section, open the following in your browser : http://localhost:8080/demo
![alt text](../../resources/demo_window.png)

## Notes
This scaffold uses lightweight, easily reproducible stubs for embedding and LLM checks so the experiment is easy to run locally. Replace the stubs with real models (embedding model, LLM API) when you want to evaluate real performance.

Add experiment-specific requirements.txt entries if you plan to use heavier models.

## ⚖️ Ethical Use

This project is intended **for defensive research and educational purposes only**.  
It does **not** contain real jailbreak payloads or exploits — only simulated examples for testing.  

Please **do not use this project to build or share offensive tools**.  
The goal of Inj3ctStop is to **understand, demonstrate, and improve defenses** against prompt injection attacks,  
so that the community can build safer LLM applications.