"""Behave environment setup"""

import subprocess
import sys


def before_all(context):
    """Run pytest before BDD tests"""
    print("\n" + "=" * 70)
    print("Running unit tests with pytest...")
    print("=" * 70 + "\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short"],
        cwd=".",
    )

    print("\n" + "=" * 70)
    if result.returncode == 0:
        print("[PASS] All unit tests passed!")
    else:
        print("[INFO] Some unit tests failed, but continuing with BDD tests...")
    print("=" * 70 + "\n")
    print("Starting BDD scenarios...\n")
