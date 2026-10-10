import json
import random
import requests

BASE_API_URL = "https://dummyjson.com/quotes"
LOCAL_FILE = "quotes.json"

# Códigos de cores para o terminal
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

CATEGORIES = {
    "1": ("inspirational", "Inspiradoras"),
    "2": ("wisdom", "Sabedoria"),
    "3": ("life", "Vida"),
    "4": ("history", "Histórico/Famosos"),
    "0": (None, "Aleatório (Todas)")
}


def fetch_online_quote(category=None):
    """Busca citação via API pública (com ou sem filtro de categoria)."""
    try:
        if category:
            url = f"{BASE_API_URL}/tag/{category}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            quotes = data.get("quotes", [])
            if quotes:
                selected = random.choice(quotes)
                return {"content": selected["quote"], "author": selected["author"]}
        else:
            url = f"{BASE_API_URL}/random"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return {"content": data["quote"], "author": data["author"]}
    except (requests.RequestException, KeyError, IndexError):
        return None


def load_local_quote(category=None):
    """Carrega citação do JSON local (com ou sem filtro)."""
    try:
        with open(LOCAL_FILE, "r", encoding="utf-8") as file:
            quotes = json.load(file)
            if category:
                filtered = [q for q in quotes if category in q.get("tags", [])]
                if filtered:
                    return random.choice(filtered)
            return random.choice(quotes)
    except (FileNotFoundError, json.JSONDecodeError, IndexError):
        return None


def get_quote(category=None):
    """Obtém citação respeitando a categoria escolhida."""
    quote = fetch_online_quote(category)
    if not quote:
        quote = load_local_quote(category)
    return quote


def format_quote(quote):
    """Formata a exibição da citação com cores no terminal."""
    if not quote:
        return f"\n{YELLOW}Nenhuma citação encontrada para esta categoria.{RESET}"

    border = "─" * (len(quote['author']) + 10)
    return (
        f"\n{CYAN}\"{quote['content']}\"{RESET}\n"
        f"{YELLOW}{border}{RESET}\n"
        f"— {GREEN}{BOLD}{quote['author']}{RESET}\n"
    )


def show_menu():
    """Exibe o menu de categorias."""
    print(f"\n{BOLD}Escolha uma categoria:{RESET}")
    for key, (_, label) in CATEGORIES.items():
        print(f"[{key}] {label}")


def main():
    print(f"{BOLD}=== Gerador de Citações ==={RESET}")
    
    while True:
        show_menu()
        choice = input("\nDigite o número da opção (ou Ctrl+C para sair): ").strip()

        if choice not in CATEGORIES:
            print(f"\n{YELLOW}Opção inválida! Tente novamente.{RESET}")
            continue

        category_slug, category_label = CATEGORIES[choice]
        print(f"\nBuscando citação ({category_label})...")
        
        quote = get_quote(category_slug)
        print(format_quote(quote))
        
        input(f"\n{BOLD}Pressione ENTER para continuar...{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAté logo!")
