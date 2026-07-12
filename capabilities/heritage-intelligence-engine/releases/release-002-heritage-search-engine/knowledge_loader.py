from pathlib import Path
from typing import Dict, List


def load_knowledge_cards(dataset_path: str) -> List[Dict]:
    """
    Load Markdown Knowledge Cards from a directory.

    Parameters
    ----------
    dataset_path : str
        Path to the directory containing Markdown Knowledge Cards.

    Returns
    -------
    List[Dict]
        Loaded Knowledge Cards containing filename, title and content.
    """

    path = Path(dataset_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Knowledge Card directory does not exist: {path}"
        )

    if not path.is_dir():
        raise NotADirectoryError(
            f"Knowledge Card path is not a directory: {path}"
        )

    knowledge_cards = []

    for file_path in sorted(path.glob("*.md")):
        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            continue

        lines = content.splitlines()

        title = lines[0].replace("#", "").strip()

        knowledge_cards.append(
            {
                "filename": file_path.name,
                "title": title,
                "content": content,
            }
        )

    return knowledge_cards


if __name__ == "__main__":
    from settings import DATASET_PATH

    cards = load_knowledge_cards(str(DATASET_PATH))

    print(f"Loaded {len(cards)} Knowledge Cards.")

    for card in cards:
        print(f"- {card['title']} ({card['filename']})")