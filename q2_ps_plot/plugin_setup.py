#!/usr/bin/env python
import importlib
import q2_ps_plot

from qiime2.plugin import (Plugin,
                        SemanticType,
                        model,
                        Int,
                        Range,
                        MetadataColumn,
                        Categorical,
                        Str,
                        List,
                        Visualization,
                        Metadata,
                        Bool)

from q2_pepsirf.format_types import (
    Normed, Zscore, InfoSumOfProbes, PairwiseEnrichment, InfoSNPN)
import q2_ps_plot.actions as actions
from q2_ps_plot.actions.scatter import repScatters
from q2_ps_plot.actions.boxplot import readCountsBoxplot, enrichmentRCBoxplot

from q2_types.feature_table import FeatureTable, BIOMV210DirFmt


# This is the plugin object. It is what the framework will load and what an
# interface will interact with. Basically every registration we perform will
# involve this object in some way.
plugin = Plugin("ps-plot", version=q2_ps_plot.__version__,
                website="https://github.com/LadnerLab/q2-ps-plot",
                description="Qiime2 Plug-in for the creation of visualizations from PepSIRF outputs.")

# plugin.register_formats(PepsirfContingencyTSVFormat,
#                         PepsirfContingencyTSVDirFmt)

# plugin.register_semantic_types(Normed, Zscore)
# plugin.register_semantic_type_to_format(FeatureTable[Normed | Zscore],
#                                         BIOMV210DirFmt)

shared_parameters = {
    "step_z_thresh": Int % Range(1, None),
    "upper_z_thresh": Int % Range(2, None),
    "lower_z_thresh": Int % Range(1, None),
    "exact_z_thresh": List[Str],
    "exact_cs_thresh": Str,
    "source": MetadataColumn[Categorical],
    "pn_filepath": Str,
    "peptide_metadata": Metadata,
    "pepsirf_binary": Str,
    "negative_controls": List[Str],
    "negative_id": Str,
    "tooltip": List[Str],
    "color_by": Str
}
shared_descriptions = {
    "step_z_thresh": "Integar to increment z-score thresholds.",
    "upper_z_thresh": "Upper limit of z-score thresholds (non-inclusive).",
    "lower_z_thresh": "Lower limit of z-score thresholds (inclusive).",
    "exact_z_thresh": "List of exact z score thresholds either individual or combined. "
                    "List MUST BE in descending order. (Example argument: '--p-exact-z-thresh 25 10 3' "
                    "or '--p-exact-z-thresh 6,25 4,10 1,3')",
    "exact_cs_thresh": "A single col-sum threshold. Default 20.",
    "source": "Metadata file containing all sample names and their source groups. "
            "Used to create pairs tsv to run pepsirf enrich module.",
    "pn_filepath": "Filepath of .tsv pairs file generated by standalone autopepsirf python script, "
                "containing all sample pairings, typically ending in '_PN.tsv'. (Depricated)",
    "peptide_metadata": "Filename of file that contains peptide metadata related to "
                        "data to be plotted.",
    "pepsirf_binary": "The binary to call pepsirf on your system. "
                    "Used to call pepsirf enrich module.",
    "negative_controls": "Sample names of the negative controls to be used "
                        "(Example argument: --p-negative-controls sample1 sample2 sample3).",
    "tooltip": "List of title names found in the peptide metadata file "
                "to be added to the hover tooltip (Parameter is case sensitive. "
                "Example argument: --p-tooltip Species SpeciesID). "
                "'Peptide' and 'Zscores' will always be added to the list of titles, "
                "if peptide metadata is not provided just 'Peptide' and 'Zscores' will be shown.",
    "color_by": "A column within the metadata file to base the coloring of the enriched peptide points. "
                "This parameter is case sensitive and the default is the different zscore thresholds."
}

plugin.pipelines.register_function(
    function=actions.zenrich_tsv,
    inputs={},
    outputs=[
        ("zenrich_vis", Visualization)
    ],
    parameters={
        'data_filepath': Str,
        'zscores_filepath': Str,
        'negative_data_filepath': Str,
        'highlighted_probes_filepath': Str,
        **shared_parameters
    },
    input_descriptions=None,
    output_descriptions=None,
    parameter_descriptions={
        'data_filepath': "Filepath of .tsv file containing normalized read counts of samples and peptides. "
                    "First column header must be 'Sequence Name' as produced by pepsirf.",
        'zscores_filepath': "Filepath of .tsv file containing z scores of the normalized read counts. "
                    "Fist column header must be 'Sequence Name' as produced by pepsirf.",
        'negative_data_filepath':"Filepath of .tsv file containing normalized read counts of controls and peptides. "
                            "First column header must be 'Sequence Name' as produced by pepsirf.",
        'highlighted_probes_filepath': "A InfoSNPN file that contains a list of probes/peptides to highlight.",
        **shared_descriptions
    },
    name='zenrich TSV Pipeline',
    description="Pipeline that converts .tsv files to .qza files and then runs zenrich."
)

plugin.visualizers.register_function(
    function=actions.zenrich,
    inputs={
        'data': FeatureTable[Normed],
        'zscores': FeatureTable[Zscore],
        'negative_data': FeatureTable[Normed],
        'highlight_probes': InfoSNPN
    },
    parameters=shared_parameters,
    input_descriptions={
        'data': "FeatureTable containing normalized read counts of samples and peptides. "
                "First column header must be 'Sequence Name' as produced by pepsirf.",
        'zscores': "FeatureTable containing z scores of the normalized read counts. "
                "Fist column header must be 'Sequence Name' as produced by pepsirf.",
        'negative_data': "FeatureTable containing normalized read counts of controls and peptides. "
                        "First column header must be 'Sequence Name' as produced by pepsirf.",
        'highlight_probes': "A InfoSNPN file that contains a list of probes/peptides to highlight."
    },
    parameter_descriptions=shared_descriptions,
    name='Z Enrichment Variance Visualizer',
    description="Creates a scatterplot of enriched peptides, points are colored "
                "according to the z score thresholds provided. Scatterplot is "
                "layered over a heatmap containing all of the data."
)

plugin.visualizers.register_function(
    function=repScatters,
    inputs={
        'zscore': FeatureTable[Zscore],
        'col_sum': FeatureTable[Normed]
    },
    parameters={
        'source': MetadataColumn[Categorical],
        'plot_log': Bool
    },
    input_descriptions={
        'zscore': "FeatureTable containing z scores of the normalized read counts. "
                "Fist column header must be 'Sequence Name' as produced by pepsirf.",
        'col_sum': "FeatureTable containing normalized read counts of samples and peptides. "
                "First column header must be 'Sequence Name' as produced by pepsirf."
    },
    parameter_descriptions={
        'source': "Metadata file containing all sample names and their source groups. "
            "Used to create pairs tsv to run pepsirf enrich module.",
        'plot_log': "Use if you want axes to be shown on a log-scale."
    },
    name='Rep Scatter',
    description="Creates a scatterplot for reps of Col-sum data or reps of z score data"
)

plugin.visualizers.register_function(
    function=readCountsBoxplot,
    inputs={
        'read_counts':  InfoSumOfProbes
    },
    parameters={
        'png_out_dir': Str
    },
    input_descriptions={
        'read_counts': "InfoSumOfProbes file, The first entry in each column will be the name of the "
                    "sample, and the second will be the sum of the peptide/probe scores for the sample."
    },
    parameter_descriptions={
        'png_out_dir': "The name of the directory to wich to write the .png output files to"
    },
    name='Read Counts BoxPlot',
    description="Creates a boxplot for the read counts/ sum of probes"
)

plugin.visualizers.register_function(
    function=enrichmentRCBoxplot,
    inputs={
        'enriched_dir':  PairwiseEnrichment
    },
    parameters={
        'png_out_dir': Str
    },
    input_descriptions={
        'enriched_dir': "A PairwiseEnrichment semantic type or .qza. This file is the output of "
                    "q2-pepsirf's enrich module"
    },
    parameter_descriptions={
        'png_out_dir': "The name of the directory to wich to write the .png output files to"
    },
    name='Enriched Read Counts BoxPlot',
    description="Creates a boxplot for the read counts of enriched peptides"
)

importlib.import_module("q2_ps_plot.transformers")
