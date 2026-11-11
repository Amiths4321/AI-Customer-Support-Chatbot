
import fitz


def extract_pdf_text(uploaded_file):

    pdf_bytes = uploaded_file.getvalue()

    pdf_document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    extracted_pages = []

    for page_number, page in enumerate(pdf_document, start=1):

        page_text = page.get_text("text").strip()

        if page_text:
            extracted_pages.append({
                "page": page_number,
                "text": page_text
            })

    pdf_document.close()

    return extracted_pages
