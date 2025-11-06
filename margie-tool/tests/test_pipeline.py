#!/usr/bin/env python3

import os
import sys
import tempfile
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.pipeline import GenomeAnnotationPipeline, AnnotationDatabase

def create_test_fasta():
    """Create a small test FASTA file with 2 entries."""
    fasta_content = """>sequence1 test DNA sequence
ATGCGATCGATCGATCGATCGATCGATCGATCAAATAG
>sequence2 another test sequence
GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAAATAG
"""

    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False)
    temp_file.write(fasta_content)
    temp_file.close()

    return temp_file.name


def test_pipeline():
    """Test the complete annotation pipeline."""
    print("🧪 Testing Genome Annotation Pipeline")
    print("=" * 50)

    # Create test FASTA file
    test_fasta = create_test_fasta()
    print(f"📁 Created test FASTA: {test_fasta}")

    # Create temporary output directory
    output_dir = tempfile.mkdtemp(prefix="margie_test_")
    print(f"📁 Output directory: {output_dir}")

    try:
        # Initialize pipeline
        config = {
            "pfam_database": "/mock/path/Pfam-A.hmm",
            "tigrfam_database": "/mock/path/TIGRFAMs.hmm"
        }

        pipeline = GenomeAnnotationPipeline(test_fasta, output_dir, config)
        print("🚀 Running annotation pipeline...")
        # Run the pipeline
        db_path = pipeline.run()

        print("\n📊 Pipeline Results:")
        print("-" * 30)

        # Get annotations summary
        summary = pipeline.get_annotations_summary()
        print(f"Sequences in database: {summary['sequence_count']}")
        print(f"Annotation counts: {summary['annotation_counts']}")

        # Test database queries
        print("\n🔍 Testing Database Queries:")
        print("-" * 30)

        db = AnnotationDatabase(db_path)

        # Get annotations for sequence1
        annotations = db.get_sequence_annotations("sequence1")
        print(f"Annotations for sequence1: {len(annotations)}")
        for ann in annotations:
            print(f"  - {ann['annotation_type']}: {ann['description']}")

        # Get annotations for sequence2
        annotations = db.get_sequence_annotations("sequence2")
        print(f"Annotations for sequence2: {len(annotations)}")
        for ann in annotations:
            print(f"  - {ann['annotation_type']}: {ann['description']}")

        db.close()

        print(f"\n✅ Test completed successfully!")
        print(f"📁 Results saved in: {output_dir}")
        print(f"🗄️  Database: {db_path}")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

    finally:
        # Cleanup test FASTA file
        if os.path.exists(test_fasta):
            os.unlink(test_fasta)


def test_database_operations():
    """Test database operations independently."""
    print("\n🧪 Testing Database Operations")
    print("=" * 50)

    # Create temporary database
    db_path = tempfile.mktemp(suffix='.db')

    try:
        db = AnnotationDatabase(db_path)

        # Test adding mock sequences
        print("Adding mock sequences...")

        conn = db._get_connection()
        cursor = conn.cursor()

        # Add test sequences
        cursor.execute('''
            INSERT INTO sequences (header, sequence, length, gc_content)
            VALUES (?, ?, ?, ?)
        ''', ("test_seq1", "ATGCGATCG", 9, 55.6))

        cursor.execute('''
            INSERT INTO sequences (header, sequence, length, gc_content)
            VALUES (?, ?, ?, ?)
        ''', ("test_seq2", "GCTAGCTAG", 9, 55.6))

        conn.commit()

        # Test adding annotations
        print("Adding mock annotations...")

        cursor.execute('''
            INSERT INTO annotations
            (sequence_id, annotation_type, tool, start_pos, end_pos, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (1, "pfam", "hmmscan", 1, 100, "Test domain"))

        cursor.execute('''
            INSERT INTO annotations
            (sequence_id, annotation_type, tool, start_pos, end_pos, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (2, "tigrfam", "hmmscan", 50, 150, "Another domain"))

        conn.commit()

        # Test queries
        annotations = db.get_sequence_annotations("test_seq1")
        print(f"Found {len(annotations)} annotations for test_seq1")

        annotations = db.get_sequence_annotations("test_seq2")
        print(f"Found {len(annotations)} annotations for test_seq2")

        db.close()

        print("✅ Database operations test passed!")
        return True

    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        return False

    finally:
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)


def main():
    """Run all tests."""
    print("🧬 margie Pipeline Testing Suite")
    print("=" * 50)

    all_tests_passed = True

    # Test 1: Database operations
    if not test_database_operations():
        all_tests_passed = False

    # Test 2: Full pipeline
    if not test_pipeline():
        all_tests_passed = False

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")

    return 0 if all_tests_passed else 1


if __name__ == '__main__':
    exit(main())
