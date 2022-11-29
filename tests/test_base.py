import motorpy


def test_base_name():
    assert motorpy.base.NAME == "motorpy"


async def test_client_init(client: motorpy.Motor):
    assert client is not None


async def test_org_settings(client: motorpy.Motor):
    org_settings = await client.org_settings()
    assert org_settings is not None


async def test_language(client: motorpy.Motor):
    language = await client.language()
    assert language is not None
    assert isinstance(language, str)
    assert language in ["en", "fr", "de", "es", "it", "nl", "pt", "sv", "ar"]


async def test_org_name(client: motorpy.Motor):
    org_name = await client.org_name()
    assert org_name is not None
    assert isinstance(org_name, str)


async def test_api_request(client: motorpy.Motor):
    # will return a dict
    response = await client.api.request("GET", "/config/drivers")
    assert response is not None
    assert isinstance(response, dict)

    # will return a list
    response = await client.api.request("GET", "/config/risk")
    assert response is not None
    assert isinstance(response, list)
