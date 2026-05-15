"""
pipeline.py
Orchestrates the full profiling pipeline.
"""

import logging
import sys
import requests
from protein_profiler.fetchers import uniprot, chembl, pdb, ncbi
from protein_profiler import enrichment
from protein_profiler.models.protein import ProteinProfile


def setup_logging(headless: bool) -> None:
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler = logging.FileHandler("logs/protein_profiler.log") if headless else logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)


def run(
    uniprot_id: str,
    headless: bool = False,
    no_display: bool = False,
    email: str = "",
    limit: int = 100,
) -> ProteinProfile:
    setup_logging(headless)
    logger = logging.getLogger(__name__)
    logger.info(f"Starting pipeline for {uniprot_id}")

    raw = requests.get(f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json")
    raw.raise_for_status()
    raw_data = raw.json()

    profile = uniprot.fetch(uniprot_id)

    refs = raw_data.get("uniProtKBCrossReferences", [])
    profile.structures = pdb.parse(refs)
    logger.info(f"Loaded {len(profile.structures)} structures")

    if profile.chembl_target_id:
        profile.ligands = chembl.fetch(profile.chembl_target_id, limit=limit)
        logger.info(f"Loaded {len(profile.ligands)} ligands")
    else:
        logger.warning("No ChEMBL target ID found, skipping bioactivity fetch")

    profile.ligands = enrichment.calculate_properties(profile.ligands)
    profile.ligands = enrichment.deduplicate_ligands(profile.ligands)
    logger.info("RDKit properties calculated")
    logger.info(f"After deduplication: {len(profile.ligands)} unique ligands")

    if profile.ncbi_gene_id:
        profile.gene_info = ncbi.fetch(profile.ncbi_gene_id, email=email)
        logger.info(f"Loaded NCBI gene info for gene ID {profile.ncbi_gene_id}")
    else:
        logger.warning("No NCBI gene ID found, skipping gene info fetch")

    return profile