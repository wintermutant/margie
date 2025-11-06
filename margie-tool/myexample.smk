OUTPUT_DIR = config.get("output_dir", "output")
SAMPLE_TO_FASTA = config.get("sample_to_file", {})
SAMPLES = config.get("samples", [])


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