"""
fetchers/chembl.py
Docs: https://github.com/chembl/chembl_webresource_client
"""

import logging
from chembl_webresource_client.new_client import new_client
from protein_profiler.models.ligand import Ligand

logger = logging.getLogger(__name__)


def fetch(chembl_target_id: str, limit: int = 100) -> list[Ligand]:
    logger.info(f"Fetching ChEMBL bioactivity for {chembl_target_id}")

    activity = new_client.activity
    results = activity.filter(
        target_chembl_id=chembl_target_id,
        standard_type__in=["IC50", "Ki"],
        standard_relation="=",
    ).only([
        "molecule_chembl_id",
        "canonical_smiles",
        "standard_type",
        "standard_value",
        "standard_units",
        "assay_chembl_id",
        "pchembl_value",
    ])

    records = list(results[:limit])

    ligands = []
    for r in records:
        # skip records missing SMILES or activity value
        if not r.get("canonical_smiles") or not r.get("standard_value"):
            continue

        ligands.append(Ligand(
            chembl_id=r.get("molecule_chembl_id", ""),
            smiles=r.get("canonical_smiles", ""),
            activity_type=r.get("standard_type", ""),
            activity_value=float(r["standard_value"]),
            activity_units=r.get("standard_units", ""),
            assay_id=r.get("assay_chembl_id", ""),
        ))

    logger.info(f"Retrieved {len(ligands)} ligands")
    return ligands