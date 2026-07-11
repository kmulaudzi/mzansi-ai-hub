from pathlib import Path


ENGINE_ROOT = Path(__file__).resolve().parents[1]
RELEASE_ROOT = ENGINE_ROOT / "releases" / "release-001-knowledge-cards"


def test_release_001_directory_exists():
    assert RELEASE_ROOT.exists()
    assert RELEASE_ROOT.is_dir()


def test_release_001_has_readme():
    assert (RELEASE_ROOT / "README.md").exists()


def test_release_001_has_python_application():
    python_files = list(RELEASE_ROOT.rglob("*.py"))
    assert python_files, "No Python files were found in Release 001."


def test_release_001_has_heritage_data():
    supported_extensions = {
        ".json",
        ".csv",
        ".yaml",
        ".yml",
        ".txt",
        ".md",
    }

    data_files = [
        path
        for path in RELEASE_ROOT.rglob("*")
        if path.is_file() and path.suffix.lower() in supported_extensions
    ]

    assert data_files, "No Knowledge Card or heritage data files were found."
