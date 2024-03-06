from re import findall, sub


def clean_price(price):
    cleaned_price = sub(
        r"[^\d.]", "", price
    )  # Remove all non-digit and non-decimal point characters
    dot_count = len([char for char in cleaned_price if char == "."]) - 1
    cleaned_price = sub(
        r"\.(?=.*\.)", " ", cleaned_price, count=dot_count
    )  # Replace the first occurrence of '.' with a space
    cleaned_price = sub(
        r"(\.\d{2})\d*$", r"\1", cleaned_price
    )  # Keep only the decimal point before the last two numbers
    return cleaned_price


def parse_text(response):
    """
    This function is not guaranteed to work all the time because it relies on parsing the text which can be unpredictable structure wise.
    """
    full_text = response.full_text_annotation.text

    sections = full_text.split("\n")

    print(sections)

    symbol_pattern = r"\w+,\s"
    action_pattern = r"\s(sell|buy)\s\d+\.\d+"
    date_pattern = r"\d\d\d\d\.\d\d\.\d\d"
    price_pattern = r"\d+\s*\d+.\d+"
    roi_pattern = r"(\+|\-)\d+.\d+"

    clean_matches = []

    symbol, action = None, None

    for section in sections:
        if findall(symbol_pattern, section):
            symbol = findall(symbol_pattern, section)[0][:-2]
        if findall(action_pattern, section):
            action = findall(action_pattern, section)[0].split(" ")[0]
            continue
        if findall(date_pattern, section):
            continue
        if findall(roi_pattern, section):
            continue
        if findall(price_pattern, section):
            if any(char.isalpha() for char in section):
                no_comma_test = findall(r"\d+(\s|\.)\d\d", section)
                if no_comma_test:
                    clean_matches.append(sub(r"[a-zA-Z:]", "", section))
                    continue
            else:
                for match in findall(price_pattern, section):
                    clean_matches.append(match)
                    continue

    print(clean_matches)
    action_price = clean_matches[0]
    current_price = clean_matches[1]
    take_profit_price = clean_matches[2]

    return {
        "SYMBOL": symbol,
        "ACTION": action,
        "ACTION PRICE": action_price,
        "CURRENT PRICE": current_price,
        "T/P": take_profit_price,
    }


def parse_geometry(width, height, response):
    """
    This function is better because it relies on the position of the text which is fixed.
    """

    # Filter half of the image which is irrelevant.

    texts = [
        {
            "text": text.description,
            "x": text.bounding_poly.vertices[0].x,
            "y": text.bounding_poly.vertices[0].y,
        }
        for text in response.text_annotations[1:]
    ]

    useful_side_texts = [text for text in texts if (text["x"] < width / 2)]

    symbol_action_texts = [
        text["text"] for text in useful_side_texts if (text["y"] < height / 12)
    ]
    action_current_texts = [
        text["text"]
        for text in useful_side_texts
        if (text["y"] > height * (3 / 24) and text["y"] < height * (3 / 12))
    ]

    sl_texts = [
        text["text"]
        for text in useful_side_texts
        if (text["x"] > width / 4)
        and (text["y"] > height * 1 / 2 and text["y"] < height * (1 / 2) * (1 + 1 / 3))
        and any(char.isdigit() for char in text["text"])
    ]
    tp_texts = [
        text["text"]
        for text in useful_side_texts
        if (text["x"] > width / 4)
        and (
            text["y"] > height * (1 / 2) * (1 + 1 / 3)
            and text["y"] < height * (1 / 2) * (1 + 2 / 3)
        )
        and any(char.isdigit() for char in text["text"])
    ]

    symbol_pattern = r"\w+"
    action_pattern = r"(sell|buy)\d+\.\d+"
    price_pattern = r"\d+\s*.\d+\.\d\d"

    symbol = None
    action = None
    entry_price = None
    current_price = None
    sl_price = None
    tp_price = None

    symbol_action = "".join(symbol_action_texts)

    symbol = findall(symbol_pattern, symbol_action)[0]
    action = findall(action_pattern, symbol_action)[0]

    action_current = " ".join(action_current_texts)

    entry_price = findall(price_pattern, action_current)[0]
    current_price = findall(price_pattern, action_current)[1]

    if sl_texts:
        sl = " ".join(sl_texts)

        # Remove any non-digit character
        if any(char.isalpha() for char in sl):
            sl = sub(r"[a-zA-Z]", "", sl)

        normal_match = findall(price_pattern, sl)
        if normal_match:
            sl_price = normal_match[0]

        special_match = findall(r"\d+\s*\d+\s\d\d", sl)
        if special_match:
            sl_price = sl[:-3] + "." + sl[-2:]

    if tp_texts:
        tp = " ".join(tp_texts)

        if any(char.isalpha() for char in tp):
            tp = sub(r"[a-zA-Z]", "", tp)

        normal_match = findall(price_pattern, tp)
        if normal_match:
            tp_price = normal_match[0]

        special_match = findall(r"\d+\s*\d+\s\d\d", tp)
        if special_match:
            tp_price = tp[:-3] + "." + tp[-2:]

    return {
        "SYMBOL": symbol.upper(),
        "ACTION": action.upper(),
        "ENTRY PRICE": clean_price(entry_price),
        "CURRENT PRICE": clean_price(current_price),
        "S/L": "-" if sl_price == None else clean_price(sl_price),
        "T/P": clean_price(tp_price),
    }
