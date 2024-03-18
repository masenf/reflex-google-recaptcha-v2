"""Reflex custom component GoogleRecaptchaV2."""

from __future__ import annotations

import os
from typing import Any, Dict

import httpx

import reflex as rx


VERIFY_ENDPOINT = "https://www.google.com/recaptcha/api/siteverify"
SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")
SECRET_KEY = os.environ.get("RECAPTCHA_SECRET_KEY")


def set_site_key(site_key: str):
    """Set the site key."""
    global SITE_KEY
    SITE_KEY = site_key


def set_secret_key(secret_key: str):
    """Set the secret key."""
    global SECRET_KEY
    SECRET_KEY = secret_key


class GoogleRecaptchaV2State(rx.State):
    recaptcha_verify_response_json: str = rx.LocalStorage(sync=True)
    _is_valid: bool = False

    def verify_captcha(self, token: str):
        """Validate the captcha token."""
        payload = {
            "secret": SECRET_KEY,
            "response": token,
            "remoteip": getattr(
                self.router.headers, "x_forwarded_for", self.router.session.client_ip
            ),
        }
        resp = httpx.post(VERIFY_ENDPOINT, data=payload)
        resp.raise_for_status()
        try:
            self._is_valid = resp.json().get("success", False)
        except ValueError:
            pass

    @rx.cached_var
    def token_is_valid(self) -> bool:
        """Check if the token is valid."""
        return self._is_valid


class GoogleRecaptchaV2(rx.NoSSRComponent):
    """GoogleRecaptchaV2 component.

    Event Triggers:
        - async_script_on_load: optional callback when the google recaptcha script has been loaded
        - on_change: The function to be called when the user successfully completes the captcha
        - on_errored: optional callback when the challenge errored, most likely due to network issues.
        - on_expired: optional callback when the challenge is expired and has to be redone by user. By default it will call the onChange with null to signify expired callback.
    """

    # The React library to wrap.
    library = "react-google-recaptcha"

    # The React component tag.
    tag = "ReCAPTCHA"

    is_default = True

    # Positions ReCAPTCHA badge. Only for invisible ReCAPTCHA. bottomright, bottomleft or inline.
    badge: rx.Var[str]

    # Set the hl parameter, which allows the captcha to be used from different languages, see reCAPTCHA hl
    hl: rx.Var[str]

    # For plugin owners to not interfere with existing reCAPTCHA installations on a page. If true, this reCAPTCHA instance will be part of a separate ID space. (default: false)
    isolated: rx.Var[bool]

    # The API client key (required).
    sitekey: rx.Var[str]

    # The size of the widget - compact, normal, or invisible (default: normal).
    size: rx.Var[str]

    # Set the stoken parameter, which allows the captcha to be used from different domains, see reCAPTCHA secure-token
    stoken: rx.Var[str]

    # The tabindex on the element (default: 0).
    tabindex: rx.Var[int]

    # The type of initial captcha - image or audio (defaults: image).
    type: rx.Var[str]

    # The theme of the widget - light or dark (defaults: light).
    theme: rx.Var[str]

    @classmethod
    def create(cls, **props) -> "GoogleRecaptchaV2":
        if props.get("size") == "invisible":
            props.setdefault("id", rx.vars.get_unique_variable_name())
            raise NotImplementedError("Invisible mode is not currently working.")
        props.setdefault("sitekey", SITE_KEY)
        props.setdefault("on_change", GoogleRecaptchaV2State.verify_captcha)
        return super().create(**props)

    def get_event_triggers(self) -> Dict[str, Any]:
        return {
            **super().get_event_triggers(),
            "async_script_on_load": lambda e0: [e0],
            "on_change": lambda e0: [e0],
            "on_errored": lambda e0: [e0],
            "on_expired": lambda e0: [e0],
        }

    def api(self) -> "GoogleRecaptchaV2API" | None:
        raise NotImplementedError("Invisible mode is not currently working.")
        ref = self.get_ref()
        if ref:
            return GoogleRecaptchaV2API(ref_name=self.get_ref())
        raise ValueError("Be sure to set an id on the component to use the API.")


google_recaptcha_v2 = GoogleRecaptchaV2.create


class GoogleRecaptchaV2API(rx.Base):
    """The API for triggering execute() in invisible mode.

    Ref API:
        getValue() returns the value of the captcha field
        getWidgetId() returns the recaptcha widget Id
        reset() forces reset. See the JavaScript API doc
        execute() programmatically invoke the challenge
            need to call when using "invisible" reCAPTCHA - example below

    (TODO: Not currently working with Reflex.)
    """

    ref_name: str

    def _get_api_spec(self, fn_name) -> rx.Var[rx.EventChain]:
        return rx.Var.create(
            f"{rx.Var.create(self.ref_name).as_ref()}?.current?.{fn_name}",
            _var_is_local=False,
            _var_is_string=False,
        )._replace(
            _var_type=rx.EventChain,
        )

    def get_value(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("get_value")

    def get_widget_id(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("get_widget_id")

    def reset(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("reset")

    def execute(self) -> rx.Var[rx.EventChain]:
        return self._get_api_spec("execute")
