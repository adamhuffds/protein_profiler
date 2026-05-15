"""
models/structure.py
Docs: https://docs.python.org/3/library/dataclasses.html
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Structure:
    pdb_id: str
    title: str = ""
    method: str = ""
    resolution: Optional[float] = None
    chains: list[str] = field(default_factory=list)
    deposition_date: str = ""