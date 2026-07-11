from pathlib import Path


def load_knowledge_cards(dataset_path):
    dataset_path = Path(dataset_path)

    knowledge_cards = []

    for file in dataset_path.glob("*.md"):
        content = file.read_text(encoding="utf-8")

        knowledge_cards.append({
            "filename": file.name,
            "title": content.splitlines()[0].replace("#", "").strip(),
            "content": content
        })

    return knowledge_cards


if __name__ == "__main__":
    path = "foundation-dataset/knowledge-cards"
    cards = load_knowledge_cards(path)

    print(f"Loaded {len(cards)} knowledge cards.")

    for card in cards:
        print(f"- {card['title']} ({card['filename']})")