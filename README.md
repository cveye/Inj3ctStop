# Inj3ctStop

**Stop prompt injections. Ship safer LLM apps.**

Inj3ctStop is a lightweight security layer for LLM applications. It provides:
- prompt wrappers with sanitization and scoping,
- a simple response verifier,
- ready-to-run scripts for local and remote (VM) environments.

All examples use **simulated** injection inputs. This project is defensive and educational, intended to evolve into a professional toolkit.

## Quickstart

```bash
git clone https://github.com/cveye/Inj3ctStop.git
cd Inj3ctStop
make install        # create venv and install dependencies
make run            # run the injection-handling example