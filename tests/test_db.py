from db import get_user, init_db, save_user


def test_save_and_read_user(tmp_path):
    path = tmp_path / "test.sqlite3"
    init_db(path)
    save_user(123, "student", path)
    assert get_user(123, path) == "student"
    assert get_user(999, path) is None


def test_user_update(tmp_path):
    path = tmp_path / "test.sqlite3"
    init_db(path)
    save_user(123, "old", path)
    save_user(123, "new", path)
    assert get_user(123, path) == "new"


def test_items_add_list_total_clear(tmp_path):
    from db import add_item, clear_items, list_items, total_price
    path = tmp_path / "test.sqlite3"
    init_db(path)
    add_item(1, "Чай", 100, path)
    add_item(1, "Кофе", 250.5, path)
    add_item(2, "Чужое", 999, path)
    assert list_items(1, path) == [{"name": "Чай", "price": 100}, {"name": "Кофе", "price": 250.5}]
    assert total_price(1, path) == 350.5
    assert total_price(3, path) == 0
    assert clear_items(1, path) == 2
    assert list_items(1, path) == []
    assert list_items(2, path) != []
