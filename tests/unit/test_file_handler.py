import pytest

def test_file_reading(file_handler, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test content")
    
    content = file_handler.sync_read(test_file)
    assert content == "Test content"

def test_pdf_handling(file_handler, tmp_path):
    # Note: Nécessite un PDF de test dans resources/
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4...")  # Simplifié
    
    with pytest.raises(Exception):
        file_handler.sync_read(pdf_file)