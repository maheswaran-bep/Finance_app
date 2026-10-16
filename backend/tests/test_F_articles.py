
from fastapi.testclient import TestClient

from backend.routers.finance_articles_api import router

client = TestClient(router)


def fake_get(url, *args, **kwargs):
    class FakeResponse:
        def json(self):
            return [
                {
                    "date": "2026-10-16 09:00:00",
                    "title": "Test financial news",
                    "content": "Mock article content for testing.",
                    "link": "https://example.com/test-article",
                }
            ]

    return FakeResponse()


def test_get_articles(monkeypatch):
    monkeypatch.setattr(
        "backend.routers.finance_articles_api.requests.get",
        fake_get,
    )

    response = client.post(
        "/news/article",
        json={"company_name": "AAPL", "limit": "1"},
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    for article in data:
        assert "date" in article
        assert "title" in article
        assert "content" in article
        assert "link" in article
