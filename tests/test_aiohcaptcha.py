import pytest  # type: ignore

from aiohcaptcha import HCaptchaClient, __version__

TESTING_SECRET_KEY = "0x0000000000000000000000000000000000000000"
TESTING_SITE_KEY = "10000000-ffff-ffff-ffff-000000000001"


def test_version():
    assert __version__ == "0.1.1"


@pytest.mark.asyncio
async def test_verification():
    with pytest.raises(RuntimeError):
        HCaptchaClient()
    client = HCaptchaClient(TESTING_SECRET_KEY)
    assert await client.verify(TESTING_SITE_KEY), client.response.error_codes


@pytest.mark.asyncio
async def test_incorrect_response():
    client = HCaptchaClient(TESTING_SECRET_KEY)
    result = await client.verify(TESTING_SITE_KEY.replace("0001", "1001"))
    assert result is False
    assert len(client.response.error_codes) == 1
    assert "invalid-input-response" in client.response.error_codes


@pytest.mark.asyncio
async def test_expected_sitekey():
    client = HCaptchaClient(TESTING_SECRET_KEY)
    result = await client.verify(TESTING_SITE_KEY, sitekey=TESTING_SITE_KEY)
    assert result, client.response.error_codes


@pytest.mark.asyncio
async def test_incorrect_response_code():
    client = HCaptchaClient(TESTING_SECRET_KEY, api_url="https://pypi.org")
    result = await client.verify(TESTING_SITE_KEY, remote_ip="127.0.0.1")
    assert result is False
    assert client.response is None
