
from datetime import datetime


def create_support_ticket(
    customer_message,
    conversation_history
):

    ticket = {
        "ticket_id": datetime.now().strftime(
            "SUP-%Y%m%d-%H%M%S"
        ),
        "created_at": datetime.now().isoformat(),
        "status": "Pending Human Review",
        "customer_message": customer_message,
        "conversation": conversation_history
    }

    return ticket


def clear_conversation():

    return [
        {
            "role": "assistant",
            "content": (
                "Hello! Welcome to Customer Support. "
                "How can I help you today?"
            )
        }
    ]
