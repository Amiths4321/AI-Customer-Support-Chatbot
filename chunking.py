
def create_chunks(
    documents,
    chunk_size=500,
    overlap=75
):
    all_chunks = []

    for document in documents:

        filename = document["filename"]

        for page in document["pages"]:

            text = page["text"]
            page_number = page["page"]

            start = 0

            while start < len(text):

                end = start + chunk_size

                chunk_text = text[start:end].strip()

                if chunk_text:

                    all_chunks.append({
                        "filename": filename,
                        "page": page_number,
                        "text": chunk_text
                    })

                start += chunk_size - overlap

    return all_chunks
