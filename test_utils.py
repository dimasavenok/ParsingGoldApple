from src.models import Perfume
from src.utils import save_to_csv, save_to_json, clean_html_text


def test_clean_html_text():
    html = "Test<br>Line<br/>Another<br />end <p>ignored</p>"
    result = clean_html_text(html)
    assert result == "Test\nLine\nAnother\nend ignored"


def test_save_to_json(tmp_path):
    perfume = Perfume(url="t", brand="b")
    file = tmp_path / "test.json"

    save_to_json([perfume], file)

    assert file.exists()
    content = file.read_text(encoding="utf-8")
    assert '"brand": "b"' in content


def test_save_to_csv(tmp_path):
    perfume = Perfume(url="t", brand="b", name="n")
    file = tmp_path / "test.csv"

    save_to_csv([perfume], file)

    assert file.exists()
    content = file.read_text(encoding="utf-8")
    assert "brand" in content
    assert "b" in content