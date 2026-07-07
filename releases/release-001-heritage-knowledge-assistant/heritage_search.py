from knowledge_loader import load_knowledge_cards


def search_cards(question, cards):
    question_words = question.lower().split()

    best_card = None
    best_score = 0

    for card in cards:
        content = card["content"].lower()

        score = 0
        for word in question_words:
            if word in content:
                score += 1

        if score > best_score:
            best_score = score
            best_card = card

    return best_card, best_score


if __name__ == "__main__":
    cards = load_knowledge_cards("foundation-dataset/knowledge-cards")

    question = input("Ask a heritage question: ")

    result, score = search_cards(question, cards)

    if result:
        print("\nBest Match")
        print("----------")
        print(f"Title: {result['title']}")
        print(f"Filename: {result['filename']}")
        print(f"Score: {score}")
        print("\nContent Preview:")
        print(result["content"][:500])
    else:
        print("No matching knowledge card found.")