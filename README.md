# KIRO FOR LIFE SCIENCES

Kiro for Life Sciences is a comprehensive Power package that turns Kiro into
a full-featured life sciences development environment. It provides:

• 24 modular MCP servers covering 100+ databases, tools, and platforms across
  ALL life sciences disciplines — not just genomics
• 10 domain skills with practical guidance for bioinformatics, clinical data,
  ecology, cheminformatics, imaging, immunology, metabolomics, and more
• 16 guided workflows (steering files) for common multi-step tasks
• A searchable resource catalog with 25 categories
• An onboarding dashboard showing everything available at a glance
• Cross-database search that queries multiple databases simultaneously
• Integration with AWS HealthOmics for running genomics pipelines

The architecture is modular: one central Power acts as the hub, and users
install only the MCP servers they need. Each server is a standalone Python
package runnable via `uvx`.

**Disciplines covered:**

Genomics & Sequencing | Proteomics | Structural Biology | Pathways |
Ontologies | Clinical & Pharma | Model Organisms | Molecular Biology |
Computational Chemistry | Immunology | Microbiology & Metagenomics |
Metabolomics | Epigenomics | Imaging & Microscopy | Agriculture & Plants |
Ecology & Environment | Neuroscience | Cell Biology | Healthcare Standards |
Biobanking | Pipelines | Data Standards | Cloud & HPC | AI/ML

**What you can do with it:**

- Search and query 100+ life sciences databases from within Kiro
- Run bioinformatics pipelines (nf-core, WDL, CWL) via AWS HealthOmics
- Design PCR primers and cloning strategies
- Perform molecular docking and ADMET predictions
- Analyze antibody sequences and predict epitopes
- Submit BLAST searches and multiple sequence alignments
- Validate data standards (SBML, ISA-Tab, MAGE-TAB, BioPAX)
- Exchange clinical data via FHIR, HL7, and OMOP CDM
- Submit compute jobs to AWS Batch, Terra, and Galaxy
- Run protein structure predictions with ESM and AlphaFold
- Extract biomedical entities from text with BioNLP
- Cross-reference gene-disease associations across multiple databases
- And much more...

---

## Deployment Instructions

**Prerequisites:**
- Kiro IDE installed
- Python 3.10 or higher
- uv package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Step 1: Unzip the package

```bash
cd ./kiro-life-sciences
```

### Step 2: Create a virtual environment and install packages

```bash
uv venv .venv
source .venv/bin/activate

# Install the shared base package first
uv pip install -e ./life-sciences-common

# Install the central Power package
uv pip install -e "./kiro-life-sciences[dev]"

# Install whichever MCP servers you want to test (pick any/all):
uv pip install -e ./life-sciences-genomics
uv pip install -e ./life-sciences-proteomics
uv pip install -e ./life-sciences-structural
uv pip install -e ./life-sciences-pathways
uv pip install -e ./life-sciences-ontologies
uv pip install -e ./life-sciences-clinical
uv pip install -e ./life-sciences-model-organisms
uv pip install -e ./life-sciences-molbio
uv pip install -e ./life-sciences-cheminformatics
uv pip install -e ./life-sciences-immunology
uv pip install -e ./life-sciences-microbiology
uv pip install -e ./life-sciences-metabolomics
uv pip install -e ./life-sciences-epigenomics
uv pip install -e ./life-sciences-imaging
uv pip install -e ./life-sciences-agriculture
uv pip install -e ./life-sciences-ecology
uv pip install -e ./life-sciences-neuroscience
uv pip install -e ./life-sciences-cellbiology
uv pip install -e ./life-sciences-healthcare
uv pip install -e ./life-sciences-biobanking
uv pip install -e ./life-sciences-pipelines
uv pip install -e ./life-sciences-datastandards
uv pip install -e ./life-sciences-cloud
uv pip install -e ./life-sciences-aiml
```

### Step 3: Copy the Power into Kiro

```bash
cp -r kiro-life-sciences/ ~/.kiro/powers/kiro-life-sciences/
```

### Step 4: Configure MCP servers in your workspace

Create or edit `.kiro/settings/mcp.json` in your Kiro workspace:

```json
{
  "mcpServers": {
    "life-sciences-genomics": {
      "command": "/path/to/KiroLS/.venv/bin/life-sciences-genomics"
    },
    "life-sciences-proteomics": {
      "command": "/path/to/KiroLS/.venv/bin/life-sciences-proteomics"
    },
    "life-sciences-structural": {
      "command": "/path/to/KiroLS/.venv/bin/life-sciences-structural"
    },
    "life-sciences-scigantic": {
      "command": "/path/to/KiroLS/.venv/bin/life-sciences-scigantic"
    }
  }
}
```

Replace `/path/to/KiroLS/` with the actual path where you unzipped.
Add only the servers you installed in Step 2.

### Step 5: Configure credentials (optional)

For databases that require API keys, add env vars:

```json
{
  "mcpServers": {
    "life-sciences-genomics": {
      "command": "/path/to/KiroLS/.venv/bin/life-sciences-genomics",
      "env": {
        "NCBI_API_KEY": "your-ncbi-api-key-here"
      }
    },
    "life-sciences-clinical": {
      "command": "/path/to/KiroLS/.venv/bin/life-sciences-clinical",
      "env": {
        "OMIM_API_KEY": "your-omim-key",
        "DRUGBANK_API_KEY": "your-drugbank-key"
      }
    }
  }
}
```

### Step 6: Verify installation

```bash
source .venv/bin/activate
pytest kiro-life-sciences/tests/ -q
pytest life-sciences-common/tests/ -q
```

Expected: 338+ tests passing for kiro-life-sciences, 32 for life-sciences-common.

### Step 7: Test in Kiro

1. Open Kiro
2. Activate the "kiro-life-sciences" Power from the Powers panel
3. Try asking: "Search NCBI for BRCA1" or "Look up TP53 in UniProt"
4. The Power's tools should be available in chat

---

## Capabilities Map

### MCP Server & Database Coverage

| # | Server | Databases/Tools | Tools | Auth |
|---|--------|----------------|-------|------|
| 1 | **life-sciences-genomics** | NCBI, Ensembl, ClinVar, GEO, SRA, COSMIC, gnomAD, dbSNP, ENCODE, 1000G, DDBJ | 18 | NCBI_API_KEY (optional), COSMIC_API_KEY (required) |
| 2 | **life-sciences-proteomics** | UniProt, InterPro, Pfam, STRING, PRIDE, neXtProt | 8 | None |
| 3 | **life-sciences-structural** | PDB, AlphaFold DB, CATH, SCOP | 6 | None |
| 4 | **life-sciences-pathways** | KEGG, Reactome, BioCyc, WikiPathways, IntAct | 7 | None |
| 5 | **life-sciences-ontologies** | Gene Ontology, HPO, Disease Ontology | 6 | None |
| 6 | **life-sciences-clinical** | OMIM, DrugBank, ChEMBL, PharmGKB, OpenTargets, FDA FAERS, ClinicalTrials.gov | 10 | OMIM_API_KEY, DRUGBANK_API_KEY |
| 7 | **life-sciences-model-organisms** | FlyBase, WormBase, ZFIN, MGI, SGD | 5 | None |
| 8 | **life-sciences-molbio** | BLAST, Clustal Omega, MUSCLE, HMMER, Primer3, PrimerBLAST, REBASE | 9 | None |
| 9 | **life-sciences-cheminformatics** | PubChem, ChemSpider, ZINC, RDKit, SwissDock, ADMET | 8 | CHEMSPIDER_API_KEY |
| 10 | **life-sciences-immunology** | IEDB, ImmPort, IMGT, abYsis | 4 | IMMPORT_USERNAME + IMMPORT_PASSWORD |
| 11 | **life-sciences-microbiology** | SILVA, Greengenes, QIIME 2, MG-RAST, BV-BRC, CARD | 8 | None |
| 12 | **life-sciences-metabolomics** | HMDB, MetaboLights, METLIN, MassBank | 4 | None |
| 13 | **life-sciences-epigenomics** | IHEC, Roadmap Epigenomics, MethBase | 3 | None |
| 14 | **life-sciences-imaging** | OMERO, CellProfiler, ImageJ, DICOM, BioImage Archive, IDR, EMPIAR | 7 | OMERO credentials (optional) |
| 15 | **life-sciences-agriculture** | Phytozome, TAIR, Gramene, PlantGDB | 4 | None |
| 16 | **life-sciences-ecology** | GBIF, BOLD, iNaturalist, IUCN Red List, GenBank Env, MGnify | 7 | IUCN_API_KEY |
| 17 | **life-sciences-neuroscience** | Allen Brain Atlas, NeuroMorpho, OpenNeuro, BrainMap | 5 | None |
| 18 | **life-sciences-cellbiology** | Cell Atlas, CellxGene, Single Cell Expression Atlas | 4 | None |
| 19 | **life-sciences-healthcare** | FHIR, HL7 v2, OMOP CDM, REDCap, DICOMweb | 8 | REDCAP_API_TOKEN |
| 20 | **life-sciences-biobanking** | BBMRI, BioSample, LIMS, protocols.io | 6 | LIMS credentials (optional) |
| 21 | **life-sciences-pipelines** | nf-core, GATK/Broad (WDL), CWL Community, GitHub Community | 8 | None |
| 22 | **life-sciences-datastandards** | MAGE-TAB, ISA-Tab, SBML, BioPAX | 7 | None |
| 23 | **life-sciences-cloud** | AWS Batch, Terra, Galaxy | 7 | TERRA_TOKEN |
| 24 | **life-sciences-aiml** | ESM, AlphaFold, BioNLP (BioGPT/PubMedBERT) | 6 | None |
| 25 | **life-sciences-scigantic** | Scigantic (cross-domain dataset catalog + schema cards) | 6 | None |

### Domain Skills (10)

| Skill | Focus |
|-------|-------|
| bioinformatics-file-formats | FASTA, FASTQ, BAM, VCF, GFF, BED, DICOM, SBML |
| genomics-pipeline-best-practices | WDL/Nextflow/CWL design patterns |
| data-compliance | HIPAA, GDPR, GxP, MIAME, MINSEQE |
| clinical-interoperability | FHIR, HL7, OMOP CDM |
| ecological-data-analysis | Species distribution, biodiversity, eDNA |
| cheminformatics-best-practices | SMILES, InChI, Lipinski, SAR |
| biomedical-imaging | Segmentation, feature extraction, DICOM |
| immunology-vaccine-design | Epitope prediction, MHC binding, antibodies |
| metabolomics-analysis | Metabolite ID, spectral matching |
| single-cell-analysis | QC, clustering, trajectory inference |

### Steering Workflows (16)

| Steering File | Workflow | Auto-Activates On |
|---------------|----------|-------------------|
| variant-calling-pipeline | HealthOmics variant calling | `*.wdl`, `*.nf`, `*.cwl` |
| gene-disease-associations | ClinVar → OMIM → HPO cross-referencing | `*clinvar*`, `*variant*`, `*disease*` |
| protein-structure-analysis | PDB → AlphaFold → CATH | `*protein*`, `*structure*`, `*pdb*` |
| pipeline-import-healthomics | Import nf-core/WDL into HealthOmics | `*.wdl`, `*.nf`, `nextflow.config` |
| resource-catalog-browsing | Search/browse the catalog | Always available |
| fhir-clinical-integration | FHIR + OMOP CDM workflows | `*fhir*`, `*clinical*`, `*omop*` |
| species-distribution-analysis | GBIF → IUCN → iNaturalist | `*species*`, `*occurrence*`, `*gbif*` |
| metabolite-identification | HMDB → MetaboLights → MassBank | `*metabol*`, `*hmdb*`, `*massbank*` |
| microbiome-analysis | SILVA → QIIME 2 → MG-RAST | `*microbiome*`, `*16s*`, `*metagenom*` |
| compound-screening | PubChem → RDKit → ZINC → docking | `*compound*`, `*screen*`, `*smiles*` |
| biomedical-image-analysis | OMERO → CellProfiler → ImageJ | `*image*`, `*microscop*`, `*dicom*` |
| molecular-docking | PDB → ligand prep → SwissDock | `*dock*`, `*ligand*`, `*binding*` |
| primer-design-cloning | Primer3 → PrimerBLAST → REBASE | `*primer*`, `*clone*`, `*restriction*` |
| single-cell-rnaseq | CellxGene → expression analysis | `*single*cell*`, `*scrnaseq*`, `*10x*` |
| epigenomics-analysis | IHEC → Roadmap → ENCODE | `*epigenom*`, `*methylat*`, `*chromatin*` |
| amr-analysis | CARD → BV-BRC resistance profiling | `*resistance*`, `*amr*`, `*antibiotic*` |

### Cross-Database Search

| Search Type | Databases Queried |
|-------------|-------------------|
| **gene** | NCBI Gene, UniProt, Ensembl, ClinVar, OMIM, Gene Ontology, KEGG, Reactome |
| **drug** | DrugBank, ChEMBL, PharmGKB, OpenTargets, PubChem, HMDB, CARD |
| **protein** | UniProt, PDB, AlphaFold DB, InterPro, STRING, neXtProt, ESM |
| **species** | GBIF, IUCN Red List, BOLD, iNaturalist, NCBI Taxonomy, MGnify |
| **metabolite** | HMDB, MetaboLights, METLIN, MassBank, PubChem, KEGG |
| **cell_type** | CellxGene, Single Cell Expression Atlas, Cell Atlas, Allen Brain Atlas |

### Authentication Reference

| Database | Credential | Required? |
|----------|-----------|-----------|
| NCBI | `NCBI_API_KEY` | Optional (increases rate limit) |
| COSMIC | `COSMIC_API_KEY` | Required |
| OMIM | `OMIM_API_KEY` | Required |
| DrugBank | `DRUGBANK_API_KEY` | Required |
| ChemSpider | `CHEMSPIDER_API_KEY` | Required |
| ImmPort | `IMMPORT_USERNAME`, `IMMPORT_PASSWORD` | Required |
| IUCN Red List | `IUCN_API_KEY` | Required |
| FHIR Server | `FHIR_BASE_URL` | Required |
| REDCap | `REDCAP_API_KEY`, `REDCAP_BASE_URL` | Required |
| OMERO | `OMERO_HOST`, `OMERO_USERNAME`, `OMERO_PASSWORD` | Required |
| Terra | `TERRA_API_KEY` | Required |
| Galaxy | `GALAXY_BASE_URL`, `GALAXY_API_KEY` | Optional |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Kiro IDE                              │
├─────────────────────────────────────────────────────────────┤
│              kiro-life-sciences Power (Hub)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │  Dashboard   │ │   Catalog    │ │ Credential Mgr   │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │   Skills     │ │   Steering   │ │ Bundle Manifest  │    │
│  │  (10 Guides) │ │ (16 Workflows│ │ (24 Servers)     │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│         Modular MCP Servers (Install as Needed via uvx)     │
│  genomics · proteomics · structural · pathways · ontologies │
│  clinical · model-organisms · molbio · cheminformatics ...  │
├─────────────────────────────────────────────────────────────┤
│            Peer Power: aws-healthomics                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Package Contents

### kiro-life-sciences/ — Central Power Hub

| Component | Description |
|-----------|-------------|
| `POWER.md` | Documentation and getting-started guide |
| `pyproject.toml` | Package config (pydantic, httpx, pytest, hypothesis) |
| `bundle-manifest.json` | Declares all 24 MCP servers, 10 skills, 16 steering files |
| `skills/` | 10 domain-specific skill files |
| `steering/` | 16 step-by-step workflow guides |
| `src/kiro_life_sciences/` | Core Python modules (catalog, dashboard, credentials, installer, skills) |

### life-sciences-common/ — Shared Base Package

- `BaseLifeSciencesServer` — Async HTTP client with retry logic
- Error classes — RateLimitError, AuthenticationError, NotFoundError, etc.
- Exponential backoff — 429 retry, 5xx retry, timeout retry

---

## Additional Files

- [common_queries.md](common_queries.md) — Example test cases and advanced multi-step workflows
- [CAPABILITIES.md](CAPABILITIES.md) — Full capabilities overview with detailed descriptions
