import motorpy


def test_base_name():
    assert motorpy.base.NAME == "motorpy"

async def test_client_init(client: motorpy.Motor):
    assert client is not None