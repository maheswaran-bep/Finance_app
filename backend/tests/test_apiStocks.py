
import pytest
from fastapi.testclient import TestClient

from backend.routers.stocks_api import router

client = TestClient(router)


def fake_get(url, *args, **kwargs):
    class FakeResponse:
        def json(self):
            return {
                "symbol": "AAPL",
                "close": 150.0,
                "price": 150.0,
            }

    return FakeResponse()


@pytest.mark.parametrize("stock_name", ["AAPL", "MSFT"])
def test_get_stocks_bursa_close(stock_name, monkeypatch):
    monkeypatch.setattr(
        "backend.routers.stocks_api.requests.get",
        fake_get,
    )

    response = client.post(
        "/stocks/bursa_close",
        json={"stock_": stock_name},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.parametrize("stock_name", ["AAPL", "MSFT"])
def test_realtime_data_company(stock_name, monkeypatch):
    monkeypatch.setattr(
        "backend.routers.stocks_api.requests.get",
        fake_get,
    )

    response = client.post(
        "/stocks/realTime",
        json={"stock_": stock_name},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), dict)
