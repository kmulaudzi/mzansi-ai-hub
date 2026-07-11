## from mycolab code --> %%writefile prompt_builder.py

def build_prompt(question, knowledge_card):
    prompt = f"""
You are the Mzansi AI Heritage Assistant.

Use the heritage knowledge below to answer the question.

Write 3 to 5 complete sentences.
Do not answer with only a name or one word.
Explain the topic clearly and simply.

Heritage Knowledge:
{knowledge_card["content"]}

Question:
{question}

Answer in 3 to 5 complete sentences:
"""
    return prompt