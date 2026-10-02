import json
import random
import requests

# API alternativa gratuita e ativa
API_URL = "https://dummyjson.com/quotes/random"
LOCAL_FILE = "quotes.json"


def fetch_online_quote():
    """Busca uma citação aleatória via API pública."""
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        # O DummyJSON devolve as chaves 'quote' e 'author'
        return {"content": data["quote"], "author": data["author"]}
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


# Códigos de cores ANSI
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"


def format_quote(quote):
    """Formata a exibição da citação no terminal com cores."""
    if not quote:
        return "Nenhuma citação encontrada."

    border = "─" * (len(quote['author']) + 10)
    return (
        f"\n{CYAN}\"{quote['content']}\"{RESET}\n"
        f"{YELLOW}{border}{RESET}\n"
        f"— {GREEN}{BOLD}{quote['author']}{RESET}\n"
    )


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
