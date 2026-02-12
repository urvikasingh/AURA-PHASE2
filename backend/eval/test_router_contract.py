from backend.router.domain_router import route_message


def test_greeting_only_on_empty_input():
    reply = route_message(
        user_id=1,
        domain="usp",
        message=""
    )
    assert "help you" in reply.lower()


def test_no_greeting_on_real_question():
    reply = route_message(
        user_id=1,
        domain="usp",
        message="Explain gravity briefly"
    )
    assert "help you" not in reply.lower()
