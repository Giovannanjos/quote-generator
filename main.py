import json
import random
import requests

API_URL = "https://api.quotable.io/random"
LOCAL_FILE = "quotes.json"


def fetch_online_quote():
    """Busca uma citação aleatória via API pública."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {"content": data["content"], "author": data["author"]}
    except (requests.RequestException, KeyError):
        return None


def load_local_quote():
    """Carrega uma citação do arquivo local JSON como fallback."""
    try:
        with open(LOCAL_FILE, "r", encoding="utf-8") as file:
            quotes = json.load(file)
            return random.choice(quotes)
    except (FileNotFoundError, json.JSONDecodeError, IndexError):
        return None


def get_quote():
    """Obtém citação (online primeiro, offline se falhar)."""
    quote = fetch_online_quote()
    if not quote:
        quote = load_local_quote()
    return quote


def format_quote(quote):
    """Formata a exibição da citação no terminal."""
    if not quote:
        return "Nenhuma citação encontrada."

    border = "─" * (len(quote['author']) + 10)
    return f'\n"{quote["content"]}"\n{border}\n— {quote["author"]}\n'


def main():
    print("=== Gerador de Citações ===")
    while True:
        input("\nPressione ENTER para gerar uma citação (ou Ctrl+C para sair)...")
        quote = get_quote()
        print(format_quote(quote))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAté logo!")