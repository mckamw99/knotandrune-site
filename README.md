# Knot & Rune website

Static site for knotandrune.com, hosted on GitHub Pages (same setup as aequitas-site).

- Edit page content in `src/*.html`; shared header, footer, page titles and the email sign-up settings live in `build.py`.
- Run `python3 build.py` to regenerate the pages in the site root, then commit.
- Styles: `assets/styles.css`. Logo files come from the locked v0.6 master (KnotAndRune_Logo_Files_v0.6.zip in Drive).
- Email sign-up: create a Google Form with one Email question, then set `SIGNUP_FORM_ACTION` and `SIGNUP_EMAIL_ENTRY` in `build.py` and rebuild.
