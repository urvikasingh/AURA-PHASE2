from backend.domains.usp.usp import usp_handler
from backend.domains.academic.academic import academic_handler
from backend.core.policy_engine import PolicyEngine


def route_message(user_id: int, domain: str, message: str) -> str:
    domain = domain.lower()

    if not message or not message.strip():
        return "Hello. How can I help you today?"

    # 🔐 Policy always runs
    policy = PolicyEngine.run(message)
    if policy.blocked:
        return policy.response

    if domain == "usp":
        return usp_handler(message, user_id)

    if domain == "academic":
        return academic_handler(message, user_id)

    return "Invalid domain selected."
