from ollama import chat

from src.analytics.evidence_matrix import build_evidence_matrix


MODEL = "llama3.2:3b"


def build_evidence_context():
    matrix = build_evidence_matrix()

    sections = []

    for _, row in matrix.iterrows():
        sections.append(
            f"""
Hypothesis: {row["hypothesis"]}
Evidence state: {row["evidence_state"]}
Evidence: {row["evidence"]}
Limitation: {row["limitation"]}
""".strip()
        )

    return "\n\n".join(sections)


def build_prompt(question):
    evidence_context = build_evidence_context()

    return f"""
You are an evidence-aware urban analytics assistant.

Answer the user's question using ONLY the supplied Project 3 evidence.

Rules:
1. Do not invent evidence.
2. Do not claim causation from observational associations.
3. Preserve distinctions between SUPPORTED, COMPLICATED,
   CONTRADICTED, and UNRESOLVED evidence.
4. State important limitations.
5. If the evidence cannot answer the question, say so explicitly.
6. Distinguish analytical findings from interpretation.
7. Keep the briefing concise and suitable for a professional analyst.

PROJECT 3 EVIDENCE

{evidence_context}

USER QUESTION

{question}
""".strip()


def generate_briefing(question):
    prompt = build_prompt(question)

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content


def main():
    question = (
        "Does the evidence support The Wire's portrayal of urban problems "
        "as interconnected institutional and structural problems?"
    )

    briefing = generate_briefing(question)

    print("\nAI ANALYTICAL BRIEFING\n")
    print(briefing)


if __name__ == "__main__":
    main()