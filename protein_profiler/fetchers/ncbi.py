"""
fetchers/ncbi.py
Docs: https://biopython.org/docs/latest/api/Bio.Entrez.html
"""

import logging
from Bio import Entrez

logger = logging.getLogger(__name__)


def fetch(ncbi_gene_id: str, email: str = "") -> dict:
    Entrez.email = email or "protein_profiler@example.com"
    logger.info(f"Fetching NCBI gene info for gene ID {ncbi_gene_id}")

    handle = Entrez.esummary(db="gene", id=ncbi_gene_id)
    record = Entrez.read(handle)
    handle.close()

    doc = record["DocumentSummarySet"]["DocumentSummary"][0]

    return {
        "name": doc.get("Name", ""),
        "description": doc.get("Description", ""),
        "chromosome": doc.get("Chromosome", ""),
        "map_location": doc.get("MapLocation", ""),
        "summary": doc.get("Summary", ""),
    }