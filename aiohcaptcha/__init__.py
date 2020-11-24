__version__ = "0.1.2"
import logging
import os
from typing import Optional

from aiohttp import ClientSession

logger = logging.getLogger("aiohcaptcha")


class HCaptchaResponse(object):
    """
    hCaptcha response model. Details: https://docs.hcaptcha.com/#server
    """

    def __init__(self, response: dict):
        self.success: bool = response.get("success", False)
        self.challenge_ts = response.get("challenge_ts", None)
        self.hostname: str = response.get("hostname", None)
        self.credit: bool = response.get("credit", False)
        self.error_codes: list = response.get("error-codes", [])
        # for enterprise account
        self.score: float = response.get("score", 0.0)
        self.score_reason: list = response.get("score_reason", [])


class HCaptchaClient(object):
    """Client for hCaptcha API."""

    def __init__(
        self,
        secret_key: Optional[str] = None,
        debug: Optional[bool] = False,
        api_url: str = "https://hcaptcha.com/siteverify",
    ):
        """
        Initialize the client for hCaptcha.
        :param secret_key: hCaptcha secret key.
        :param debug: Debug mode to bypass verification in unit testing.
        :param api_url: Custom API URL for hCaptcha.
        """
        if not secret_key:
            secret_key = os.environ.get("HCAPTCHA_SECRET_KEY", None)
        if not secret_key:
            raise RuntimeError(
                "Site key is not provided for the hCaptcha client."
                "You can define it in your environment as HCAPTCHA_SECRET_KEY"
                "or pass a site_key argument to this class."
            )
        self.secret_key = secret_key
        self.debug = debug
        self.api_url = api_url
        self.response: Optional[HCaptchaResponse] = None

    async def verify(
        self,
        user_token: str,
        remote_ip: Optional[str] = None,
        sitekey: Optional[str] = None,
    ) -> bool:
        """
        Verify hCaptcha token from the submitted form.
        Response data will be saved in self.response.

        :param user_token: The verification token you received when the user completed the captcha on your site.
        :param remote_ip: Optional. The user's IP address.
        :param sitekey: Optional. The sitekey you expect to see.
        :return: Verification result as a boolean.
        """
        self.response = None
        payload = {"secret": self.secret_key, "response": user_token}
        if remote_ip:
            payload["remoteip"] = remote_ip
        if sitekey:
            payload["sitekey"] = sitekey
        if self.debug and sitekey:
            if user_token == sitekey:
                return True
            return False
        async with ClientSession() as session:
            async with session.post(url=self.api_url, data=payload) as resp:
                if resp.status != 200:
                    raw_response = await resp.text()
                    logger.error(f"Incorrect hCaptcha response, code: {resp.status}, message: {raw_response}")
                    return False
                response: dict = await resp.json()
                self.response = HCaptchaResponse(response)
                if self.response.success:
                    return True
                return False
