import pytest
from supabase_utils.http.adapters.httpx import AsyncHttpxSession, HttpxSession

from postgrest import AsyncPostgrestClient, SyncPostgrestClient


def _clients():
    from httpx import AsyncClient, Client

    return [
        SyncPostgrestClient(base_url="http://localhost:3000", http_session=HttpxSession(Client())),
        AsyncPostgrestClient(
            base_url="http://localhost:3000", http_session=AsyncHttpxSession(AsyncClient())
        ),
    ]


@pytest.mark.parametrize("client", _clients(), ids=["sync", "async"])
def test_schema_replaces_profile_headers(client):
    private = client.schema("private")
    assert private.default_headers.get_list("Accept-Profile") == ["private"]
    assert private.default_headers.get_list("Content-Profile") == ["private"]

    analytics = private.schema("analytics")
    assert analytics.default_headers.get_list("Accept-Profile") == ["analytics"]
    assert analytics.default_headers.get_list("Content-Profile") == ["analytics"]

    # the original client is left untouched
    assert client.default_headers.get_list("Accept-Profile") == ["public"]
    assert client.default_headers.get_list("Content-Profile") == ["public"]
