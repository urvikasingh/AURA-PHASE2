from backend.domains.academic.academic import academic_handler
from backend.domains.usp.usp import usp_handler


def route_message(
    user_id: int,
    domain: str,
    message: str,
    conversation_id: int | None = None,
):
    if domain == "academic":
        return academic_handler(
            message=message,
            user_id=user_id,
            conversation_id=conversation_id,
        )

    if domain == "usp":
        return usp_handler(
            message=message,
            user_id=user_id,
            conversation_id=conversation_id,
        )

    raise ValueError(f"Unknown domain: {domain}")
