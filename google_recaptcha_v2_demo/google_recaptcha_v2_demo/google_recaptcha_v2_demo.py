import reflex as rx

import reflex_google_recaptcha_v2
from reflex_google_recaptcha_v2 import google_recaptcha_v2, GoogleRecaptchaV2State


reflex_google_recaptcha_v2.set_site_key("6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI")
reflex_google_recaptcha_v2.set_secret_key("6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")


class State(rx.State):
    pass


def index() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Token is valid? ",
            rx.cond(GoogleRecaptchaV2State.token_is_valid, "Yes", "No"),
        ),
        rx.cond(
            rx.State.is_hydrated & ~GoogleRecaptchaV2State.token_is_valid,
            google_recaptcha_v2(),
        ),
        height="100vh",
        align="center",
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
