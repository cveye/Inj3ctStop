# Inj3ctStop  

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)  [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Status](https://img.shields.io/badge/status-live-brightgreen.svg)](#)  [![Tests](https://img.shields.io/badge/tests-passing-success.svg)](#)  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-blueviolet.svg)](https://github.com/cveye/Inj3ctStop/pulls)  [![Made with ❤️](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)](#)  
 

**Stop prompt injections. Ship safer LLM apps.**  

Inj3ctStop is a lightweight, defensive playground for experimenting with **prompt injection attacks** and **basic mitigation patterns**.  

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
cd Inj3ctStop


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