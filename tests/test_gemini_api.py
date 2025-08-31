import importlib
import numpy as np
import types
import pytest


def reload_module(monkeypatch, key_present=True):
    if key_present:
        monkeypatch.setenv("GEMINI_API_KEY", "dummy")
    else:
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    import gemini_api
    importlib.reload(gemini_api)
    return gemini_api


def test_get_embedding(monkeypatch):
    gemini_api = reload_module(monkeypatch, key_present=True)

    def fake_embed_content(**kwargs):
        return {"embedding": [0.1, 0.2]}

    monkeypatch.setattr(gemini_api.genai, "embed_content", fake_embed_content)
    emb = gemini_api.get_embedding("hello")
    assert np.allclose(emb, [0.1, 0.2])


def test_get_embedding_empty_text(monkeypatch):
    gemini_api = reload_module(monkeypatch, key_present=True)
    emb = gemini_api.get_embedding("   ")
    assert isinstance(emb, np.ndarray)
    assert np.all(emb == 0)


def test_generate_fit_summary(monkeypatch):
    gemini_api = reload_module(monkeypatch, key_present=True)

    class FakeModel:
        def generate_content(self, prompt):
            return types.SimpleNamespace(text="summary")

    monkeypatch.setattr(gemini_api.genai, "GenerativeModel", lambda *a, **k: FakeModel())
    summary = gemini_api.generate_fit_summary("job", "resume")
    assert summary == "summary"


def test_generate_fit_summary_missing_key(monkeypatch):
    gemini_api = reload_module(monkeypatch, key_present=False)
    with pytest.raises(gemini_api.MissingAPIKeyError):
        gemini_api.generate_fit_summary("job", "resume")

