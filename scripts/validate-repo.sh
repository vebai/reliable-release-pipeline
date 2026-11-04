#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"
require python3
cd "$ROOT_DIR"
echo '[1/4] Python compilation'
python3 -m compileall -q app scripts tests
echo '[2/4] Application tests'
./scripts/test.sh
echo '[3/4] Evidence record tests'
python3 -m unittest discover -s tests -v
echo '[4/4] Bash syntax'
for file in scripts/*.sh; do bash -n "$file"; done
if python3 -c 'import yaml' >/dev/null 2>&1; then
  echo '[bonus] YAML parsing'
  python3 - <<'PY'
from pathlib import Path
import yaml
for file in sorted(Path('.github/workflows').glob('*.yml')):
    data = yaml.load(file.read_text(), Loader=yaml.BaseLoader)
    assert data.get('jobs') and data.get('on'), file
    print('  parsed:', file)
PY
else
  echo 'NOTE: YAML parser not installed; static YAML parsing not checked.'
fi
echo 'PASS - offline repository checks (Docker/GitHub/AWS untested in this environment)'
