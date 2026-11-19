# Kiro Life Sciences Power - Capabilities Overview

## Executive Summary

The **Kiro Life Sciences Power** is a comprehensive, modular platform that brings together 100+ life sciences databases, 250+ bioinformatics tools, and expert guidance into a unified development environment. Designed for bioinformaticians, clinical researchers, computational biologists, and life sciences professionals, this Power provides seamless access to the entire life sciences data ecosystem—from genomics and proteomics to clinical trials and ecological data.

### What Makes This Unique

- **Modular Architecture**: Install only what you need. Each of the 25 MCP servers is independently deployable via `uvx`, keeping your environment lightweight while providing access to the full ecosystem.
- **Unified Access**: Query 100+ databases through a single interface with consistent authentication, error handling, and result formatting.
- **Cross-Database Intelligence**: Perform parallel searches across multiple databases simultaneously, with automatic result aggregation and graceful degradation.
- **Context-Aware Workflows**: 16 steering files auto-activate based on your workspace files, guiding you through complex multi-step workflows.
- **Expert Guidance**: 10 domain skills provide practical, actionable guidance for common life sciences tasks—from HIPAA compliance to single-cell RNA-seq analysis.
- **AWS HealthOmics Integration**: Seamlessly create, run, and monitor genomics workflows in AWS HealthOmics directly from your IDE.

### At a Glance

| Metric | Count |
|--------|-------|
| **MCP Servers** | 25 modular servers |
| **Databases** | 100+ life sciences databases |
| **Tools** | 250+ bioinformatics tools |
| **Domain Skills** | 10 expert guidance modules |
| **Steering Files** | 16 workflow guides |
| **Resource Categories** | 25 organized domains |
| **Cross-Database Search Types** | 6 intelligent search modes |

---

## 🧬 Complete MCP Server & Database Coverage

This table shows all 25 MCP servers, the databases and tools they provide access to, approximate tool counts, and authentication requirements.

| # | Server Name | Domain | Databases/Tools Covered | Tool Count | Auth Required |
|---|-------------|--------|------------------------|------------|---------------|
| 1 | **life-sciences-genomics** | Genomics & Sequencing | NCBI, Ensembl, ClinVar, GEO, SRA, COSMIC, gnomAD, dbSNP, ENCODE, 1000 Genomes, DDBJ | ~16 | Optional (NCBI), Required (COSMIC) |
| 2 | **life-sciences-proteomics** | Proteomics | UniProt, InterPro, Pfam, STRING, PRIDE, neXtProt | ~18 | No |
| 3 | **life-sciences-structural** | Structural Biology | PDB, AlphaFold DB, CATH, SCOP | ~8 | No |
| 4 | **life-sciences-pathways** | Pathways & Interactions | KEGG, Reactome, BioCyc, WikiPathways, IntAct | ~10 | No |
| 5 | **life-sciences-ontologies** | Ontologies | Gene Ontology, HPO, Disease Ontology | ~7 | No |
| 6 | **life-sciences-clinical** | Clinical & Pharma | OMIM, DrugBank, ChEMBL, PharmGKB, OpenTargets, FDA FAERS, ClinicalTrials.gov | ~20 | Required (OMIM, DrugBank) |
| 7 | **life-sciences-model-organisms** | Model Organisms | FlyBase, WormBase, ZFIN, MGI, SGD | ~10 | No |
| 8 | **life-sciences-molbio** | Molecular Biology | BLAST, Clustal Omega, MUSCLE, HMMER, Primer3, PrimerBLAST, REBASE | ~15 | No |
| 9 | **life-sciences-cheminformatics** | Computational Chemistry | PubChem, ChemSpider, ZINC, RDKit, AutoDock, SwissDock, ADMET | ~15 | Required (ChemSpider) |
| 10 | **life-sciences-immunology** | Immunology | IEDB, ImmPort, IMGT, abYsis | ~10 | Required (ImmPort) |
| 11 | **life-sciences-microbiology** | Microbiology & Metagenomics | SILVA, Greengenes, QIIME 2, MG-RAST, BV-BRC, CARD | ~12 | No |
| 12 | **life-sciences-metabolomics** | Metabolomics | HMDB, MetaboLights, METLIN, MassBank | ~8 | No |
| 13 | **life-sciences-epigenomics** | Epigenomics | IHEC, Roadmap Epigenomics, MethBase | ~6 | No |
| 14 | **life-sciences-imaging** | Imaging & Microscopy | OMERO, CellProfiler, ImageJ, DICOM, BioImage Archive, IDR, EMPIAR | ~14 | Required (OMERO) |
| 15 | **life-sciences-agriculture** | Agricultural & Plant Biology | Phytozome, TAIR, Gramene, PlantGDB | ~9 | Required (Phytozome) |
| 16 | **life-sciences-ecology** | Ecology & Environmental | GBIF, BOLD, iNaturalist, IUCN Red List, GenBank Env, MGnify | ~15 | Required (IUCN) |
| 17 | **life-sciences-neuroscience** | Neuroscience | Allen Brain Atlas, NeuroMorpho, OpenNeuro, BrainMap | ~8 | No |
| 18 | **life-sciences-cellbiology** | Cell Biology | Cell Atlas, CellxGene, Single Cell Expression Atlas | ~7 | No |
| 19 | **life-sciences-healthcare** | Healthcare Standards | FHIR, HL7 v2, OMOP CDM, REDCap, DICOMweb | ~15 | Required (FHIR, REDCap) |
| 20 | **life-sciences-biobanking** | Biobanking & Sample Mgmt | BBMRI, BioSample, LIMS (SiLA 2), Sample Inventory, protocols.io | ~10 | Required (LIMS) |
| 21 | **life-sciences-pipelines** | Pipelines | nf-core, WDL, CWL, GitHub pipeline index | ~8 | No |
| 22 | **life-sciences-datastandards** | Data Standards & Formats | MAGE-TAB, ISA-Tab, SBML, BioPAX | ~9 | No |
| 23 | **life-sciences-cloud** | Cloud & HPC | AWS Batch, Terra, Galaxy | ~12 | Required (Terra), Optional (Galaxy) |
| 24 | **life-sciences-aiml** | AI/ML for Life Sciences | ESM, AlphaFold predictions, BioNLP | ~10 | No |
| 25 | **life-sciences-cancergenomics** | Cancer Genomics | cBioPortal | ~7 | No |

**Total: ~250+ tools across 100+ databases**

---

## 🎯 Domain Skills (10 Expert Guidance Modules)

Skills provide context-specific, practical guidance for common life sciences tasks. Activate them manually when you need domain expertise.

| # | Skill Name | Focus Area | Key Topics Covered |
|---|------------|------------|-------------------|
| 1 | **bioinformatics-file-formats** | File Formats & Standards | FASTA, FASTQ, BAM, VCF, GFF, BED, DICOM, SBML, BioPAX, MAGE-TAB, ISA-Tab with parsing examples and best practices |
| 2 | **genomics-pipeline-best-practices** | Pipeline Design & Optimization | WDL/Nextflow/CWL workflow patterns, CPU/memory/storage optimization, error handling, checkpointing, reproducibility |
| 3 | **data-compliance** | Regulatory & Data Governance | HIPAA, GDPR, GxP, MIAME, MINSEQE compliance, data classification, de-identification, consent management, audit trails |
| 4 | **clinical-interoperability** | Clinical Data Exchange | FHIR resource modeling, HL7 v2 message construction, OMOP CDM mapping, terminology services (SNOMED CT, LOINC, ICD) |
| 5 | **ecological-data-analysis** | Ecology & Biodiversity | Species distribution modeling, biodiversity metrics (Shannon, Simpson), environmental DNA analysis, occurrence data handling |
| 6 | **cheminformatics-best-practices** | Drug Discovery & Chemistry | SMILES, InChI, MOL formats, molecular property calculation, Lipinski rules, SAR analysis, virtual screening workflows |
| 7 | **biomedical-imaging** | Image Analysis & Microscopy | Image preprocessing, segmentation algorithms (Otsu, watershed, U-Net), feature extraction, DICOM handling, microscopy pipelines |
| 8 | **immunology-vaccine-design** | Immunology & Vaccines | Epitope prediction workflows, MHC binding analysis, antibody engineering patterns, immunogenicity assessment |
| 9 | **metabolomics-analysis** | Metabolomics & Mass Spec | Metabolite identification (MSI levels), spectral matching, pathway enrichment, statistical analysis, normalization methods |
| 10 | **single-cell-analysis** | Single-Cell Genomics | QC metrics, normalization (scran, SCTransform), clustering (Leiden, Louvain), differential expression, trajectory inference (Monocle, PAGA) |

---

## 🗺️ Steering Files (16 Workflow Guides)

Steering files are step-by-step workflow guides that auto-activate based on file patterns in your workspace, providing contextual guidance for complex multi-step tasks.

| # | Steering File | Workflow Description | Auto-Activates On |
|---|---------------|---------------------|-------------------|
| 1 | **variant-calling-pipeline** | Create HealthOmics workflow, configure inputs, start run, monitor progress, and analyze results | `*.wdl`, `*.nf`, `*.cwl` |
| 2 | **gene-disease-associations** | Cross-reference ClinVar → OMIM → HPO → Disease Ontology for comprehensive gene-disease links | `*clinvar*`, `*variant*`, `*disease*` |
| 3 | **protein-structure-analysis** | Search PDB → AlphaFold → CATH → UniProt for comprehensive structural and functional analysis | `*protein*`, `*structure*`, `*pdb*` |
| 4 | **pipeline-import-healthomics** | Import nf-core/WDL pipeline → package dependencies → create HealthOmics workflow → run | `*.wdl`, `*.nf`, `*.cwl`, `nextflow.config` |
| 5 | **resource-catalog-browsing** | Discover, search, filter, and browse the complete life sciences resource catalog | Always available |
| 6 | **fhir-clinical-integration** | Connect to FHIR server → query clinical resources → map to OMOP CDM for analytics | `*fhir*`, `*clinical*`, `*omop*`, `*hl7*` |
| 7 | **species-distribution-analysis** | GBIF occurrences → IUCN conservation status → iNaturalist observations → distribution modeling | `*species*`, `*occurrence*`, `*gbif*` |
| 8 | **metabolite-identification** | HMDB search → MetaboLights datasets → MassBank spectral matching for metabolite ID | `*metabol*`, `*hmdb*`, `*massbank*` |
| 9 | **microbiome-analysis** | SILVA taxonomy → QIIME 2 pipeline → MG-RAST functional annotation | `*microbiome*`, `*16s*`, `*metagenom*` |
| 10 | **compound-screening** | PubChem search → RDKit molecular descriptors → ZINC filtering → molecular docking | `*compound*`, `*screen*`, `*smiles*`, `*drug*` |
| 11 | **biomedical-image-analysis** | OMERO import → CellProfiler segmentation pipeline → ImageJ quantitative analysis | `*image*`, `*microscop*`, `*dicom*`, `*.tif` |
| 12 | **molecular-docking** | PDB structure retrieval → ligand preparation → SwissDock docking → analyze binding poses | `*dock*`, `*ligand*`, `*binding*` |
| 13 | **primer-design-cloning** | Primer3 design → PrimerBLAST specificity check → REBASE restriction sites → cloning strategy | `*primer*`, `*clone*`, `*restriction*` |
| 14 | **single-cell-rnaseq** | CellxGene datasets → expression analysis → cell type annotation and visualization | `*single*cell*`, `*scrnaseq*`, `*10x*` |
| 15 | **epigenomics-analysis** | IHEC epigenomic data → Roadmap chromatin states → ENCODE integration and analysis | `*epigenom*`, `*methylat*`, `*chromatin*` |
| 16 | **amr-analysis** | CARD resistance gene search → BV-BRC genome analysis → antimicrobial resistance profiling | `*resistance*`, `*amr*`, `*antibiotic*` |

---

## 🔐 Authentication & Credentials Reference

Some databases require API keys or authentication. This table shows all credential requirements and how to obtain them.

| Database/Service | Credentials Needed | Required? | How to Obtain |
|------------------|-------------------|-----------|---------------|
| **NCBI** | `NCBI_API_KEY` | Optional (increases rate limit from 3 to 10 req/sec) | [NCBI Account Settings](https://www.ncbi.nlm.nih.gov/account/settings/) |
| **COSMIC** | `COSMIC_API_KEY` | Required for COSMIC access | [COSMIC Registration](https://cancer.sanger.ac.uk/cosmic/register) |
| **OMIM** | `OMIM_API_KEY` | Required for OMIM access | [OMIM API Access](https://www.omim.org/api) |
| **DrugBank** | `DRUGBANK_API_KEY` | Required for DrugBank access | [DrugBank API](https://go.drugbank.com/api) |
| **ChemSpider** | `CHEMSPIDER_API_KEY` | Required for ChemSpider access | [ChemSpider Developer](https://developer.rsc.org/) |
| **ImmPort** | `IMMPORT_USERNAME`, `IMMPORT_PASSWORD` | Required for ImmPort access | [ImmPort Registration](https://www.immport.org/registration) |
| **IUCN Red List** | `IUCN_API_KEY` | Required for IUCN access | [IUCN API](https://apiv3.iucnredlist.org/) |
| **FHIR Server** | `FHIR_BASE_URL` | Required for FHIR access | Your organization's FHIR endpoint |
| **REDCap** | `REDCAP_API_KEY`, `REDCAP_BASE_URL` | Required for REDCap access | Your institution's REDCap admin |
| **OMERO** | `OMERO_HOST`, `OMERO_USERNAME`, `OMERO_PASSWORD` | Required for OMERO server access | Your OMERO server administrator |
| **LIMS** | `LIMS_BASE_URL`, `LIMS_API_KEY` | Required for LIMS integration | Your LIMS administrator |
| **Phytozome** | `PHYTOZOME_USERNAME`, `PHYTOZOME_PASSWORD` | Required for Phytozome access | [Phytozome Registration](https://phytozome-next.jgi.doe.gov/) |
| **Terra** | `TERRA_API_KEY` | Required for Terra platform access | [Terra Platform](https://app.terra.bio/) |
| **Galaxy** | `GALAXY_BASE_URL`, `GALAXY_API_KEY` | Optional for Galaxy server access | Your Galaxy server admin panel |

**Credential Management**: All credentials are configured in `mcp.json` using the `${secret:key-name}` syntax. Kiro's secret management resolves these at runtime—credentials are never written to project files or version control.

---

## 📂 Resource Categories (26 Organized Domains)

All databases, tools, and resources are organized into 26 categories for easy discovery and browsing:

| # | Category | Representative Databases/Tools |
|---|----------|-------------------------------|
| 1 | **Genomics and Sequencing** | NCBI, Ensembl, ClinVar, GEO, SRA, COSMIC, gnomAD, dbSNP, ENCODE, 1000 Genomes, DDBJ |
| 2 | **Proteomics** | UniProt, InterPro, Pfam, STRING, PRIDE, neXtProt |
| 3 | **Structural Biology** | PDB, AlphaFold DB, CATH, SCOP |
| 4 | **Pathways and Interactions** | KEGG, Reactome, BioCyc, WikiPathways, IntAct |
| 5 | **Ontologies** | Gene Ontology, HPO (Human Phenotype Ontology), Disease Ontology |
| 6 | **Clinical and Pharma** | OMIM, DrugBank, ChEMBL, PharmGKB, OpenTargets, FDA FAERS, ClinicalTrials.gov |
| 7 | **Model Organisms** | FlyBase (Drosophila), WormBase (C. elegans), ZFIN (Zebrafish), MGI (Mouse), SGD (Yeast) |
| 8 | **Molecular Biology and Biochemistry** | BLAST, Clustal Omega, MUSCLE, HMMER, Primer3, PrimerBLAST, REBASE |
| 9 | **Computational Chemistry and Drug Discovery** | PubChem, ChemSpider, ZINC, RDKit, AutoDock, SwissDock, ADMET prediction |
| 10 | **Immunology** | IEDB (Immune Epitope Database), ImmPort, IMGT, abYsis |
| 11 | **Microbiology and Metagenomics** | SILVA, Greengenes, QIIME 2, MG-RAST, BV-BRC, CARD (Antibiotic Resistance) |
| 12 | **Metabolomics** | HMDB (Human Metabolome Database), MetaboLights, METLIN, MassBank |
| 13 | **Epigenomics** | IHEC, Roadmap Epigenomics, MethBase |
| 14 | **Imaging and Microscopy** | OMERO, CellProfiler, ImageJ, DICOM, BioImage Archive, IDR, EMPIAR |
| 15 | **Agricultural and Plant Biology** | Phytozome, TAIR (Arabidopsis), Gramene, PlantGDB |
| 16 | **Ecology and Environmental Biology** | GBIF, BOLD, iNaturalist, IUCN Red List, GenBank Environmental, MGnify |
| 17 | **Neuroscience** | Allen Brain Atlas, NeuroMorpho, OpenNeuro, BrainMap |
| 18 | **Cell Biology** | Cell Atlas, CellxGene, Single Cell Expression Atlas |
| 19 | **Healthcare Standards** | FHIR, HL7 v2, OMOP CDM, REDCap, DICOMweb |
| 20 | **Biobanking and Sample Management** | BBMRI, BioSample, LIMS (SiLA 2), Sample Inventory, protocols.io |
| 21 | **Pipelines** | nf-core, WDL workflows, CWL workflows, GitHub community pipelines |
| 22 | **Bioinformatics Analysis Tools** | BLAST, sequence alignment tools, primer design, restriction analysis |
| 23 | **Data Standards and Formats** | MAGE-TAB, ISA-Tab, SBML, BioPAX |
| 24 | **Cloud and HPC** | AWS Batch, Terra (Broad Institute), Galaxy |
| 25 | **AI/ML for Life Sciences** | ESM (protein language models), AlphaFold predictions, BioNLP |
| 26 | **Cancer Genomics** | cBioPortal (studies, molecular profiles, clinical data, tumor mutation burden) |

---

## 🔍 Cross-Database Search Intelligence

The cross-database search feature orchestrates parallel queries across multiple installed MCP servers, automatically aggregating results and handling failures gracefully.

### Search Types & Database Coverage

| Search Type | Databases Queried in Parallel |
|-------------|------------------------------|
| **gene** | NCBI Gene, UniProt, Ensembl, ClinVar, OMIM, Gene Ontology, KEGG, Reactome, Allen Brain Atlas, IEDB, CellxGene |
| **drug** | DrugBank, ChEMBL, PharmGKB, OpenTargets, PubChem, HMDB, CARD |
| **protein** | UniProt, PDB, AlphaFold DB, InterPro, STRING, neXtProt, ESM, abYsis |
| **species** | GBIF, IUCN Red List, BOLD, iNaturalist, NCBI Taxonomy, MGnify |
| **metabolite** | HMDB, MetaboLights, METLIN, MassBank, PubChem, KEGG |
| **cell_type** | CellxGene, Single Cell Expression Atlas, Cell Atlas, Allen Brain Atlas |

### How It Works

1. **Specify Query**: Provide a search term and type (e.g., "BRCA1" with type "gene")
2. **Parallel Execution**: All relevant databases are queried simultaneously with 10-second timeout per database
3. **Result Aggregation**: Results are grouped by database with no duplicates
4. **Graceful Degradation**: Databases that fail (not installed, missing credentials, API errors, timeouts) are reported separately with reason codes
5. **Partial Success**: You get results from all successful databases even when some fail

### Error Handling

| Status | Meaning |
|--------|---------|
| `not_installed` | MCP server not configured in `mcp.json` |
| `credentials_missing` | Server installed but required credentials not configured |
| `api_error` | Database returned an error response |
| `timeout` | Database query exceeded the 10-second timeout |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Kiro IDE                              │
├─────────────────────────────────────────────────────────────┤
│              kiro-life-sciences Power (Hub)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │  Dashboard   │ │   Catalog    │ │ Credential Mgr   │    │
│  │  (Status &   │ │  (Search &   │ │ (Unified Auth)   │    │
│  │   Setup)     │ │   Browse)    │ │                  │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │
│  │   Skills     │ │   Steering   │ │ Bundle Manifest  │    │
│  │  (10 Expert  │ │  (16 Workflow│ │ (Declarative     │    │
│  │   Guides)    │ │   Guides)    │ │  Registry)       │    │
│  └──────────────┘ └──────────────┘ └──────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│         Modular MCP Servers (via uvx - Install as Needed)   │
│  genomics · proteomics · structural · pathways · ontologies │
│  clinical · model-organisms · molbio · cheminformatics ...  │
├─────────────────────────────────────────────────────────────┤
│            Peer Power: aws-healthomics                       │
│  (Genomics workflow management in AWS HealthOmics)           │
└─────────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

- **Modular by Design**: The Power hub doesn't contain MCP server implementations—it knows about all 25 servers declaratively through the bundle manifest
- **Install What You Need**: Each MCP server is independently deployable via `uvx`. Install only the domains relevant to your work
- **Unified Interface**: Consistent authentication, error handling, and result formatting across all databases
- **Graceful Degradation**: The system works even when only a subset of servers is installed
- **Status Awareness**: The dashboard and catalog show real-time status of all resources (ready, needs credentials, needs setup)

---

## 🚀 Getting Started

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

---

## 🎯 Key Features & Benefits

### ✅ Comprehensive Coverage
- **100+ databases** spanning genomics, proteomics, clinical, ecology, neuroscience, and more
- **250+ tools** for bioinformatics analysis, molecular biology, drug discovery, and data standards
- **25 organized categories** for easy discovery and navigation

### ✅ Modular & Lightweight
- Install only the MCP servers you need
- Each server is independently deployable via `uvx`
- No bloat—keep your environment lean while maintaining access to the full ecosystem

### ✅ Intelligent Search & Discovery
- **Cross-database search** queries multiple databases in parallel
- **Automatic result aggregation** with no duplicates
- **Graceful degradation** when databases are unavailable
- **Searchable resource catalog** with relevance ranking

### ✅ Expert Guidance
- **10 domain skills** provide practical, actionable guidance
- **16 steering files** auto-activate based on workspace context
- Step-by-step workflows for complex multi-database tasks

### ✅ Unified Authentication
- Centralized credential management via `mcp.json`
- Secure `${secret:key-name}` syntax
- Never write credentials to project files or version control

### ✅ AWS HealthOmics Integration
- Create, run, and monitor genomics workflows in AWS HealthOmics
- Import nf-core and WDL pipelines directly
- Performance analysis and timeline visualizations

### ✅ Production-Ready
- Consistent error handling across all databases
- Timeout protection (10-second default per database)
- Status tracking (ready, needs credentials, needs setup)
- Onboarding dashboard with setup guidance

---

## 📖 Use Cases

### Genomics Research
- Search NCBI, Ensembl, and ClinVar for gene variants
- Cross-reference with OMIM for disease associations
- Import and run variant calling pipelines in AWS HealthOmics
- Analyze results with Gene Ontology and pathway enrichment

### Drug Discovery
- Search PubChem and ChemSpider for compounds
- Calculate molecular descriptors with RDKit
- Perform virtual screening with ZINC database
- Run molecular docking with SwissDock
- Check drug-gene interactions in PharmGKB

### Clinical Research
- Query FHIR servers for patient data
- Map to OMOP CDM for analytics
- Search ClinicalTrials.gov for relevant trials
- Analyze adverse events from FDA FAERS

### Proteomics & Structural Biology
- Search UniProt for protein sequences
- Retrieve predicted structures from AlphaFold DB
- Analyze protein domains with InterPro and Pfam
- Explore protein-protein interactions with STRING

### Ecology & Conservation
- Query GBIF for species occurrence data
- Check IUCN Red List conservation status
- Analyze biodiversity with iNaturalist observations
- Model species distributions

### Single-Cell Genomics
- Browse CellxGene datasets
- Perform QC and normalization
- Cluster cells and identify cell types
- Trajectory inference and differential expression

---

## 📚 Additional Resources

- **POWER.md**: Complete documentation with setup instructions and examples
- **Resource Catalog**: Searchable index of all databases, tools, and resources
- **Onboarding Dashboard**: Post-installation summary with status indicators
- **Skills Directory**: `kiro-life-sciences/skills/` - 10 expert guidance modules
- **Steering Files**: Auto-activating workflow guides for common tasks

---

## 🤝 Support & Contribution

For issues, feature requests, or contributions, please refer to the main Kiro Life Sciences Power repository.

---

**Last Updated**: May 2026  
**Version**: 1.0  
**License**: See main Power documentation
