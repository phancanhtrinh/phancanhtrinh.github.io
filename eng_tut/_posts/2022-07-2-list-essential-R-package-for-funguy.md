---
layout: post
title: Essential R packages for fungal guy
author: TrinhPHAN
link: 
---


1. [EuPathDB](https://bioconductor.org/packages/release/data/annotation/html/EuPathDB.html): Provides access to pathogen annotation resources available on EuPathDB databases

This package helps us to retrieve annotation data from EuPathDB. 

2. [AnnotationForge](https://bioconductor.org/packages/3.15/bioc/html/AnnotationForge.html): Tools for building SQLite-based annotation data packages

Databases for fungal pathogens were provided on different platforms, we need a way to make it compatible to input into other analysis packages. Annotation Forge is a robust tool for this task.

3. [AnnotationHub](https://bioconductor.org/packages/release/bioc/html/AnnotationHub.html): Client to access AnnotationHub resources

The Bioconductor team wants to collect popular web resources into their package called AnnotationHub. This beneficial tool provides genomic and transcriptomic profiles for many applications. 

4. [Biomart](https://bioconductor.org/packages/release/bioc/html/biomaRt.html): Interface to BioMart databases (i.e. Ensembl)

This tool provides a way to access BioMart (Ensembl) annotation database directly from R. This is very useful to query annotation data from Ensembl.

5. [clusterProfiler](https://bioconductor.org/packages/release/bioc/html/clusterProfiler.html): A universal enrichment tool for interpreting omics data

This package provides an interface for functional annotation using data from various sources. They also provide excellent functions to visualize enrichment results obtained from its analysis.
