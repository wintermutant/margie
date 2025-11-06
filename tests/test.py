import os
import tempfile
from bioinformatics_tools.file_classes.Fasta import Fasta

def create_test_fasta():
    """Create a small test FASTA file with 2 entries."""
    fasta_content = """>sequence1 test DNA sequence
ATGCGATCGATCGATCGATCGATCGATCGATC
>sequence2 another test sequence
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCT
"""

    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False)
    temp_file.write(fasta_content)
    temp_file.close()

    return temp_file.name

def main():
    print(f'Starting test')

    # Create test FASTA file
    test_fasta_path = create_test_fasta()
    print(f'Created test FASTA file: {test_fasta_path}')

    try:
        # Step 1: Validate the fasta file
        print(f'Running Fasta class validation')
        fastaClass = Fasta(file=test_fasta_path, run_mode='module')
        print(f"Validating FASTA file: {test_fasta_path}")

        if not fastaClass.valid:
            print(f"Error: FASTA file '{test_fasta_path}' is invalid.")
            return 1

        print(f"FASTA file '{test_fasta_path}' is valid.")
        print(f"FASTA key: {fastaClass.fastaKey}")
        print(f"Pydantic model: {fastaClass.to_pydantic()}")

        return 0

    finally:
        # Clean up temporary file
        if os.path.exists(test_fasta_path):
            os.unlink(test_fasta_path)
            print(f"Cleaned up temporary file: {test_fasta_path}")
            print(f'✅ Tests passed successfully!')

if __name__ == '__main__':
    exit(main())
