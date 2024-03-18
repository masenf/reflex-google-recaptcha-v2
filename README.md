# google-recaptcha-v2

A Reflex custom component google-recaptcha-v2.

## Installation

```bash
pip install reflex-google-recaptcha-v2
```

## Usage

Set your site key and secret key in your environment variables.

```bash
export RECAPTCHA_SITE_KEY="your-site-key"
export RECAPTCHA_SECRET_KEY="your-secret-key"
```

Alternatively, you can set the keys via python functions as seen in the demo app.

### Place the Recaptcha component

```python
import reflex as rx

from reflex_google_recaptcha_v2 import google_recaptcha_v2

def index():
    return rx.vstack(
        ...,
        google_recaptcha_v2(),
    )
```

### Verify the Recaptcha response

Before taking actions on the backend, you should verify that the user
browser has passed validation of the token.

This value will be set for the specific tab that has completed validation and
persists for the lifetime of the Reflex session (until the tab is closed).

```python
import reflex as rx

from reflex_google_recaptcha_v2 import GoogleRecaptchaV2State


class MyState(rx.State):
    form_error: str

    async def handle_submit(self, form_data):
        ...
        recaptcha_state = await self.get_state(GoogleRecaptchaV2State)
        if not recaptcha_state.token_is_valid:
            self.form_error = "Invalid recaptcha. Are you a robot?"
            return
```