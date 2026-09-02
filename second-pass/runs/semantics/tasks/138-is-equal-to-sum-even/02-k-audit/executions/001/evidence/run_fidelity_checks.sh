#!/usr/bin/env bash
set -uo pipefail

script_dir="$(cd "$(dirname "$0")" && pwd)"

echo "COMMAND: bash $script_dir/check_translation.sh"
bash "$script_dir/check_translation.sh"
echo "EXIT_STATUS: $?"

echo "COMMAND: python3 $script_dir/differential_test.py"
python3 "$script_dir/differential_test.py"
echo "EXIT_STATUS: $?"
