import json
import os
from typing import Iterator

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from mistralai.models.jobs import DetailedJob

from models import Label


class MistralAPIClient:
    _MISTRAL_MODELS_FILE_PATH = "mistral_models.json"

    _client: MistralClient
    _mistral_models_dict: dict[Label, DetailedJob]

    def __init__(self) -> None:
        # Check whether the api key exists
        api_key = os.getenv("MISTRAL_API_KEY")
        if api_key is None:
            raise ValueError("MISTRAL_API_KEY environment variable is not set.")

        self._client = MistralClient(api_key=api_key)

        with open(MistralAPIClient._MISTRAL_MODELS_FILE_PATH, "r") as f:
            self._mistral_models_dict = {
                Label(label): self._client.jobs.retrieve(id)
                for label, id in json.load(f).items()
            }

    def chat(self, query: str, label: Label) -> Iterator[dict[str, str]]:
        """
        Sends a chat request to Mistral with the given query and label, streaming the response.

        Parameters:
            query (str): The query to send to Mistral.
            label (Label): The label to specify the Mistral model to use.

        Yields:
            dict[str, str]: A dictionary with a key 'data' containing the SSE formatted string of response data from Mistral.
        """
        model_name = self._mistral_models_dict[label]
        messages = [ChatMessage(role="user", content=query)]
        stream_response = self._client.chat_stream(
            model=model_name.fine_tuned_model, messages=messages
        )

        for chunk in stream_response:
            response = chunk.choices[0].delta.content

            if response is None:
                yield {"data": json.dumps({"error": {}})}
                continue

            yield {"data": response}

        yield {"data": json.dumps({"done": True})}
