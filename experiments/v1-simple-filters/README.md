# v1 — Simple Filters & Scoped Prompts
 
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../../LICENSE) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blueviolet.svg)](https://github.com/cveye/Inj3ctStop/pulls)[![GitHub stars](https://img.shields.io/github/stars/cveye/Inj3ctStop?style=social)](https://github.com/cveye/Inj3ctStop/stargazers)


**Stop prompt injections. Ship safer LLM apps.**  

This is **experiment v1** of the Inj3ctStop research series. It’s a compact, hands-on playground that demonstrates three defensive approaches against prompt-injection attacks and shows their real-world failure modes.

> ⚠️ Educational / defensive only — all inputs are simulated. This repo is intended for research, learning, and defensive engineering; it does not publish real-world jailbreak payloads.


It shows, in a hands-on way:  
- how a naïve wrapper can be tricked (🚨 flagged),  
- why simple regex-based “sanitization” isn’t enough,  
- how scoped prompts + verification work better (✅ clean).  

All examples use **simulated injection inputs**. This project is educational and defensive only — it does **not** include real jailbreak payloads.  

---

## Quickstart (Local Only)  

### 1. Clone the repo  
```bash
git clone https://github.com/cveye/Inj3ctStop.git
cd Inj3ctStop/experiments/v1-simple-filters


2. Create virtual environment & install dependencies

```bash
make install
```

3. Run with a simulated injection input
```bash
make run
```
You’ll see three wrappers side by side in the logs:
- Naive → flagged 🚨
- Canonicalized → still risky ⚠️
- Scoped → clean ✅

4. (Optional) Run tests
```bash
make test
```
### Example Output

```
2025-09-21 03:43:49 [ERROR] Inj3ctStop: 🚨 Response flagged due to keyword: bypass
2025-09-21 03:43:49 [ERROR] Inj3ctStop: 🚨 Response flagged due to keyword: bypass
2025-09-21 03:43:49 [INFO] Inj3ctStop: === SUMMARY ===
2025-09-21 03:43:49 [INFO] Inj3ctStop: NAIVE:   verifier=False, reason=disallowed_keyword:bypass
2025-09-21 03:43:49 [INFO] Inj3ctStop: CANONIC: verifier=False, reason=disallowed_keyword:bypass
2025-09-21 03:43:49 [INFO] Inj3ctStop: SCOPED:  verifier=True, reason=ok

```
### Ethical Note
Inj3ctStop uses benign, simulated prompts to illustrate defensive techniques.

- No real exploits are included.
- The focus is security awareness and safer LLM usage.