"""
models/ligand.py
Docs: https://docs.python.org/3/library/dataclasses.html
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Ligand:
    chembl_id: str
    name: str = ""
    smiles: str = ""
    activity_type: str = ""
    activity_value: Optional[float] = None
    activity_units: str = ""
    assay_id: str = ""
    molecular_weight: Optional[float] = None
    logp: Optional[float] = None
    hbd: Optional[int] = None
    hba: Optional[int] = None
    tpsa: Optional[float] = None
    rotatable_bonds: Optional[int] = None
    ro5_pass: Optional[bool] = None