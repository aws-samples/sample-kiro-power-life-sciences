# Kiro for Life Sciences

A unified Kiro Power that provides life sciences developers, bioinformaticians, clinical researchers, ecologists, neuroscientists, immunologists, and other life sciences professionals with a comprehensive suite of tools, databases, pipelines, and skills spanning genomics, proteomics, structural biology, clinical research, ecology, neuroscience, and more.

## Overview

Kiro for Life Sciences follows a **Power + Modular MCP Servers** architecture. This central Power acts as the hub — providing the onboarding dashboard, resource catalog, credential manager, skills, and steering files. Domain-specific MCP servers are independently deployable via `uvx` and configured in `mcp.json`. You install only the MCP servers you need, keeping the resource footprint light.

### What's Included

- **25 domain MCP servers** covering 100+ life sciences databases and tools
- **10 domain skills** with practical guidance for common life sciences tasks
- **16 steering files** with step-by-step workflow guides
- **Resource catalog** — searchable, categorized index of all available resources
- **Onboarding dashboard** — post-installation summary with status indicators
- **Credential manager** — unified credential configuration for authenticated databases
- **AWS HealthOmics integration** — peer Power for genomics workflow management

## Getting Started

### 1. Install the Power

Install the `kiro-life-sciences` Power from the Kiro Powers panel. This installs the central hub with the resource catalog, dashboard, skills, and steering files.

### 2. Configure MCP Servers

Add the MCP servers you need to your `mcp.json`. Each server is a standalone Python package runnable via `uvx`:

> **Security note:** These packages are not published to PyPI. Always launch them with `uvx --from git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=<package>` (or `--from /path/to/clone/<package>`) as shown below. Never run `uvx <package>` with a bare name: that resolves from public PyPI, where anyone could register the name.

```json
{
  "mcpServers": {
    "life-sciences-genomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-genomics", "life-sciences-genomics"],
      "env": {
        "NCBI_API_KEY": "${secret:ncbi-api-key}"
      }
    },
    "life-sciences-proteomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-proteomics", "life-sciences-proteomics"]
    }
  }
}
```

### 3. Configure Credentials (Optional)

Some databases require API keys or authentication. Configure credentials using the `${secret:key-name}` syntax in `mcp.json`. The onboarding dashboard shows which resources need credentials and provides links to obtain them.

### 4. Explore the Resource Catalog

Use the resource catalog to discover databases, pipelines, tools, and skills. Search by keyword, browse by category, or filter by resource type.

### 5. Activate Skills and Steering Files

Activate domain skills for context-specific guidance. Steering files auto-activate based on file patterns in your workspace.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Kiro IDE                          │
├─────────────────────────────────────────────────────┤
│              kiro-life-sciences Power                │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │ Dashboard │ │ Catalog  │ │ Credential Manager│   │
│  └──────────┘ └──────────┘ └───────────────────┘   │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │  Skills  │ │ Steering │ │  Bundle Manifest  │   │
│  └──────────┘ └──────────┘ └───────────────────┘   │
├─────────────────────────────────────────────────────┤
│           Modular MCP Servers (via uvx)             │
│  genomics · proteomics · structural · pathways ...  │
├─────────────────────────────────────────────────────┤
│              Peer: aws-healthomics Power             │
└─────────────────────────────────────────────────────┘
```

The Power does not contain MCP server implementations. It knows about all 25 servers declaratively through the bundle manifest and can show their status, provide setup instructions, and coordinate cross-database searches even when only a subset is installed.

## MCP Servers

### 1. life-sciences-genomics
**Domain:** Genomics and Sequencing
**Databases:** NCBI, Ensembl, ClinVar, GEO, SRA, COSMIC, gnomAD, dbSNP, ENCODE, 1000 Genomes, DDBJ
**Tools:** ~16 tools for gene search, sequence retrieval, variant lookup, expression data, and functional genomics.
**Auth:** NCBI API key (optional, increases rate limit). COSMIC API key (required for COSMIC).

```json
{
  "life-sciences-genomics": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-genomics", "life-sciences-genomics"],
    "env": {
      "NCBI_API_KEY": "${secret:ncbi-api-key}",
      "COSMIC_API_KEY": "${secret:cosmic-api-key}"
    }
  }
}
```

### 2. life-sciences-proteomics
**Domain:** Proteomics
**Databases:** UniProt, InterPro, Pfam, STRING, PRIDE, neXtProt
**Tools:** ~18 tools for protein search, domain analysis, interaction networks, and proteomics datasets.
**Auth:** None required (all open access).

```json
{
  "life-sciences-proteomics": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-proteomics", "life-sciences-proteomics"]
  }
}
```

### 3. life-sciences-structural
**Domain:** Structural Biology
**Databases:** PDB, AlphaFold DB, CATH, SCOP
**Tools:** ~8 tools for structure search, predicted structure retrieval, and domain classification.
**Auth:** None required.

```json
{
  "life-sciences-structural": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-structural", "life-sciences-structural"]
  }
}
```

### 4. life-sciences-pathways
**Domain:** Pathways and Interactions
**Databases:** KEGG, Reactome, BioCyc, WikiPathways, IntAct
**Tools:** ~10 tools for pathway search, enrichment analysis, and interaction data.
**Auth:** None required.

```json
{
  "life-sciences-pathways": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-pathways", "life-sciences-pathways"]
  }
}
```

### 5. life-sciences-ontologies
**Domain:** Ontologies
**Databases:** Gene Ontology, HPO (Human Phenotype Ontology), Disease Ontology
**Tools:** ~7 tools for ontology term lookup, hierarchy navigation, and annotation.
**Auth:** None required.

```json
{
  "life-sciences-ontologies": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-ontologies", "life-sciences-ontologies"]
  }
}
```

### 6. life-sciences-clinical
**Domain:** Clinical and Pharma
**Databases:** OMIM, DrugBank, ChEMBL, PharmGKB, OpenTargets, FDA FAERS, ClinicalTrials.gov
**Tools:** ~20 tools for disease-gene associations, drug information, pharmacogenomics, and clinical trials.
**Auth:** OMIM API key (required). DrugBank API key (required).

```json
{
  "life-sciences-clinical": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-clinical", "life-sciences-clinical"],
    "env": {
      "OMIM_API_KEY": "${secret:omim-api-key}",
      "DRUGBANK_API_KEY": "${secret:drugbank-api-key}"
    }
  }
}
```

### 7. life-sciences-model-organisms
**Domain:** Model Organisms
**Databases:** FlyBase, WormBase, ZFIN, MGI, SGD
**Tools:** ~10 tools for model organism gene search, phenotype data, and ortholog mapping.
**Auth:** None required.

```json
{
  "life-sciences-model-organisms": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-model-organisms", "life-sciences-model-organisms"]
  }
}
```

### 8. life-sciences-molbio
**Domain:** Molecular Biology and Biochemistry
**Databases/Tools:** BLAST, Clustal Omega, MUSCLE, HMMER, Primer3, PrimerBLAST, REBASE, Restriction Enzymes, Cloning Design
**Tools:** ~15 tools for sequence alignment, primer design, restriction analysis, and cloning.
**Auth:** None required.

```json
{
  "life-sciences-molbio": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-molbio", "life-sciences-molbio"]
  }
}
```

### 9. life-sciences-cheminformatics
**Domain:** Computational Chemistry and Drug Discovery
**Databases/Tools:** PubChem, ChemSpider, ZINC, RDKit, AutoDock/SwissDock, ADMET, Molecular Visualization
**Tools:** ~15 tools for compound search, molecular descriptors, docking, and ADMET prediction.
**Auth:** ChemSpider API key (required for ChemSpider).

```json
{
  "life-sciences-cheminformatics": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cheminformatics", "life-sciences-cheminformatics"],
    "env": {
      "CHEMSPIDER_API_KEY": "${secret:chemspider-api-key}"
    }
  }
}
```

### 10. life-sciences-immunology
**Domain:** Immunology
**Databases:** IEDB, ImmPort, IMGT, abYsis
**Tools:** ~10 tools for epitope prediction, immune data, antibody analysis, and immunogenetics.
**Auth:** ImmPort credentials (required for ImmPort).

```json
{
  "life-sciences-immunology": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-immunology", "life-sciences-immunology"],
    "env": {
      "IMMPORT_USERNAME": "${secret:immport-username}",
      "IMMPORT_PASSWORD": "${secret:immport-password}"
    }
  }
}
```

### 11. life-sciences-microbiology
**Domain:** Microbiology and Metagenomics
**Databases:** SILVA, Greengenes, QIIME 2, MG-RAST, BV-BRC, CARD
**Tools:** ~12 tools for taxonomy, microbiome analysis, metagenomics, and antimicrobial resistance.
**Auth:** None required.

```json
{
  "life-sciences-microbiology": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-microbiology", "life-sciences-microbiology"]
  }
}
```

### 12. life-sciences-metabolomics
**Domain:** Metabolomics
**Databases:** HMDB, MetaboLights, METLIN, MassBank
**Tools:** ~8 tools for metabolite search, spectral matching, and pathway context.
**Auth:** None required.

```json
{
  "life-sciences-metabolomics": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-metabolomics", "life-sciences-metabolomics"]
  }
}
```

### 13. life-sciences-epigenomics
**Domain:** Epigenomics
**Databases:** IHEC, Roadmap Epigenomics, MethBase
**Tools:** ~6 tools for chromatin state maps, methylation data, and epigenomic datasets.
**Auth:** None required.

```json
{
  "life-sciences-epigenomics": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-epigenomics", "life-sciences-epigenomics"]
  }
}
```

### 14. life-sciences-imaging
**Domain:** Imaging and Microscopy
**Databases/Tools:** OMERO, CellProfiler, ImageJ, DICOM, BioImage Archive, IDR, EMPIAR
**Tools:** ~14 tools for image import, segmentation, feature extraction, and DICOM handling.
**Auth:** OMERO credentials (required for OMERO server access).

```json
{
  "life-sciences-imaging": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-imaging", "life-sciences-imaging"],
    "env": {
      "OMERO_HOST": "${secret:omero-host}",
      "OMERO_USERNAME": "${secret:omero-username}",
      "OMERO_PASSWORD": "${secret:omero-password}"
    }
  }
}
```

### 15. life-sciences-agriculture
**Domain:** Agricultural and Plant Biology
**Databases:** Phytozome, TAIR, Gramene, PlantGDB
**Tools:** ~9 tools for plant gene search, genome browsing, and comparative genomics.
**Auth:** Phytozome credentials (required for Phytozome).

```json
{
  "life-sciences-agriculture": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-agriculture", "life-sciences-agriculture"],
    "env": {
      "PHYTOZOME_USERNAME": "${secret:phytozome-username}",
      "PHYTOZOME_PASSWORD": "${secret:phytozome-password}"
    }
  }
}
```

### 16. life-sciences-ecology
**Domain:** Ecology and Environmental Biology
**Databases:** GBIF, BOLD, iNaturalist, IUCN Red List, GenBank Env, MGnify
**Tools:** ~15 tools for occurrence data, conservation status, species identification, and metagenomics.
**Auth:** IUCN Red List API key (required for IUCN).

```json
{
  "life-sciences-ecology": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-ecology", "life-sciences-ecology"],
    "env": {
      "IUCN_API_KEY": "${secret:iucn-api-key}"
    }
  }
}
```

### 17. life-sciences-neuroscience
**Domain:** Neuroscience
**Databases:** Allen Brain Atlas, NeuroMorpho, OpenNeuro, BrainMap
**Tools:** ~8 tools for brain gene expression, neuron morphology, neuroimaging datasets, and brain mapping.
**Auth:** None required.

```json
{
  "life-sciences-neuroscience": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-neuroscience", "life-sciences-neuroscience"]
  }
}
```

### 18. life-sciences-cellbiology
**Domain:** Cell Biology
**Databases:** Cell Atlas, CellxGene, Single Cell Expression Atlas
**Tools:** ~7 tools for cell type data, single-cell gene expression, and cell atlas browsing.
**Auth:** None required.

```json
{
  "life-sciences-cellbiology": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cellbiology", "life-sciences-cellbiology"]
  }
}
```

### 19. life-sciences-healthcare
**Domain:** Healthcare Standards
**Databases/Tools:** FHIR, HL7 v2, OMOP CDM, REDCap, DICOMweb
**Tools:** ~15 tools for clinical data exchange, EHR integration, and medical imaging.
**Auth:** FHIR server URL (required). REDCap API key (required for REDCap).

```json
{
  "life-sciences-healthcare": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-healthcare", "life-sciences-healthcare"],
    "env": {
      "FHIR_BASE_URL": "${secret:fhir-base-url}",
      "REDCAP_API_KEY": "${secret:redcap-api-key}",
      "REDCAP_BASE_URL": "${secret:redcap-base-url}"
    }
  }
}
```

### 20. life-sciences-biobanking
**Domain:** Biobanking and Sample Management
**Databases/Tools:** BBMRI, BioSample, LIMS (SiLA 2), Sample Inventory, protocols.io
**Tools:** ~10 tools for biobank search, sample tracking, lab protocols, and LIMS integration.
**Auth:** LIMS credentials (required for LIMS). protocols.io API key (optional).

```json
{
  "life-sciences-biobanking": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-biobanking", "life-sciences-biobanking"],
    "env": {
      "LIMS_BASE_URL": "${secret:lims-base-url}",
      "LIMS_API_KEY": "${secret:lims-api-key}"
    }
  }
}
```

### 21. life-sciences-pipelines
**Domain:** Pipelines
**Databases/Tools:** nf-core index, WDL index, CWL index, GitHub pipeline index
**Tools:** ~8 tools for pipeline search, browse by language/category, and HealthOmics import instructions.
**Auth:** None required.

```json
{
  "life-sciences-pipelines": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-pipelines", "life-sciences-pipelines"]
  }
}
```

### 22. life-sciences-datastandards
**Domain:** Data Standards and Formats
**Databases/Tools:** MAGE-TAB, ISA-Tab, SBML, BioPAX
**Tools:** ~9 tools for parsing, validating, and generating data standard files.
**Auth:** None required.

```json
{
  "life-sciences-datastandards": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-datastandards", "life-sciences-datastandards"]
  }
}
```

### 23. life-sciences-cloud
**Domain:** Cloud and HPC
**Databases/Tools:** AWS Batch, Terra, Galaxy
**Tools:** ~12 tools for cloud job submission, workspace management, and workflow execution.
**Auth:** Terra credentials (required for Terra). Galaxy API key (optional).

```json
{
  "life-sciences-cloud": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cloud", "life-sciences-cloud"],
    "env": {
      "TERRA_API_KEY": "${secret:terra-api-key}",
      "GALAXY_BASE_URL": "${secret:galaxy-base-url}",
      "GALAXY_API_KEY": "${secret:galaxy-api-key}"
    }
  }
}
```

### 24. life-sciences-aiml
**Domain:** AI/ML for Life Sciences
**Databases/Tools:** ESM (protein language model), AlphaFold predictions, BioNLP
**Tools:** ~10 tools for protein embeddings, structure prediction, and biomedical NLP.
**Auth:** None required (uses public APIs).

```json
{
  "life-sciences-aiml": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-aiml", "life-sciences-aiml"]
  }
}
```

### 25. life-sciences-cancergenomics
**Domain:** Cancer Genomics
**Databases:** cBioPortal
**Tools:** 7 tools for cancer study search, molecular profiles, clinical data, gene lookups, cancer type browsing, and tumor mutation burden (TMB) analysis.
**Auth:** None required (cBioPortal public API is open access).

```json
{
  "life-sciences-cancergenomics": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cancergenomics", "life-sciences-cancergenomics"]
  }
}
```


## Skills

Skills are domain-specific instruction sets that provide practical guidance for common life sciences tasks. Activate them manually via the Kiro context menu when you need domain expertise.

| # | Skill | Description |
|---|-------|-------------|
| 1 | **bioinformatics-file-formats** | Guide to FASTA, FASTQ, BAM, VCF, GFF, BED, DICOM, SBML, BioPAX, MAGE-TAB, and ISA-Tab formats with examples, tools, and usage guidance. |
| 2 | **genomics-pipeline-best-practices** | Workflow design patterns, resource optimization (CPU/memory/storage), error handling, checkpointing, and reproducibility for WDL/Nextflow/CWL pipelines. |
| 3 | **data-compliance** | HIPAA, GDPR, GxP, MIAME, and MINSEQE compliance guidance including data classification, de-identification, consent management, and audit trails. |
| 4 | **clinical-interoperability** | FHIR resource modeling, HL7 v2 message construction, OMOP CDM mapping, and terminology services (SNOMED CT, LOINC, ICD). |
| 5 | **ecological-data-analysis** | Species distribution modeling, biodiversity metrics (Shannon, Simpson), environmental DNA analysis, and occurrence data handling. |
| 6 | **cheminformatics-best-practices** | SMILES, InChI, MOL formats, molecular property calculation, Lipinski rules, SAR analysis, and virtual screening workflows. |
| 7 | **biomedical-imaging** | Image preprocessing, segmentation algorithms (Otsu, watershed, U-Net), feature extraction, DICOM handling, and microscopy analysis pipelines. |
| 8 | **immunology-vaccine-design** | Epitope prediction workflows, MHC binding analysis, antibody engineering patterns, and immunogenicity assessment. |
| 9 | **metabolomics-analysis** | Metabolite identification (MSI levels), spectral matching, pathway enrichment, statistical analysis, and normalization methods. |
| 10 | **single-cell-analysis** | QC metrics, normalization (scran, SCTransform), clustering (Leiden, Louvain), differential expression, and trajectory inference (Monocle, PAGA). |

## Steering Files

Steering files are step-by-step workflow guides that auto-activate based on file patterns in your workspace. They guide you through multi-step life sciences tasks using the appropriate MCP server tools.

| # | Steering File | Description | Auto-Activates On |
|---|--------------|-------------|-------------------|
| 1 | **variant-calling-pipeline** | Create HealthOmics workflow, configure inputs, start run, monitor, and analyze results. | `*.wdl`, `*.nf`, `*.cwl` |
| 2 | **gene-disease-associations** | Cross-reference ClinVar → OMIM → HPO → Disease Ontology for gene-disease links. | `*clinvar*`, `*variant*`, `*disease*` |
| 3 | **protein-structure-analysis** | Search PDB → AlphaFold → CATH → UniProt for comprehensive structural analysis. | `*protein*`, `*structure*`, `*pdb*` |
| 4 | **pipeline-import-healthomics** | Import nf-core/WDL pipeline → package → create HealthOmics workflow → run. | `*.wdl`, `*.nf`, `*.cwl`, `nextflow.config` |
| 5 | **resource-catalog-browsing** | Discover, search, filter, and browse the life sciences resource catalog. | Always available |
| 6 | **fhir-clinical-integration** | Connect to FHIR server → query resources → map to OMOP CDM. | `*fhir*`, `*clinical*`, `*omop*`, `*hl7*` |
| 7 | **species-distribution-analysis** | GBIF occurrences → IUCN status → iNaturalist observations → distribution model. | `*species*`, `*occurrence*`, `*gbif*` |
| 8 | **metabolite-identification** | HMDB search → MetaboLights → MassBank spectral matching. | `*metabol*`, `*hmdb*`, `*massbank*` |
| 9 | **microbiome-analysis** | SILVA taxonomy → QIIME 2 pipeline → MG-RAST annotation. | `*microbiome*`, `*16s*`, `*metagenom*` |
| 10 | **compound-screening** | PubChem search → RDKit descriptors → ZINC filtering → docking. | `*compound*`, `*screen*`, `*smiles*`, `*drug*` |
| 11 | **biomedical-image-analysis** | OMERO import → CellProfiler pipeline → ImageJ analysis. | `*image*`, `*microscop*`, `*dicom*`, `*.tif` |
| 12 | **molecular-docking** | PDB structure → ligand prep → SwissDock docking → analyze poses. | `*dock*`, `*ligand*`, `*binding*` |
| 13 | **primer-design-cloning** | Primer3 design → PrimerBLAST specificity → REBASE sites → cloning strategy. | `*primer*`, `*clone*`, `*restriction*` |
| 14 | **single-cell-rnaseq** | CellxGene datasets → expression analysis → cell type annotation. | `*single*cell*`, `*scrnaseq*`, `*10x*` |
| 15 | **epigenomics-analysis** | IHEC data → Roadmap chromatin states → ENCODE integration. | `*epigenom*`, `*methylat*`, `*chromatin*` |
| 16 | **amr-analysis** | CARD resistance search → BV-BRC genome analysis → resistance profiling. | `*resistance*`, `*amr*`, `*antibiotic*` |

## Credential Configuration

Several databases require API keys or authentication. Here's how to configure credentials for each:

### How Credentials Work

Credentials are stored as environment variables in `mcp.json` using the `${secret:key-name}` syntax. Kiro's secret management resolves these at runtime. Credentials are never written to project files or version control.

### Credential Reference

| Database | Env Variable | Required? | How to Obtain |
|----------|-------------|-----------|---------------|
| NCBI | `NCBI_API_KEY` | Optional (increases rate limit) | [NCBI Account Settings](https://www.ncbi.nlm.nih.gov/account/settings/) |
| COSMIC | `COSMIC_API_KEY` | Required | [COSMIC Registration](https://cancer.sanger.ac.uk/cosmic/register) |
| OMIM | `OMIM_API_KEY` | Required | [OMIM API Access](https://www.omim.org/api) |
| DrugBank | `DRUGBANK_API_KEY` | Required | [DrugBank API](https://go.drugbank.com/api) |
| ChemSpider | `CHEMSPIDER_API_KEY` | Required | [ChemSpider Developer](https://developer.rsc.org/) |
| ImmPort | `IMMPORT_USERNAME`, `IMMPORT_PASSWORD` | Required | [ImmPort Registration](https://www.immport.org/registration) |
| IUCN Red List | `IUCN_API_KEY` | Required | [IUCN API](https://apiv3.iucnredlist.org/) |
| FHIR Server | `FHIR_BASE_URL` | Required | Your organization's FHIR endpoint |
| REDCap | `REDCAP_API_KEY`, `REDCAP_BASE_URL` | Required | Your institution's REDCap admin |
| OMERO | `OMERO_HOST`, `OMERO_USERNAME`, `OMERO_PASSWORD` | Required | Your OMERO server admin |
| LIMS | `LIMS_BASE_URL`, `LIMS_API_KEY` | Required | Your LIMS administrator |
| Phytozome | `PHYTOZOME_USERNAME`, `PHYTOZOME_PASSWORD` | Required | [Phytozome Registration](https://phytozome-next.jgi.doe.gov/) |
| Terra | `TERRA_API_KEY` | Required | [Terra Platform](https://app.terra.bio/) |
| Galaxy | `GALAXY_BASE_URL`, `GALAXY_API_KEY` | Optional | Your Galaxy server admin panel |

## Resource Catalog

The resource catalog is a searchable, categorized index of all databases, pipelines, tools, skills, and steering files available in the bundle.

### Searching

Search across all resources by keyword. Results are ranked by relevance:
1. Exact name match (highest relevance)
2. Name contains keyword
3. Description contains keyword
4. Category matches keyword
5. Data formats contain keyword

### Browsing by Category

Browse resources organized into 26 categories:

| Category | Description |
|----------|-------------|
| Genomics and Sequencing | NCBI, Ensembl, ClinVar, GEO, SRA, COSMIC, gnomAD, dbSNP, ENCODE, 1000 Genomes, DDBJ |
| Cancer Genomics | cBioPortal (studies, molecular profiles, clinical data, tumor mutation burden) |
| Proteomics | UniProt, InterPro, Pfam, STRING, PRIDE, neXtProt |
| Structural Biology | PDB, AlphaFold DB, CATH, SCOP |
| Pathways and Interactions | KEGG, Reactome, BioCyc, WikiPathways, IntAct |
| Ontologies | Gene Ontology, HPO, Disease Ontology |
| Clinical and Pharma | OMIM, DrugBank, ChEMBL, PharmGKB, OpenTargets, FDA FAERS, ClinicalTrials.gov |
| Model Organisms | FlyBase, WormBase, ZFIN, MGI, SGD |
| Molecular Biology and Biochemistry | BLAST, Clustal Omega, MUSCLE, HMMER, Primer3, PrimerBLAST, REBASE |
| Computational Chemistry and Drug Discovery | PubChem, ChemSpider, ZINC, RDKit, AutoDock/SwissDock, ADMET |
| Immunology | IEDB, ImmPort, IMGT, abYsis |
| Microbiology and Metagenomics | SILVA, Greengenes, QIIME 2, MG-RAST, BV-BRC, CARD |
| Metabolomics | HMDB, MetaboLights, METLIN, MassBank |
| Epigenomics | IHEC, Roadmap Epigenomics, MethBase |
| Imaging and Microscopy | OMERO, CellProfiler, ImageJ, DICOM, BioImage Archive, IDR, EMPIAR |
| Agricultural and Plant Biology | Phytozome, TAIR, Gramene, PlantGDB |
| Ecology and Environmental Biology | GBIF, BOLD, iNaturalist, IUCN Red List, GenBank Env, MGnify |
| Neuroscience | Allen Brain Atlas, NeuroMorpho, OpenNeuro, BrainMap |
| Cell Biology | Cell Atlas, CellxGene, Single Cell Expression Atlas |
| Healthcare Standards | FHIR, HL7, OMOP CDM, REDCap, DICOMweb |
| Biobanking and Sample Management | BBMRI, BioSample, LIMS, Sample Inventory, protocols.io |
| Pipelines | nf-core, WDL, CWL, GitHub community pipelines |
| Bioinformatics Analysis Tools | BLAST, alignment tools, primer design |
| Data Standards and Formats | MAGE-TAB, ISA-Tab, SBML, BioPAX |
| Cloud and HPC | AWS Batch, Terra, Galaxy |
| AI/ML for Life Sciences | ESM, AlphaFold predictions, BioNLP |

### Filtering

Filter resources by:
- **Category**: Any of the 26 categories above.
- **Resource type**: `database`, `pipeline`, `tool`, `skill`, or `steering_file`.
- **Auth requirement**: `authenticated` or `open_access`.

### Resource Status

Each resource shows one of three statuses:
- **ready** — MCP server installed and credentials configured. Ready to use.
- **needs_credentials** — MCP server installed but required credentials are missing.
- **needs_setup** — MCP server not yet added to `mcp.json`.

## Onboarding Dashboard

The onboarding dashboard displays after installation and is accessible at any time. It shows:

- **Summary header**: Total counts of databases, MCP servers, skills, pipelines, and steering files.
- **Resources by category**: All resources grouped by category with status indicators.
- **Quick-access links**: Direct links to resource details and tool invocations.
- **Credential instructions**: Setup guidance for resources that need authentication.

## Cross-Database Search

The cross-database search skill orchestrates parallel queries across multiple installed MCP servers, grouping results by database.

### Search Types

| Search Type | Databases Queried |
|-------------|-------------------|
| `gene` | NCBI Gene, UniProt, Ensembl, ClinVar, OMIM, GO, KEGG, Reactome, Allen Brain Atlas, IEDB, CellxGene |
| `drug` | DrugBank, ChEMBL, PharmGKB, OpenTargets, PubChem, HMDB, CARD |
| `protein` | UniProt, PDB, AlphaFold DB, InterPro, STRING, neXtProt, ESM, abYsis |
| `species` | GBIF, IUCN Red List, BOLD, iNaturalist, NCBI Taxonomy, MGnify |
| `metabolite` | HMDB, MetaboLights, METLIN, MassBank, PubChem, KEGG |
| `cell_type` | CellxGene, Single Cell Expression Atlas, Cell Atlas, Allen Brain Atlas |

### How It Works

1. You specify a query and search type (e.g., "BRCA1" with type "gene").
2. The skill identifies all databases mapped to that search type.
3. Each database is queried in parallel with a 10-second timeout.
4. Results are grouped by database — no duplicates.
5. Databases that are not installed, missing credentials, or experiencing errors are reported separately with reason codes.
6. You get results from all successful databases even when some fail.

### Graceful Degradation

The search handles failures gracefully:
- **not_installed**: MCP server not configured in `mcp.json`.
- **credentials_missing**: Server installed but required credentials not configured.
- **api_error**: Database returned an error response.
- **timeout**: Database query exceeded the 10-second timeout.

## AWS HealthOmics Integration

The existing `aws-healthomics` Power is included as a peer dependency. It provides tools for:

- **Workflow management**: Create, list, get, and version workflows.
- **Run management**: Start, monitor, list, and diagnose workflow runs.
- **Performance analysis**: Analyze run performance and generate timeline visualizations.
- **Genomics file search**: Search for FASTQ, BAM, VCF, and other genomics files across S3 and sequence stores.
- **Container management**: Check, clone, and grant HealthOmics access to ECR containers.
- **Sequence stores**: Create, list, and manage sequence stores and read sets.
- **Reference stores**: Manage reference genomes and import jobs.

The variant calling and pipeline import steering files reference HealthOmics tools directly for end-to-end genomics workflows.

## Complete mcp.json Example

Here's a full `mcp.json` configuration with all 25 MCP servers:

```json
{
  "mcpServers": {
    "life-sciences-genomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-genomics", "life-sciences-genomics"],
      "env": { "NCBI_API_KEY": "${secret:ncbi-api-key}" }
    },
    "life-sciences-proteomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-proteomics", "life-sciences-proteomics"]
    },
    "life-sciences-structural": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-structural", "life-sciences-structural"]
    },
    "life-sciences-pathways": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-pathways", "life-sciences-pathways"]
    },
    "life-sciences-ontologies": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-ontologies", "life-sciences-ontologies"]
    },
    "life-sciences-clinical": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-clinical", "life-sciences-clinical"],
      "env": {
        "OMIM_API_KEY": "${secret:omim-api-key}",
        "DRUGBANK_API_KEY": "${secret:drugbank-api-key}"
      }
    },
    "life-sciences-model-organisms": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-model-organisms", "life-sciences-model-organisms"]
    },
    "life-sciences-molbio": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-molbio", "life-sciences-molbio"]
    },
    "life-sciences-cheminformatics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cheminformatics", "life-sciences-cheminformatics"],
      "env": { "CHEMSPIDER_API_KEY": "${secret:chemspider-api-key}" }
    },
    "life-sciences-immunology": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-immunology", "life-sciences-immunology"],
      "env": {
        "IMMPORT_USERNAME": "${secret:immport-username}",
        "IMMPORT_PASSWORD": "${secret:immport-password}"
      }
    },
    "life-sciences-microbiology": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-microbiology", "life-sciences-microbiology"]
    },
    "life-sciences-metabolomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-metabolomics", "life-sciences-metabolomics"]
    },
    "life-sciences-epigenomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-epigenomics", "life-sciences-epigenomics"]
    },
    "life-sciences-imaging": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-imaging", "life-sciences-imaging"],
      "env": {
        "OMERO_HOST": "${secret:omero-host}",
        "OMERO_USERNAME": "${secret:omero-username}",
        "OMERO_PASSWORD": "${secret:omero-password}"
      }
    },
    "life-sciences-agriculture": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-agriculture", "life-sciences-agriculture"],
      "env": {
        "PHYTOZOME_USERNAME": "${secret:phytozome-username}",
        "PHYTOZOME_PASSWORD": "${secret:phytozome-password}"
      }
    },
    "life-sciences-ecology": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-ecology", "life-sciences-ecology"],
      "env": { "IUCN_API_KEY": "${secret:iucn-api-key}" }
    },
    "life-sciences-neuroscience": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-neuroscience", "life-sciences-neuroscience"]
    },
    "life-sciences-cellbiology": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cellbiology", "life-sciences-cellbiology"]
    },
    "life-sciences-healthcare": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-healthcare", "life-sciences-healthcare"],
      "env": {
        "FHIR_BASE_URL": "${secret:fhir-base-url}",
        "REDCAP_API_KEY": "${secret:redcap-api-key}",
        "REDCAP_BASE_URL": "${secret:redcap-base-url}"
      }
    },
    "life-sciences-biobanking": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-biobanking", "life-sciences-biobanking"],
      "env": {
        "LIMS_BASE_URL": "${secret:lims-base-url}",
        "LIMS_API_KEY": "${secret:lims-api-key}"
      }
    },
    "life-sciences-pipelines": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-pipelines", "life-sciences-pipelines"]
    },
    "life-sciences-datastandards": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-datastandards", "life-sciences-datastandards"]
    },
    "life-sciences-cloud": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cloud", "life-sciences-cloud"],
      "env": {
        "TERRA_API_KEY": "${secret:terra-api-key}",
        "GALAXY_BASE_URL": "${secret:galaxy-base-url}",
        "GALAXY_API_KEY": "${secret:galaxy-api-key}"
      }
    },
    "life-sciences-aiml": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-aiml", "life-sciences-aiml"]
    },
    "life-sciences-cancergenomics": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/aws-samples/sample-kiro-power-life-sciences#subdirectory=life-sciences-cancergenomics", "life-sciences-cancergenomics"]
    }
  }
}
```

You don't need to install all 25 servers. Add only the ones relevant to your work. The resource catalog and dashboard will show the status of all servers regardless of which are installed.
