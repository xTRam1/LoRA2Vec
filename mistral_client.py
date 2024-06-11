from models import Label


class MistralClient:

    def get_response(self, label: Label) -> str:
        return f"Response for {label}"
