"""Source-only discovery entry point owned by the Rig CLI; no grading data."""
import json
from pathlib import Path
import sys

from evaluate import prepare


if __name__ == '__main__':
    try:
        job, source, baseline = map(Path, sys.argv[1:4])
        result = prepare(source, job / 'construction', baseline,
                         seconds=int(sys.argv[4]), inventory=True)
        # Only the passive public plan crosses back to the CLI. Controller/model
        # captures and temporary paths are never ordinary command receipts.
        (job / 'inventory-result.json').write_text(json.dumps({
            'complete': result['complete'], 'plan': result['plan']}))
    except BaseException:
        sys.exit(2)
