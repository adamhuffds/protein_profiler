"""
fetchers/uniprot.py
-------------------
Fetches protein metadata from the UniProt REST API. 
Docs: https://www.uniprot.org/help/api_queries
"""

import requests
import logging
from protein_profiler.models.protein import ProteinProfile

logger = logging.getLogger(__name__)

UNIPROT_BASE = "https://rest.uniprot.org/uniprotkb"


def fetch(uniprot_id: str) -> ProteinProfile:
    url = f"{UNIPROT_BASE}/{uniprot_id}.json"
    logger.info(f"Fetching UniProt entry: {url}")

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # --- Core fields ---
    name = data["proteinDescription"]["recommendedName"]["fullName"]["value"]
    gene = data["genes"][0]["geneName"]["value"]
    organism = data["organism"]["scientificName"]
    sequence = data["sequence"]["value"]
    length = data["sequence"]["length"]

    # --- Function comment ---
    function = ""
    for comment in data.get("comments", []):
        if comment["commentType"] == "FUNCTION":
            function = comment["texts"][0]["value"]
            break

    # --- Cross-references ---
    pdb_ids = []
    chembl_target_id = None
    ncbi_gene_id = None

    for ref in data.get("uniProtKBCrossReferences", []):
        db = ref["database"]
        if db == "PDB":
            pdb_ids.append(ref["id"])
        elif db == "ChEMBL":
            chembl_target_id = ref["id"]
        elif db == "GeneID":
            ncbi_gene_id = ref["id"]

    return ProteinProfile(
        uniprot_id=uniprot_id,
        name=name,
        gene=gene,
        organism=organism,
        sequence=sequence,
        length=length,
        function=function,
        pdb_ids=pdb_ids,
        chembl_target_id=chembl_target_id,
        ncbi_gene_id=ncbi_gene_id,
    )