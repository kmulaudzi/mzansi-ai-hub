## from mycolab code --> %%writefile ai_response_generator.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from knowledge_loader import load_knowledge_cards
from heritage_search import search_cards
from prompt_builder import build_prompt


class MzansiAIAssistant:

    def __init__(self):
        print("Loading FLAN-T5 Base...")

        model_id = "google/flan-t5-base"

        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        self.cards = load_knowledge_cards(
            "foundation-dataset/knowledge-cards"
        )

        print(f"Loaded {len(self.cards)} knowledge cards.")
        print("Assistant Ready!")


    def ask(self, question):
        best_card, score = search_cards(question, self.cards)

        if best_card is None:
            return "I could not find relevant heritage information for that question."

        prompt = build_prompt(question, best_card)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=200,
            min_new_tokens=40,
            num_beams=4,
            no_repeat_ngram_size=2,
            early_stopping=True
        )

        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return answer