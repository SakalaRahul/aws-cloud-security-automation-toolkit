from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Finding:
    resource: str
    check: str
    severity: str
    status: str
    message: str
    remediation: str
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
