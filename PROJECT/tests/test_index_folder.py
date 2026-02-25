import pytest
import os
import tempfile
import shutil
from main import index_folder
import asyncio


def test_index_folder_integration():
    """Integration test for the index_folder function"""
    # Create a temporary directory with test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files of different types
        test_files = {
            "doc1.md": "# Test Document\n\n## Section 1\nThis is the first section.\n\n## Section 2\nThis is the second section.",
            "doc2.txt": "This is a plain text document.\nIt has multiple lines.\nFor testing purposes.",
            "doc3.py": "def function1():\n    \"\"\"This is function 1\"\"\"\n    pass\n\nclass Class1:\n    \"\"\"This is class 1\"\"\"\n    def method1(self):\n        pass"
        }

        for filename, content in test_files.items():
            with open(os.path.join(temp_dir, filename), "w", encoding="utf-8") as f:
                f.write(content)

        # Run the index_folder function
        result = asyncio.run(index_folder(temp_dir))

        # Assertions
        assert result is not None
        assert result["status"] == "success"
        assert result["indexed_files"] == 3  # We created 3 files
        assert result["total_documents"] >= 3  # Should be at least 3 document chunks

        # Test with a specific glob pattern
        result2 = asyncio.run(index_folder(temp_dir, "*.md"))
        assert result2["indexed_files"] == 1  # Only markdown files
        assert result2["total_documents"] >= 1


def test_index_folder_with_empty_directory():
    """Test index_folder with an empty directory"""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = asyncio.run(index_folder(temp_dir))

        assert result is not None
        assert result["status"] == "success"
        assert result["indexed_files"] == 0
        assert result["total_documents"] == 0


def test_index_folder_with_nonexistent_directory():
    """Test index_folder with a nonexistent directory"""
    result = asyncio.run(index_folder("/nonexistent/directory"))

    # Should handle the error gracefully
    assert result is not None
    assert result["status"] == "success"  # Function continues despite errors
    assert result["indexed_files"] >= 0  # Could be 0 or more depending on system