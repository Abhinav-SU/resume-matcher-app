import numpy as np
import matcher


def test_rank_resumes(monkeypatch):
    def fake_embed(text):
        if text == "job":
            return np.array([1.0, 0.0])
        elif text == "resume1":
            return np.array([0.9, 0.1])
        else:
            return np.array([0.0, 1.0])

    monkeypatch.setattr(matcher, "get_embedding", fake_embed)

    job_desc = "job"
    resumes = ["resume1", "resume2"]
    names = ["Alice", "Bob"]
    file_bytes = [b"a", b"b"]
    filenames = ["a.pdf", "b.pdf"]

    results = matcher.rank_resumes(job_desc, resumes, names, file_bytes, filenames)

    assert [r["name"] for r in results] == ["Alice", "Bob"]
    assert len(results) == 2

