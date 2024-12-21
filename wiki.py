import wikipediaapi


def detect_language(query):
    if any("\u0400" <= char <= "\u04FF" for char in query):  # Cyrillic characters
        return 'uk'  # Ukrainian Wikipedia
    # Add more rules for other languages if needed
    return 'en'  # Default to English


def fetch_wikipedia_article(query):
    language = detect_language(query)

    user_agent = "MyWikipediaBot/1.0 (https://example.com; myemail@example.com)"

    wiki = wikipediaapi.Wikipedia(user_agent, language)  # Use 'uk' for Ukrainian articles

    page = wiki.page(query)

    if not page.exists():
        return f"No article found for '{query}'. Please try again with a different request."

    title = page.title
    summary = page.summary
    url = page.fullurl

    output = "Wiki answer:\n\n"
    output += f"{title}\n\n"
    output += f"{summary}\n\n"
    output += f"{url}"
    return output
