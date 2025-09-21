#!/usr/bin/env bash
# scripts/deploy.sh
# Usage: ./deploy.sh user@host /remote/path
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <ssh-host> <remote-dir>"
  echo "Example: $0 ubuntu@1.2.3.4 /home/ubuntu/prompt-demo"
  exit 2
fi

SSH_HOST="$1"
REMOTE_DIR="$2"
LOCAL_DIR="$(pwd)"

ssh "${SSH_HOST}" "mkdir -p ${REMOTE_DIR}"

tar -cf - . | ssh "${SSH_HOST}" "tar -xf - -C ${REMOTE_DIR}"

# Optionally: run remote setup (create venv, pip install) and run demo
ssh "${SSH_HOST}" <<EOF
cd ${REMOTE_DIR}
python3 -m venv venv || true
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
# run demo with default input
python -m demo.demo_run
EOF

echo "Deployed and ran demo on ${SSH_HOST}:${REMOTE_DIR}"