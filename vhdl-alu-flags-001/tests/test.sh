#!/usr/bin/env bash
set -euo pipefail
mkdir -p /logs/verifier
python3 /tests/grade.py > /logs/verifier/reward.json
python3 -c 'import json; d=json.load(open("/logs/verifier/reward.json")); print(d.get("reward", 0.0))' > /logs/verifier/reward.txt
cat /logs/verifier/reward.json
