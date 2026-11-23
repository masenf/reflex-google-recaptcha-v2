# Changelog

Notable changes to `reflex-google-recaptcha-v2`.

New entries are added by [towncrier](https://towncrier.readthedocs.io/) from the
news fragments under `news/` — see [Releasing](README.md#releasing). Everything
below `v0.1.0.post1` was reconstructed from the git history after the fact, so
it summarizes each release rather than reproducing entries that were never
written; alpha releases are omitted.

<!-- towncrier release notes start -->

## v0.1.0.post1 (2025-09-05)

### Miscellaneous

- Build and upload the distribution with `uv` in the publish workflow. Packaging-only release; the code is identical to v0.1.0.

## v0.1.0 (2025-02-12)

### Breaking Changes

- Require `reflex>=0.6.8`. ([#4](https://github.com/masenf/reflex-google-recaptcha-v2/issues/4))
- Require Python 3.10 or newer, up from 3.8.
- `GoogleRecaptchaV2State.verify_captcha` raises `RuntimeError` when the site or secret key is not set, instead of silently failing validation. Use the new `is_key_set()` to check first. ([#3](https://github.com/masenf/reflex-google-recaptcha-v2/issues/3))

### Features

- Derive the package version from git tags with `setuptools-scm` instead of hard-coding it in `pyproject.toml`. ([#4](https://github.com/masenf/reflex-google-recaptcha-v2/issues/4))

### Bug Fixes

- Verify the captcha token with an async request, so validation no longer blocks the server. ([#4](https://github.com/masenf/reflex-google-recaptcha-v2/issues/4))

### Miscellaneous

- Run ruff and pyright from pre-commit, and check them on every pull request. ([#4](https://github.com/masenf/reflex-google-recaptcha-v2/issues/4))

## v0.0.4 (2024-09-19)

### Bug Fixes

- Replace `rx.cached_var`, deprecated in Reflex 0.6.0, with `rx.var(cache=True)`. ([#2](https://github.com/masenf/reflex-google-recaptcha-v2/issues/2))

## v0.0.3 (2024-04-10)

### Breaking Changes

- Require `reflex>=0.4.6`. ([#1](https://github.com/masenf/reflex-google-recaptcha-v2/issues/1))

### Bug Fixes

- Declare the `on_change` event trigger with the `rx.EventHandler` annotation syntax, and declare `httpx` as a dependency. ([#1](https://github.com/masenf/reflex-google-recaptcha-v2/issues/1))
- Export only the public API from the package: `GoogleRecaptchaV2`, `GoogleRecaptchaV2State`, `google_recaptcha_v2`, `set_site_key` and `set_secret_key`. ([#1](https://github.com/masenf/reflex-google-recaptcha-v2/issues/1))

## v0.0.2 (2024-03-21)

First tagged release.

### Features

- Google reCAPTCHA v2 for Reflex apps: `google_recaptcha_v2` renders the checkbox challenge, and `GoogleRecaptchaV2State` verifies the returned token against Google's API on the backend, using the keys configured with `set_site_key` and `set_secret_key`.
