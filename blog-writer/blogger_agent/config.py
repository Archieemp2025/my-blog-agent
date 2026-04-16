# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)


def get_model_wrapper(model_name: str):
    """
    Wrap OpenAI model using LiteLLM so ADK can understand it
    """
    from google.adk.models.lite_llm import LiteLlm
    return LiteLlm(model_name)


@dataclass
class ResearchConfiguration:
    """Configuration for models and agent behaviour."""

    # Models (from .env)
    worker_model: str = os.getenv("WORKER_MODEL", "gpt-4o-mini")
    critic_model: str = os.getenv("CRITIC_MODEL", "gpt-4o-mini")

    # OpenAI API Key
    openai_api_key: str = os.getenv("OPENAI_API_KEY")

    # Optional: for RAG later
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # Agent behaviour
    max_search_iterations: int = 5


# Create global config object
config = ResearchConfiguration()


# Helper function (optional but useful)
def get_model(model_name: str) -> str:
    """
    Returns model name (used by agents).
    Can be extended later if needed.
    """
    return model_name