"""
fetchers/pdb.py
Docs: https://www.uniprot.org/help/api_queries
"""

import logging
from protein_profiler.models.structure import Structure

logger = logging.getLogger(__name__)


def parse(cross_references: list[dict]) -> list[Structure]:
    """
    Parse PDB structures directly from UniProt cross-references.
    No additional API call needed — UniProt returns method, resolution, and chains.
    """
    structures = []

    for ref in cross_references:
        if ref.get("database") != "PDB":
            continue

        props = {p["key"]: p["value"] for p in ref.get("properties", [])}

        resolution_raw = props.get("Resolution", "")
        try:
            resolution = float(resolution_raw.replace(" A", ""))
        except ValueError:
            resolution = None

        chains_raw = props.get("Chains", "")
        chain_ids = list({c.strip().split("=")[0] for c in chains_raw.split("/")}) if chains_raw else []

        structures.append(Structure(
            pdb_id=ref["id"],
            method=props.get("Method", ""),
            resolution=resolution,
            chains=chain_ids,
        ))

    logger.info(f"Parsed {len(structures)} PDB structures from UniProt")
    return structures