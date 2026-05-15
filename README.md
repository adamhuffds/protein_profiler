# protein_profiler

A CLI pipeline that compiles a biochemical profile for any protein from its UniProt ID. Pulls from UniProt, RCSB PDB, ChEMBL, and NCBI to aggregate protein metadata, known structures, bioactivity data, and RDKit-computed ligand properties. Output is rendered in the terminal via Rich with matplotlib and RDKit visualizations.

# Project Structure

    protein_profiler/
    ├── protein_profiler/          # main package
    │   ├── __init__.py
    │   ├── cli.py                 # entry point, argparse
    │   ├── fetchers/              # one module per API source
    │   │   ├── __init__.py
    │   │   ├── uniprot.py
    │   │   ├── pdb.py
    │   │   ├── chembl.py
    │   │   └── ncbi.py
    │   ├── models/                # Python dataclasses for each data type
    │   │   ├── __init__.py
    │   │   ├── protein.py
    │   │   ├── structure.py
    │   │   └── ligand.py
    │   ├── pipeline.py            # orchestrates fetchers → builds profile object
    │   ├── display.py             # rich terminal output
    │   └── visualize.py           # matplotlib + rdkit plots
    ├── logs/                      # log files (gitignored)
    ├── tests/
    │   └── __init__.py
    ├── main.py                    # thin wrapper: python main.py P41145
    ├── requirements.txt
    ├── README.md
    └── .gitignore

## Usage

```bash
python main.py 
python main.py P41145
python main.py P41145 --no-display
python main.py P41145 --headless --email you@example.com
python main.py P41145 --limit 250
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `uniprot_id` | UniProt accession number | required |
| `--limit` | Max ChEMBL ligands to fetch | 100 |
| `--no-display` | Skip popup windows, save plots to temp files | False |
| `--headless` | Suppress terminal output, write logs to logs/ | False |
| `--email` | Email for NCBI Entrez API identification | "" |

## Installation

```bash
git clone https://github.com/adamhuffds/protein_profiler.git
cd protein_profiler
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Pipeline

    UniProt ID
    ↓
    UniProt — protein name, gene, organism, sequence, function, cross-references
    ↓
    PDB — known experimental structures (parsed from UniProt cross-references)
    ChEMBL — bioactivity data (IC50, Ki) for known ligands
    NCBI — gene-level metadata
    ↓
    RDKit — physicochemical property calculation (MW, LogP, HBD, HBA, TPSA, Ro5)
    ↓
    Rich terminal profile + matplotlib plots + RDKit structure grid

## Output

- Protein metadata panel (name, gene, organism)
- Sequence preview
- Functional annotation
- Gene info (chromosome, map location, NCBI summary)
- Known structures table (PDB ID, method, resolution, chains)
- Ligands table (ChEMBL ID, activity type/value, physicochemical properties, Ro5)
- Activity distribution histogram (pActivity)
- Chemical space scatter plot (MW vs LogP, Ro5 colored)
- Top 6 most potent ligands structure grid (RDKit)

## Reference Implementation

Kappa-type opioid receptor — UniProt: [P41145](https://www.uniprot.org/uniprotkb/P41145)

## Data Sources

- [UniProt REST API](https://www.uniprot.org/help/api_queries)
- [RCSB PDB](https://data.rcsb.org/index.html)
- [ChEMBL](https://chembl.gitbook.io/chembl-interface-documentation/web-services/chembl-data-web-services)
- [NCBI Entrez](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- [RDKit](https://www.rdkit.org/docs/GettingStartedInPython.html)

## Project Status

- [x] UniProt fetcher
- [x] PDB structure parser
- [x] ChEMBL bioactivity fetcher
- [x] NCBI gene info fetcher
- [x] RDKit property enrichment
- [x] Ligand deduplication
- [x] Rich terminal display
- [x] Matplotlib visualizations
- [x] RDKit structure grid
- [x] CLI with argparse
- [ ] Modeling layer