"""
FinGuard AI Dataset Acquisition Script (Backend Entrypoint).
Calls canonical dataset setup and acquisition logic in ml-backend/scripts/dataset_setup.py.
"""

import os
import sys
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
TARGET_SCRIPT = os.path.join(ROOT_DIR, "ml-backend", "scripts", "dataset_setup.py")

if __name__ == "__main__":
    python_bin = sys.executable
    cmd = [python_bin, TARGET_SCRIPT] + sys.argv[1:]
    res = subprocess.run(cmd)
    sys.exit(res.returncode)
