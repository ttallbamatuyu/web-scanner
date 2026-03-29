from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Endpoint:
    url: str
    method: str = "GET"
    parameters: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)

@dataclass
class ScanConfig:
    target_url: str
    depth: int = 1
    threads: int = 1
    timeout: int = 5

@dataclass
class Vulnerability:
    title: str
    severity: str
    endpoint: Endpoint
    payload_used: str
    evidence: str
