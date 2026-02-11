class PolicyResult:
    def __init__(self, blocked: bool, response: str | None = None):
        self.blocked = blocked
        self.response = response


class PolicyEngine:
    @staticmethod
    def run(message: str) -> PolicyResult:
        msg = message.lower()

        # 1️⃣ Medical safety refusal
        if "chest pain" in msg:
            return PolicyResult(
                blocked=True,
                response=(
                    "I can’t provide medical advice. "
                    "Chest pain can be serious — please consult a doctor."
                )
            )

        # 2️⃣ Hallucination refusal
        if "ceo of my company" in msg:
            return PolicyResult(
                blocked=True,
                response=(
                    "I don’t have enough information to answer that."
                )
            )

        # 3️⃣ Allowed
        return PolicyResult(blocked=False)
