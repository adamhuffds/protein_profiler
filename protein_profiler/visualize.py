"""
visualize.py
Matplotlib and RDKit visualizations for the compiled ProteinProfile.
Docs:
  matplotlib  — https://matplotlib.org/stable/api/index.html
  rdkit draw  — https://www.rdkit.org/docs/GettingStartedInPython.html#drawing-molecules
"""

import logging
import math
import subprocess
import tempfile
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from rdkit import Chem
from rdkit.Chem import Draw
from protein_profiler.models.protein import ProteinProfile
import numpy as np

logger = logging.getLogger(__name__)


def _open(path: str) -> None:
    subprocess.Popen(["xdg-open", path])


def plot_activity_distribution(profile: ProteinProfile, no_display: bool = False) -> None:
    values = [
        l.activity_value
        for l in profile.ligands
        if l.activity_value and l.activity_value > 0
    ]

    if not values:
        logger.warning("No activity values to plot")
        return

    pvalues = [-math.log10(v * 1e-9) for v in values]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(pvalues, bins=20, color="steelblue", edgecolor="white")
    ax.set_xlabel("pActivity (-log10 M)", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title(f"{profile.name}\nActivity Distribution (n={len(pvalues)})", fontsize=13)
    ax.axvline(x=6, color="red", linestyle="--", alpha=0.7, label="pActivity = 6 (1 µM)")
    ax.axvline(x=9, color="green", linestyle="--", alpha=0.7, label="pActivity = 9 (1 nM)")
    ax.legend()
    plt.tight_layout()

    path = os.path.join(tempfile.gettempdir(), "activity_distribution.png")
    plt.savefig(path)
    plt.close()

    if not no_display:
        _open(path)


def plot_chemical_space(profile: ProteinProfile, no_display: bool = False) -> None:
    ligands = [l for l in profile.ligands if l.molecular_weight and l.logp is not None]

    if not ligands:
        logger.warning("No ligand properties to plot")
        return

    mws = [l.molecular_weight for l in ligands]
    logps = [l.logp for l in ligands]
    colors = ["steelblue" if l.ro5_pass else "tomato" for l in ligands]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(mws, logps, c=colors, alpha=0.7, edgecolors="white", linewidths=0.5)

    ax.axvline(x=500, color="gray", linestyle="--", alpha=0.5, linewidth=1)
    ax.axhline(y=5, color="gray", linestyle="--", alpha=0.5, linewidth=1)

    ax.set_xlabel("Molecular Weight (Da)", fontsize=12)
    ax.set_ylabel("LogP", fontsize=12)
    ax.set_title(f"{profile.name}\nChemical Space (MW vs LogP)", fontsize=13)

    pass_patch = mpatches.Patch(color="steelblue", label="Ro5 Pass")
    fail_patch = mpatches.Patch(color="tomato", label="Ro5 Fail")
    ax.legend(handles=[pass_patch, fail_patch])
    plt.tight_layout()

    path = os.path.join(tempfile.gettempdir(), "chemical_space.png")
    plt.savefig(path)
    plt.close()

    if not no_display:
        _open(path)


def draw_top_ligands(profile: ProteinProfile, n: int = 6, no_display: bool = False) -> None:
    sorted_ligands = sorted(
        [l for l in profile.ligands if l.smiles and l.activity_value],
        key=lambda l: l.activity_value
    )[:n]

    if not sorted_ligands:
        logger.warning("No ligands with SMILES to draw")
        return

    mols = []
    legends = []
    for l in sorted_ligands:
        mol = Chem.MolFromSmiles(l.smiles)
        if mol:
            mols.append(mol)
            legends.append(f"{l.chembl_id}  |  {l.activity_type} = {l.activity_value} nM")

    if not mols:
        logger.warning("No valid molecules to draw")
        return

    img = Draw.MolsToGridImage(
        mols,
        molsPerRow=3,
        subImgSize=(500, 400),
        legends=legends,
    )

    path = os.path.join(tempfile.gettempdir(), "top_ligands.png")
    img.save(path)
    logger.info(f"Saved top ligands grid to {path}")

    if not no_display:
        _open(path)