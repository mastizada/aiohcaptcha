# aiohcaptcha

 [![pipeline status](https://gitlab.com/mastizada/aiohcaptcha/badges/master/pipeline.svg)](https://gitlab.com/mastizada/aiohcaptcha/-/commits/master) 
 [![coverage report](https://gitlab.com/mastizada/aiohcaptcha/badges/master/coverage.svg)](https://gitlab.com/mastizada/aiohcaptcha/-/commits/master) 

AsyncIO client for the hCaptcha service

Secure your forms using a captcha.

---

## Install
    pip install aiohcaptcha
## Usage
### Configuration
You can define the secret key `HCAPTCHA_SECRET_KEY` in the environment or directly pass it to the `HCaptchaClient` model as a parameter.

Get the secret and public keys from the [hcaptcha.com](https://hcaptcha.com).
### Template
    <div class="h-captcha" data-sitekey="your_site_key"></div>
    <script src="https://hcaptcha.com/1/api.js" async defer></script>

Check [hCaptcha docs](https://docs.hcaptcha.com/) for more details on the HTML widget.
### View
    from aiohcaptcha import HCaptchaClient
    
    response_token = request.POST["h-captcha-response"]
    client = HCaptchaClient(secret_key)
    verified = await client.verify(response_token)  # a boolean

You can adjust it to any Python Web framework that has async view support.

If you are sending the form data using an AJAX request, use `$('textarea[name=h-captcha-response]').val();` for the captcha key.

### Response details

Response details are stored in `client.response`,
details of the `HCaptchaResponse` model is same as the JSON response provided in the hCaptcha documentation.

### Extra arguments

You can also add `remote_ip` and `sitekey` (expected key) to the `client.verify` function.
These parameters are explained in the [hCaptcha docs](https://docs.hcaptcha.com/).

For unit testing, you can create the Client `HCaptchaClient` with `debug=True` parameter.
In this mode, the `verify` function will return `True` if the `user_response` token and `sitekey` parameters do match, otherwise it will return `False`:

    client = HCaptchaClient("<SECRET_KEY>", debug=True)
    assert await client.verify("<USER_TOKEN>", sitekey="<SAME_TOKEN>")
    assert await client.verify("<USER_TOKEN>", sitekey="<DIFFERENT_TOKEN>") is False

---

&copy; 2020 Emin Mastizada. MIT Licenced.
