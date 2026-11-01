import json
from datetime import datetime, timezone
from pathlib import Path

def write_report(findings, output):
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(findings),
            "failed": sum(f.status == "FAIL" for f in findings),
            "unknown": sum(f.status == "UNKNOWN" for f in findings),
        },
        "findings": [f.to_dict() for f in findings],
    }
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
