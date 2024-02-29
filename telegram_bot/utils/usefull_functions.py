from utils.bot_context import languages


def _short(key: str):
    result = []

    for item in languages:
        result.append(
            languages[item]['reply_button'][key]
        )

    return result
