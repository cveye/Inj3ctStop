# Inj3ctStop

**Stop prompt injections. Ship safer LLM apps.**

Inj3ctStop is a compact, defensive playground and starter toolkit for securing LLM wrappers and assistant deployments. It’s designed for engineers and security practitioners who want hands-on, reproducible examples that demonstrate:
- how naive wrappers can be manipulated,
- simple defenses you can add quickly (sanitization, instruction scoping, response verification),
- an easy path to CI canaries and lightweight verifiers.

This repo is intentionally small and safe — all injection-like inputs are simulated and the focus is defensive.

## Quickstart

```bash
git clone https://github.com/<your-org>/Inj3ctStop.git
cd Inj3ctStop
make install        # creates venv and installs deps
make run            # runs the demo with a simulated injection input

