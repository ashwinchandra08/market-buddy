import yaml
from datetime import datetime, timezone

from src.main import all_symbols
from src.mock import mock_all
from src.mood import compute_mood
from src.render import render

CFG = yaml.safe_load(open("config.yaml", encoding="utf-8"))


def test_render_size_and_mode():
    data = mock_all(all_symbols(CFG))
    mood = compute_mood(data, CFG)
    img = render(CFG, data, mood, datetime.now(timezone.utc), None, "Buddy", "hello")
    assert img.size == (1072, 1448) and img.mode == "L"


def test_render_survives_missing_data():
    img = render(CFG, {}, compute_mood({}, CFG), datetime.now(timezone.utc), None, "Buddy", "no data")
    assert img.size == (1072, 1448)
