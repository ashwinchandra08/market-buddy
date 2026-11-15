# Contributing

Thanks for helping! Small, focused PRs are best.

## Dev setup
```bash
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
python -m src.main --mock --bias 0.9              # preview without network -> site/dash.png
python -m src.main --mock --force-tier 4          # preview any mood 0..4
```

## Guidelines
- Keep the output **grayscale, high-contrast, 1072×1448** (Kindle Paperwhite 3). Other devices: change `size:` in `config.yaml`.
- Don't commit Pokémon artwork, Kindle binaries (`fbink`, `curl`) or personal URLs/tokens.
- Shell scripts must stay busybox-`ash` compatible (`sh -n` runs in CI).
- Add a test when you change mood logic or the renderer.
- Be kind and constructive in issues and reviews.

## Ideas welcome
Other devices/resolutions, more mood tiers, more markets, better e-ink dithering, a battery-friendly RTC-wake mode.
