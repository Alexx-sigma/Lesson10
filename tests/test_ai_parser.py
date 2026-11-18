import pytest
from ai import generate_reply
from parser import parse_products


def test_ai_stub():
    assert "Привет" in generate_reply("Привет")


def test_ai_empty_prompt():
    with pytest.raises(ValueError):
        generate_reply("  ")


def test_parser_ignores_bad_items():
    data = [{"name": "Чай", "price": 100}, {"name": "", "price": 2}, {"name": "Кофе", "price": -1}]
    assert parse_products(data) == [{"name": "Чай", "price": 100}]


@pytest.mark.parametrize("text,expected", [
    ("Чай 100", {"name": "Чай", "price": 100.0}),
    ("Зелёный чай 99,5", {"name": "Зелёный чай", "price": 99.5}),
    ("  Хлеб   40  ", {"name": "Хлеб", "price": 40.0}),
])
def test_parse_item_line_ok(text, expected):
    from parser import parse_item_line
    assert parse_item_line(text) == expected


@pytest.mark.parametrize("text", ["", "Чай", "Чай abc", "Чай -5", "Чай nan", "Чай inf", None])
def test_parse_item_line_bad(text):
    from parser import parse_item_line
    assert parse_item_line(text) is None
