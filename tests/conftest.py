import sys
import pytest
import motorpy
import asyncio


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield


def pytest_addoption(parser):
    parser.addoption("--orgid", action="store")
    parser.addoption("--url", action="store")
    parser.addoption("--apikey", action="store")


@pytest.fixture(scope="session")
def org_id(pytestconfig):
    return pytestconfig.getoption("orgid")


@pytest.fixture(scope="session")
def url(pytestconfig):
    return pytestconfig.getoption("url")


@pytest.fixture(scope="session")
def api_key(pytestconfig):
    return pytestconfig.getoption("apikey")

# yield a motorpy.Motor client


@pytest.fixture(autouse=True)
def client(org_id, url, api_key):
    _api_key = api_key
    _url = url
    _org_id = org_id
    if not _api_key or not _url or not _org_id:
        raise Exception("Missing required test parameters")

    _auth = motorpy.Auth(api_key=_api_key)
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    client = motorpy.Motor(org_id=_org_id, url=_url, auth=_auth)
    print(
        f"Client Created: Motor(org_id={org_id}, url={url}, api_key={len(api_key) * '*'})")
    try:
        yield client
    finally:
        asyncio.run(client.close())


@pytest.fixture(autouse=True)
async def driver(client) -> motorpy.Driver:
    # fetch from list api
    # this driver "Joe Adams" exists in the test org
    drivers = [d async for d in client.list_drivers(
        first_name=motorpy.Search("joe", "ilike"),
        last_name=motorpy.Search("adams", "ilike"),
        max_records=1
    )]
    if len(drivers) == 0:
        raise Exception("No drivers found in org")

    # driver = await client.get_driver(
    #     drivers[0].id,
    #     risk=True,
    #     address=True,
    #     fleets=True,
    #     vehicle_count=True,
    #     distance=False,
    #     points=True,
    #     files=True,
    #     contact=True,
    #     occupation=True
    # )
    driver = drivers[0]
    await driver.refresh()
    return driver
