"""
enrichment.py
Calculates RDKit physicochemical properties for each Ligand.
Docs: https://www.rdkit.org/docs/GettingStartedInPython.html
"""

import logging
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from protein_profiler.models.ligand import Ligand

logger = logging.getLogger(__name__)


def calculate_properties(ligands: list[Ligand]) -> list[Ligand]:
    for ligand in ligands:
        mol = Chem.MolFromSmiles(ligand.smiles)
        if mol is None:
            logger.warning(f"Could not parse SMILES for {ligand.chembl_id}")
            continue

        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = rdMolDescriptors.CalcNumHBD(mol)
        hba = rdMolDescriptors.CalcNumHBA(mol)
        tpsa = rdMolDescriptors.CalcTPSA(mol)
        rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)

        ligand.molecular_weight = round(mw, 2)
        ligand.logp = round(logp, 2)
        ligand.hbd = hbd
        ligand.hba = hba
        ligand.tpsa = round(tpsa, 2)
        ligand.rotatable_bonds = rotatable

        # Lipinski Rule of Five: fail if more than one violation
        violations = sum([
            mw > 500,
            logp > 5,
            hbd > 5,
            hba > 10,
        ])
        ligand.ro5_pass = violations <= 1

    return ligands

def deduplicate_ligands(ligands: list[Ligand]) -> list[Ligand]:
    """
    Deduplicate ligands by ChEMBL ID, keeping the record with the lowest activity value.
    Same compound can appear multiple times from different assays.
    """
    seen = {}
    for ligand in ligands:
        if ligand.chembl_id not in seen:
            seen[ligand.chembl_id] = ligand
        else:
            if ligand.activity_value and ligand.activity_value < seen[ligand.chembl_id].activity_value:
                seen[ligand.chembl_id] = ligand

    return list(seen.values())