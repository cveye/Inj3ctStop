#!/usr/bin/env bash
# scripts/setup_vm.sh
# run on Ubuntu VM once to ensure python3/pip present
set -euo pipefail
sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential