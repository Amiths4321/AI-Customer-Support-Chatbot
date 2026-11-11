
import ollama

from config import OLLAMA_HOST, CHAT_MODEL, SYSTEM_PROMPT


def generate_response(messages, search_results=None):

    client = ollama.Client(host=OLLAMA_HOST)

    # Prepare company document context
    context = ""

    if search_results:

        for result in search_results:

            context += f"""
Source: {result['filename']}
Page: {result['page']}

Content:
{result['text']}

---
"""

    else:
        context = "No relevant company document information was retrieved."

    # Instructions for grounded answers
    rag_prompt = f"""
{SYSTEM_PROMPT}

COMPANY KNOWLEDGE BASE:

{context}

IMPORTANT RULES:

1. Use the supplied company information to answer customer questions.
2. Do not invent company policies, prices, or product details.
3. If the answer is not available in the supplied information,
   clearly tell the customer.
4. Mention the source filename and page number when using
   company document information.
5. Be polite, professional, and concise.
"""

    conversation = [
        {
            "role": "system",
            "content": rag_prompt
        }
    ]

    conversation.extend(messages)

    response = client.chat(
        model=CHAT_MODEL,
        messages=conversation
    )

    return response["message"]["content"]
