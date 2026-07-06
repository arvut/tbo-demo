# tbo-demo

Demo landing page for **TBO Treuhand AG** (Zürich) — a static single-page site
hosted on GitHub Pages.

- **Live:** https://arvut.github.io/tbo-demo/
- **Language:** German (Swiss Hochdeutsch)
- **Stack:** plain static HTML/CSS, no build step. Fonts and images are bundled
  in `assets/` so the page is fully self-contained.

## Structure

Everything lives in `index.html` with inline styles. Design tokens are defined
in the `:root` block (`--navy`, `--soft`, `--band`, `--radius`, …). Assets:

- `assets/fonts/` — bundled web fonts (woff2).
- `assets/img/` — images. When replacing an image, bump the `?v=N` query in the
  HTML so the CDN serves the new file.

## Local preview

No toolchain required — open `index.html` in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy

Push to `main` — GitHub Actions (`.github/workflows/pages.yml`) publishes to
GitHub Pages automatically. Verify at https://arvut.github.io/tbo-demo/.

## Contact

Maintained by Arvut. Questions → Alex (al@arvut.ch).
