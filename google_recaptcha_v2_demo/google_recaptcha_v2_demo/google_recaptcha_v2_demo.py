import reflex as rx
import reflex_google_recaptcha_v2
from reflex_google_recaptcha_v2 import GoogleRecaptchaV2State, google_recaptcha_v2

if not reflex_google_recaptcha_v2.is_key_set():
    # Default test keys (will display warning in browser if used).
    reflex_google_recaptcha_v2.set_site_key("6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI")
    reflex_google_recaptcha_v2.set_secret_key(
        "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    )


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
