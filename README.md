# aiohcaptcha

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

---

&copy; 2020 Emin Mastizada. MIT Licenced.
