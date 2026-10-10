from pathlib import Path

from app.actions.files import FileManager


def test_create_folder_and_file(tmp_path):
    fm = FileManager(desktop_path=str(tmp_path), documents_path=str(tmp_path), downloads_path=str(tmp_path))
    folder = fm.create_folder("projects", base_dir=tmp_path)
    assert "projects" in folder

    note = fm.create_file("study_plan.txt", "Review AI basics", base_dir=tmp_path)
    assert "study_plan" in note
    assert (tmp_path / "study_plan.txt").exists()


def test_search_files(tmp_path):
    fm = FileManager(desktop_path=str(tmp_path), documents_path=str(tmp_path), downloads_path=str(tmp_path))
    docs = tmp_path / "alpha.pdf"
    docs.write_text("hello", encoding="utf-8")
    matches = fm.search_files("alpha", root=str(tmp_path))
    assert len(matches) >= 1


def test_read_file(tmp_path):
    fm = FileManager(desktop_path=str(tmp_path), documents_path=str(tmp_path), downloads_path=str(tmp_path))
    file_path = tmp_path / "note.txt"
    file_path.write_text("hello there", encoding="utf-8")
    text = fm.read_text_file(file_path)
    assert text == "hello there"
