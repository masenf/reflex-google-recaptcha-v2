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

These keys can be obtained at Google's [Recaptcha Portal](https://console.cloud.google.com/security/recaptcha).
To access the secret key, which is required, go to the Integration tab and
select "Use legacy key" or "I'm integrating with a third party library".

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

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Contributing

Every pull request that changes `custom_components/` needs a news fragment — a
short markdown file under `news/`, named `<pr-number>.<type>.md`, written for
someone reading release notes:

```bash
uvx --from "reflex-release @ git+https://github.com/reflex-dev/reflex@1613d415c8d443cdd81d097fd08ae02213dfe04f#subdirectory=packages/reflex-release" \
  reflex-release create 123.bugfix.md
```

The types are `breaking`, `deprecation`, `feature`, `bugfix`, `performance`,
`docs` and `misc`. Before the PR number is known, name the file
`+something.bugfix.md` and rename it later. The `skip-changelog` label waives
the requirement for changes that are not user-facing.

Do not edit `CHANGELOG.md` by hand: a new version heading on `main` is what
triggers a publish, so CI rejects headings that were not written by the release
workflow.

## Releasing

Releases are changelog-driven, via
[reflex-release](https://github.com/reflex-dev/reflex/tree/main/packages/reflex-release).

1. Run **Dispatch release** from the Actions tab and pick an action
   (`release-patch`/`-minor`/`-major`, `release-post`, or one of the
   prerelease actions). It runs towncrier over `news/`, writes the new
   `CHANGELOG.md` section, and opens a pull request.
2. Merge that pull request. The push to `main` is what publishes: **Release
   from changelog** finds the changelog version that has no git tag, builds it,
   and waits for approval on the `pypi` environment before uploading.
3. After a successful upload the tag and GitHub release are created, and
   **Deploy demo app** redeploys `google_recaptcha_v2_demo` against the new version.

Because tags are only created after a successful upload, a failed release is
retried by pushing a fix on top of the changelog bump — there is nothing to
clean up.

Upgrading the release tooling is a `cli-command` bump in `pyproject.toml`
followed by `reflex-release sync`; the pull-request check fails while the
generated workflows are out of date.
