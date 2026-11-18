"""Offline data normalization. External HTTP is deliberately out of scope."""


def parse_products(items: list[dict]) -> list[dict]:
    result = []
    for item in items:
        name = item.get("name")
        price = item.get("price")
        if not isinstance(name, str) or not name.strip():
            continue
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            continue
        result.append({"name": name.strip(), "price": price})
    return result


def parse_item_line(text: str) -> dict | None:
    """Parse 'Чай 100' or 'Зелёный чай 99,5' into {"name", "price"}; None if invalid."""
    if not isinstance(text, str):
        return None
    parts = text.strip().rsplit(maxsplit=1)
    if len(parts) != 2:
        return None
    name, raw_price = parts
    try:
        price = float(raw_price.replace(",", "."))
    except ValueError:
        return None
    if price != price or price in (float("inf"), float("-inf")) or price < 0:
        return None
    return {"name": name.strip(), "price": price}
