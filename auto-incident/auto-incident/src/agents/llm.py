"""LLM factory for agents."""
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama

from src.config import get_settings


def get_llm() -> BaseChatModel:
    """Return configured LLM (OpenAI, Anthropic, or Ollama)."""
    settings = get_settings()
    if settings.llm_provider == "ollama":
        return ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
            temperature=0,
        )
    if settings.llm_provider == "anthropic":
        return ChatAnthropic(
            model="claude-3-haiku-20240307",
            api_key=settings.anthropic_api_key,
        )
    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
    )
