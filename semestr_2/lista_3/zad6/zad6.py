import argparse
import requests
import webbrowser
import urllib.parse

def get_random_wikipedia_article():
    url = "https://en.wikipedia.org/wiki/Special:Random"
    response = requests.get(url)
    return response.url

def get_article_title(article_url):
    parts = article_url.split("/wiki/")
    if len(parts) > 1:
        title_encoded = parts[1]
        title = urllib.parse.unquote(title_encoded)
        return title.replace("_", " ")
    return "Unknown Title"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Pobiera losowy artykuł z Wikipedii i, wyświetla go w przeglądarce za pozwoleniem usera"
    )
    args = parser.parse_args()

    # Pobierz losowy artykuł i wyodrębnij tytuł
    article_url = get_random_wikipedia_article()
    title = get_article_title(article_url)
    print(f"Losowy artykuł: {title}")

    # Pytamy użytkownika o otwarcie artykułu
    answer = input("Czy chcesz otworzyć ten artykuł w przeglądarce? Wybierz: t lub n")
    if answer.lower() in ['t', 'tak', 'y', 'yes']:
        webbrowser.open(article_url)
        print("Artykuł został otwarty w przeglądarce.")
    else:
        print("Artykuł nie został otwarty.")
