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
    threads: int = 5
    timeout: int = 5
    cookies: Dict[str, str] = field(default_factory=dict)

@dataclass
class Vulnerability:
    title: str
    severity: str
    endpoint: Endpoint
    payload_used: str
    evidence: str
    remediation: str = ""
    cwe: str = ""
    cvss_score: float = 0.0
