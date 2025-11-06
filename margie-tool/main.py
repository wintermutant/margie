#!/usr/bin/env python3

import sqlite3
import argparse
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Generator, Tuple
from pydantic import BaseModel, Field
import yaml

from bioinformatics_tools.file_classes.Fasta import Fasta

def get_fasta_files(inputs):
    """Expand directories and collect all FASTA files."""
    fasta_files = []
    for input_path in inputs:
        path = Path(input_path)
        if path.is_dir():
            # Scan directory for FASTA files
            fasta_files.extend(path.glob("*.fasta"))
            fasta_files.extend(path.glob("*.fasta.gz"))
        elif path.is_file():
            fasta_files.append(path)
        else:
            print(f"Warning: Path '{input_path}' does not exist")
    return [str(f.absolute()) for f in fasta_files]


def main():
    parser = argparse.ArgumentParser(description='Process FASTA file through genomics pipeline')
    parser.add_argument('-i', '--input', nargs='+', required=True,
                       help='Input FASTA file(s) or directory containing FASTA files')
    parser.add_argument('-o', '--output', default='output-from-default2', help='Output directory (default: output)')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite existing database')
    parser.add_argument('-b', '--batch-size', type=int, default=1000,
                       help='Batch size for database inserts (default: 1000)')

    # Pipeline control options
    parser.add_argument('--make-db', action='store_true',
                       help='Make db')
    parser.add_argument('--run-annotation', action='store_true',
                       help='Run protein annotation (annotate rule)')
    parser.add_argument('--run-all', action='store_true',
                       help='Run all pipeline steps')

    # SLURM cluster options
    parser.add_argument('--use-slurm', action='store_true',
                       help='Submit snakemake rules as SLURM jobs')
    parser.add_argument('--slurm-jobs', type=int, default=10,
                       help='Max concurrent SLURM jobs (default: 10)')
    parser.add_argument('--slurm-account', type=str, default='lindems',
                       help='SLURM account to use for job submission (default: lindems)')
    parser.add_argument('--slurm-partition', type=str, default='cpu',
                       help='SLURM partition to use for job submission (default: cpu)')

    args = parser.parse_args()

    # ---------------- Step 1: Locate input and assert each file exists --------------- #
    fasta_files = get_fasta_files(args.input)
    # Error checking 1: no fasta given
    if not fasta_files:
        print("Error: No FASTA files found")
        return 1

    print(f"\n\nStep 1: Found {len(fasta_files)} FASTA file(s): {[Path(f).name for f in fasta_files]}")

    # ----------------------- Step 2: Validate FASTA files ----------------------- #
    # TODO: Stop if 1 error or persist with working files?
    valid_files = []
    for fasta_file in fasta_files:
        if not os.path.exists(fasta_file):
            print(f"Error: FASTA file '{fasta_file}' not found")
            raise FileNotFoundError(f"FASTA file '{fasta_file}' not found")

        # Step 1: Validate the fasta file
        fastaClass = Fasta(file=fasta_file, run_mode='module')
        if not fastaClass.valid:
            print(f"Error: FASTA file '{fasta_file}' is invalid.")
            raise ValueError(f"FASTA file '{fasta_file}' is invalid.")  # TODO: Own own exception --> fun to propagate from GeneralTools...

        valid_files.append(fasta_file)
        print(f"Validated: {Path(fasta_file).name}")  # TODO: Change this to logger and --verbose mode
    print(f'Step 2: {len(valid_files)} FASTA files were validated successfully.')

    # ----------------------- Step 3: Locate Snakemake file ---------------------- #
    snakemake_file = Path(__file__).parent / "example.smk"
    if not snakemake_file.exists():
        print(f"Error: Snakemake file '{snakemake_file}' not found.")
        return 1
    print(f'Step 3: Using Snakemake file: {snakemake_file}')

    # ------------ Step 3.5: Load default config from workflow profile ----------- #
    # TODO: Hard code this location somewhere else, verify, and allow command to override
    default_workflow_config_file = Path(__file__).parent / "profiles" / "default" / "config.yaml"
    if not default_workflow_config_file.exists():
        print(f"Error: Default config file '{default_workflow_config_file}' not found.")
        return 1
    with open(default_workflow_config_file, 'r') as cf:
        margie_config: dict = yaml.safe_load(cf)
        workflow_config_defaults = margie_config.get('config', {})

    print(f'Step 3.5: Loaded default config from {margie_config}')

    # ------------- Step 4: Generating sample names from FASTA files ------------- #
    samples = []
    for fasta_file in valid_files:
        sample_name = Path(fasta_file).stem
        samples.append(sample_name)
    print(f'\nStep 4: Sample names derived from FASTA files: {samples}')

    # ----------------------Step 5: generating target files --------------------- #
    targets = []
    output_dir = workflow_config_defaults.get('output_dir', 'output')
    for sample in samples:
        # if 'make_db' in rules_to_run:
        if True:  #TODO: Make this dynanmic based on the CLI
            # targets.append(f"{output_dir}/{sample}.db")
            targets.append(f"{output_dir}/annotations/agg/{sample}.gff")
    print(f'\nStep 5: Target files to be generated: {targets}')

    # Create sample to file mapping
    sample_mapping = {sample: fasta for sample, fasta in zip(samples, valid_files)}

    # ------------ Step 6: Create temporary config file for snakemake ------------ #
    temp_config = {
        "sample_to_file": sample_mapping,
        "samples": samples
    }
    temp_config_file = Path("temp_snakemake_config.json")

    # Write new config
    with open(temp_config_file, 'w') as f:
        json.dump(temp_config, f, indent=2)
    print(f"\nStep 6: Wrote temporary config file to {temp_config_file}")

    # ------------------ Step 7: Build command using configfile ------------------ #
    cmd = [
        "snakemake",
        "--snakefile", str(snakemake_file),
        "--configfile", str(temp_config_file.absolute()),
        "--workflow-profile", "profiles/default"
    ] + targets

    # TODO: Add SLURM cluster execution if requested (Snakemake v8+ executor plugin)
    if args.use_slurm:
        cmd.extend([
            "--executor", "slurm",
            "--jobs", str(args.slurm_jobs),
            "--latency-wait", "60",
            "--default-resources",
            f"slurm_account={args.slurm_account}",
            f"slurm_partition={args.slurm_partition}"
        ])

    print(f"\nStep 7: Command generated:\n{' '.join(cmd)}")

    # ---------------------- Step 8: Run the actual command ---------------------- #
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
    print(f'Snakemake stdout:\n{result.stdout}')
    print(f'Snakemake stderr:\n{result.stderr}')

    if result.returncode == 0:
        print("Snakemake pipeline completed successfully!")
        print("Output:", result.stdout)
    else:
        print(f"Snakemake pipeline failed with return code {result.returncode}")
        print("Error:", result.stderr)
        return 1
    print(f'\nStep 8: Snakemake pipeline finished.')

    # ------------ Step 9 Archive temporary config file with timestamp ----------- #
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logs_dir = Path(__file__).parent / ".margie" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    archived_config = logs_dir / f"config_{timestamp}.json"
    temp_config_file.rename(archived_config)
    print(f'\nStep 9: Archived temporary config file to {archived_config}')
    print(f'\n✅ Margie pipeline completed successfully!')

if __name__ == '__main__':
    exit(main())
