from bot import help_text, start_text


def test_start_mentions_help():
    assert "/help" in start_text()


def test_help_mentions_commands():
    assert "/start" in help_text()
    assert "/help" in help_text()


def test_help_mentions_shopping_commands():
    for cmd in ("/add", "/list", "/total", "/clear"):
        assert cmd in help_text()


def test_format_list_and_total():
    from bot import format_list, format_total
    assert "пуст" in format_list([])
    text = format_list([{"name": "Чай", "price": 100.0}, {"name": "Кофе", "price": 250.5}])
    assert "1. Чай — 100" in text and "2. Кофе — 250.50" in text
    assert format_total(350.5) == "Итого: 350.50"
