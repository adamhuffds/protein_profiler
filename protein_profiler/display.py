"""
display.py
Rich terminal display for the compiled ProteinProfile.
Docs: https://rich.readthedocs.io/en/stable/
"""

import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from protein_profiler.models.protein import ProteinProfile

logger = logging.getLogger(__name__)
console = Console()


def show_profile(profile: ProteinProfile) -> None:
    _show_header(profile)
    _show_sequence(profile)
    _show_function(profile)
    _show_gene_info(profile)
    _show_structures(profile)
    _show_ligands(profile)


def _show_header(profile: ProteinProfile) -> None:
    content = (
        f"[bold]{profile.name}[/bold]\n"
        f"UniProt: {profile.uniprot_id}  |  "
        f"Gene: {profile.gene}  |  "
        f"Organism: {profile.organism}"
    )
    console.print(Panel(content, title="Protein Profile", border_style="cyan"))


def _show_sequence(profile: ProteinProfile) -> None:
    content = f"Length: [bold]{profile.length}[/bold] residues\n{profile.sequence}"
    console.print(Panel(content, title="Sequence", border_style="dim"))


def _show_function(profile: ProteinProfile) -> None:
    if profile.function:
        console.print(Panel(profile.function, title="Function", border_style="dim"))


def _show_gene_info(profile: ProteinProfile) -> None:
    if not profile.gene_info:
        return

    g = profile.gene_info
    content = (
        f"[bold]{g.get('name', '')}[/bold] — {g.get('description', '')}\n"
        f"Chromosome: {g.get('chromosome', 'N/A')}  |  "
        f"Location: {g.get('map_location', 'N/A')}\n\n"
        f"{g.get('summary', '')}"
    )
    console.print(Panel(content, title="Gene Info (NCBI)", border_style="dim"))


def _show_structures(profile: ProteinProfile) -> None:
    if not profile.structures:
        return

    table = Table(title="Known Structures", box=box.SIMPLE_HEAVY, header_style="bold cyan")
    table.add_column("PDB ID")
    table.add_column("Method")
    table.add_column("Resolution (Å)")
    table.add_column("Chains")

    for s in profile.structures:
        resolution = f"{s.resolution:.2f}" if s.resolution else "N/A"
        chains = ", ".join(s.chains) if s.chains else "N/A"
        table.add_row(s.pdb_id, s.method, resolution, chains)

    console.print(table)


def _show_ligands(profile: ProteinProfile) -> None:
    if not profile.ligands:
        return

    table = Table(title=f"Ligands (n={len(profile.ligands)})", box=box.SIMPLE_HEAVY, header_style="bold cyan")
    table.add_column("ChEMBL ID")
    table.add_column("Type")
    table.add_column("Value (nM)")
    table.add_column("MW")
    table.add_column("LogP")
    table.add_column("HBD")
    table.add_column("HBA")
    table.add_column("TPSA")
    table.add_column("Ro5")

    for l in profile.ligands:
        ro5 = "[green]✓[/green]" if l.ro5_pass else "[red]✗[/red]"
        table.add_row(
            l.chembl_id,
            l.activity_type,
            str(l.activity_value),
            str(l.molecular_weight),
            str(l.logp),
            str(l.hbd),
            str(l.hba),
            str(l.tpsa),
            ro5,
        )

    console.print(table)