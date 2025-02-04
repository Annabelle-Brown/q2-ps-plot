# q2-ps-plot
Qiime2 Plug-in for the creation of visualizations from PepSIRF outputs.

### Table of Contents
- [Installation](https://github.com/LadnerLab/q2-ps-plot#installation)

- [Tutorial](https://github.com/LadnerLab/q2-ps-plot#tutorial)

- [Usage](https://github.com/LadnerLab/q2-ps-plot#usage)

## Installation

### Qiime2 Installation:
Visit: https://docs.qiime2.org/2021.8/install/ for intallation documentation on Qiime2

### PepSIRF Installation:
Visit: https://github.com/LadnerLab/PepSIRF for installation documentation on PepSIRF

### q2-ps-plot Installation:
#### Dependencies:
- `qiime2`
- `PepSIRF`
- `altair`

#### Directions:
Make sure your Qiime2 conda environment is activated by running the command:
  
```
conda activate qiime2-2021.8
```

You can replace `qiime2-2021.8` above with whichever version of QIIME 2 you have currently installed.

Now you are ready to install ps-plot. Run the following commands:

```
pip install altair
pip install git+https://github.com/LadnerLab/q2-ps-plot.git
```

Run `qiime info` to check for a successful installation. If installation was successful, you should see `ps-plot: version` in the list of installed plugins.

## Tutorial
File inputs for tutorial located in q2-ps-plot/example

### Running zenrich
Download the following files:

- IM0032-pA_PV1_subset_CS.qza
- IM0032-pA_PV1_subset_Z-HDI95.qza
- pairs_source.tsv

Run the following command:

```
qiime ps-plot zenrich --i-data IM0032-pA_PV1_subset_CS.qza \
--i-zscores IM0032-pA_PV1_subset_Z-HDI95.qza \
--m-source-file pairs_source.tsv \
--m-source-column Source \
--p-negative-controls SB_pA_A SB_pA_B SB_pA_D \
--o-visualization testing_zenrich
```

*If you cannot run PepSIRF by simply calling 'pepsirf' in the command line, you need to add `--p-pepsirf-binary` to the above command, followed by how you can call PepSIRF on your system*

Once ps-plot has finished running you should see: `Saved Visualization to: testing_zenrich.qzv`

You can view this visualization by dropping the `testing_zenrich.qzv` file into https://view.qiime2.org/.

### Running zenrich-tsv
Download the following files:

- IM0032-pA_PV1_subset_CS.tsv
- IM0032-pA_PV1_subset_Z-HDI95.tsv
- pairs_source.tsv

Run the following command:

```
qiime ps-plot zenrich-tsv --p-data-filepath IM0032-pA_PV1_subset_CS.tsv \
--p-zscores-filepath IM0032-pA_PV1_subset_Z-HDI95.tsv \
--m-source-file pairs_source.tsv \
--m-source-column Source \
--p-negative-controls SB_pA_A SB_pA_B SB_pA_D \
--o-zenrich-vis testing_zenrich_tsv
```

*If you cannot run PepSIRF by simply calling 'pepsirf' in the command line, you need to add `--p-pepsirf-binary` to the above command, followed by how you can call PepSIRF on your system*

Once ps-plot has finished running you should see: `Saved Visualization to: testing_zenrich_tsv.qzv`

You can view this visualization by dropping the `testing_zenrich_tsv.qzv` file into https://view.qiime2.org/.

## Usage

### zenrich Arguments
| Optional/Required | Argument(s) | Description | Example | Default |
| :--: | :------: | --- | --- | -- |
| **Required** | `--i-data` | Featuretable[Normed] - FeatureTable containing normalized read counts of samples and peptides. First column header must be 'Sequence Name' as produced by pepsirf. | **--i-data** some_file.qza | N/A |
| **Required** | `--i-zscores` | Featuretable[Zscore] - FeatureTable containing z scores of the normalized read counts. Fist column header must be 'Sequence Name' as produced by pepsirf. | **--i-zscores** some_file.qza | N/A |
| *Optional* | `--i-negative-data` | Featuretable[Normed] - FeatureTable containing normalized read counts of controls and peptides. First column header must be 'Sequence Name' as produced by pepsirf. | **-i-negative-data** some_file.qza | None |
| **Required** | `--m-source-file` | Metadata file containing all sample names and their source groups. Used to create pairs tsv to run pepsirf enrich module. | **--m-source-file** some_file.tsv | N/A |
| **Required** | `--m-source-column` | Name of column to collect source info from. | **--m-source-column** Source | N/A |
| *Optional* | `--m-peptide-metadata-file` | Filename of file that contains peptide metadata related to data to be plotted. | **--m-peptide-metadata-file** some_file.tsv | None |
| **Required** | `--p-negative-controls` | Sample names of the negative controls to be used. | **--p-negative-controls** sample1 sample2 sample3 | N/A |
| *Optional* | `--p-tooltip` | List of title names found in the peptide metadata file to be added to the hover tooltip (Parameter is case sensitive).  'Peptide' and 'Zscores' will always be added to the list of titles, if peptide metadata is not provided just 'Peptide' and 'Zscores' will be shown. | **--p-tooltip** Species SpeciesID | **['Species', 'SpeciesID']** or None |
| *Optional* | `--p-step-z-thresh` | Integar to increment z-score thresholds. | **--p-step-z-thresh** 1 | **5** |
| *Optional* | `--p-upper-z-thresh` | Upper limit of z-score thresholds (non-inclusive). | **--p-upper-z-thresh** 10 | **30** |
| *Optional* | `--p-lower-z-thresh` | Lower limit of z-score thresholds (inclusive). | **--p-lower-z-thresh** 5 | **5** |
| *Optional* | `--p-exact-z-thresh` | List of exact z score thresholds either individual or combined. List MUST BE in descending order. | **--p-exact-z-thresh** 25 10 3 *or* **--p-exact-z-thresh** 6,25 4,10 1,3 | None |
| *Optional* | `--p-pepsirf-binary` | The binary to call pepsirf on your system. Used to call pepsirf enrich module. | **--p-pepsirf-binary** pepsirf_executable | **'pepsirf'** |
| **Required** | `--o-visualization` | Visualization output name | **--o-visualization** file_name.qzv | N/A |
| *Optional* | `--output-dir` | Output unspecified results to a directory | **--output-dir** directory_name | **Current Working Directory** |

### zenrich_tsv Arguments
| Optional/Required | Argument(s) | Description | Example | Default |
| :--: | :------: | --- | --- | -- |
| **Required** | `--p-data-filepath` | Filepath of .tsv file containing normalized read counts of samples and peptides. First column header must be 'Sequence Name' as produced by pepsirf. | **--p-data-filepath** some_file.tsv | N/A |
| **Required** | `--p-zscores-filepath` | Filepath of .tsv file containing z scores of the normalized read counts. Fist column header must be 'Sequence Name' as produced by pepsirf. | **--p-zscores-filepath** some_file.tsv | N/A |
| *Optional* | `--p-negative-data-filepath` | Filepath of .tsv file containing normalized read counts of controls and peptides. First column header must be 'Sequence Name' as produced by pepsirf. | **-p-negative-data-filepath** some_file.tsv | None |
| **Required** | `--m-source-file` | Metadata file containing all sample names and their source groups. Used to create pairs tsv to run pepsirf enrich module. | **--m-source-file** some_file.tsv | N/A |
| **Required** | `--m-source-column` | Name of column to collect source info from. | **--m-source-column** Source | N/A |
| *Optional* | `--m-peptide-metadata-file` | Filename of file that contains peptide metadata related to data to be plotted. | **--m-peptide-metadata-file** some_file.tsv | None |
| **Required** | `--p-negative-controls` | Sample names of the negative controls to be used. | **--p-negative-controls** sample1 sample2 sample3 | N/A |
| *Optional* | `--p-tooltip` | List of title names found in the peptide metadata file to be added to the hover tooltip (Parameter is case sensitive).  'Peptide' and 'Zscores' will always be added to the list of titles, if peptide metadata is not provided just 'Peptide' and 'Zscores' will be shown. | **--p-tooltip** Species SpeciesID | **['Species', 'SpeciesID']** or None |
| *Optional* | `--p-step-z-thresh` | Integar to increment z-score thresholds. | **--p-step-z-thresh** 1 | **5** |
| *Optional* | `--p-upper-z-thresh` | Upper limit of z-score thresholds (non-inclusive). | **--p-upper-z-thresh** 10 | **30** |
| *Optional* | `--p-lower-z-thresh` | Lower limit of z-score thresholds (inclusive). | **--p-lower-z-thresh** 5 | **5** |
| *Optional* | `--p-exact-z-thresh` | List of exact z score thresholds either individual or combined. List MUST BE in descending order. | **--p-exact-z-thresh** 25 10 3 *or* **--p-exact-z-thresh** 6,25 4,10 1,3 | None |
| *Optional* | `--p-pepsirf-binary` | The binary to call pepsirf on your system. Used to call pepsirf enrich module. | **--p-pepsirf-binary** pepsirf_executable | **'pepsirf'** |
| **Required** | `--o-zenrich-vis` | Visualization output name | **--o-zenrich-vis** file_name.qzv | N/A |
| *Optional* | `--output-dir` | Output unspecified results to a directory | **--output-dir** directory_name | **Current Working Directory** |

### `More visualizers coming soon...`
