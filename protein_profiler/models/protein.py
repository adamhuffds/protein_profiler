"""
models/protein.py
Docs: https://docs.python.org/3/library/dataclasses.html
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProteinProfile:
    uniprot_id: str
    name: str = ""
    gene: str = ""
    organism: str = ""
    sequence: str = ""
    length: int = 0
    function: str = ""
    pdb_ids: list[str] = field(default_factory=list)
    chembl_target_id: Optional[str] = None
    ncbi_gene_id: Optional[str] = None
    structures: list = field(default_factory=list)
    bioactivities: list = field(default_factory=list)
    ligands: list = field(default_factory=list)
    gene_info: dict = field(default_factory=dict)