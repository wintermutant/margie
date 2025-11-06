# configfile: "profiles/default/config.yaml

OUTPUT_DIR = config.get("output_dir", "output")
SAMPLE_TO_FASTA = config.get("sample_to_file", {})
SAMPLES = config.get("samples", [])

# Default rule - defines what outputs we want
rule all:
    input:
        expand(f"{OUTPUT_DIR}/{{sample}}.db", sample=SAMPLES)


rule make_db:
    """Create a genome database from FASTA file using sample wildcard."""
    message:
        "Creating genome database from FASTA: {input.fasta} -> {output.db_file}"
    input:
        fasta = lambda wildcards: SAMPLE_TO_FASTA[wildcards.sample]
    output:
        db_file = f"{OUTPUT_DIR}/{{sample}}.db"
    log:
        f"{OUTPUT_DIR}/logs/{{sample}}_make_db.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        echo "Starting"
        mkdir -p {OUTPUT_DIR}/logs {OUTPUT_DIR}/benchmarks
        # Placeholder for making the db
        echo "Sample: {wildcards.sample}" > {output.db_file}
        echo "Input FASTA: {input.fasta}" >> {output.db_file}
        echo "This is a sqlite3 db for {wildcards.sample}" >> {output.db_file}
        """

rule run_hmmer:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        hmmer_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_hmmer"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_hmmer.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.hmmer_token}
        """

rule run_prodigal:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        hmmer_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_prodigal"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_prodigal.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.hmmer_token}
        """

rule run_tigr:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        tigr_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_tigr"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_tigr.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.tigr_token}
        """

rule run_kegg:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        kegg_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_kegg"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_kegg.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.kegg_token}
        """

rule run_cog:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        cog_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_cog"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_cog.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.cog_token}
        """

rule run_pfam:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        pfam_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_pfam"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_pfam.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    # benchmark:
    #     f"{OUTPUT_DIR}/benchmarks/{{sample}}_{{rule}}.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.pfam_token}
        """

rule run_cazyme:
    """TODO"""
    message:
        "TODO"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db"
    output:
        cazyme_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_cazyme"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_run_cazyme.log"
    resources:
        mem_mb=8000,        # 8GB RAM
        cpus=4,             # 4 CPUs
        slurm_time="02:00:00",  # 2 hours
        slurm_partition="cpu"
    benchmark:
        f"{OUTPUT_DIR}/benchmarks/{{sample}}__run_cazyme.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.cazyme_token}
        """

rule all_annotations:
    """Aggregate all annotations into a single GFF file"""
    message:
        "Aggregating all annotations for sample {wildcards.sample}"
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db",
        hmmer_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_hmmer",
        prodigal_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_prodigal",
        tigr_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_tigr",
        kegg_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_kegg",
        cog_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_cog",
        pfam_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_pfam",
        cazyme_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_cazyme"
    output:
        gff = f"{OUTPUT_DIR}/annotations/agg/{{sample}}.gff"
    log:
        f"{OUTPUT_DIR}/logs/annotations/{{sample}}_all_annotations.log"
    resources:
        mem_mb=4000,        # 4GB RAM
        cpus=2,             # 2 CPUs
        slurm_time="01:00:00",  # 1 hour
        slurm_partition="cpu"
    benchmark:
        f"{OUTPUT_DIR}/benchmarks/{{sample}}__all_annotations.txt"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/annotations/agg {OUTPUT_DIR}/logs/annotations
        #TODO: Implement annotation aggregation
        touch {output.gff}
        """

rule run_operon_tool:
    input:
        db = f"{OUTPUT_DIR}/{{sample}}.db",
    output:
        operon_token = f"{OUTPUT_DIR}/annotations/{{sample}}.run_operon_tool"
    shell:
        """
        mkdir -p {OUTPUT_DIR}/logs/annotations
        touch {output.operon_token}
        """
