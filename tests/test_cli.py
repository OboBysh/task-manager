import subprocess
import sys

def test_help():
    result = subprocess.run(
        [sys.executable, 'main.py', '-h'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert 'CLI-менеджер' in result.stdout
