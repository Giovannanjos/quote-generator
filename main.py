import json
import random
import requests

# Endpoints de APIs públicas com grandes acervos
ZENQUOTES_URL = "https://zenquotes.io/api/random"
DUMMYJSON_URL = "https://dummyjson.com/quotes"
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
    "3": ("life", "Vida / Filosofia"),
    "4": ("history", "Histórico / Famosos"),
    "0": (None, "Aleatório (Acervo Geral Global)")
}


def fetch_from_zenquotes():
    """Busca citação no acervo da ZenQuotes."""
    try:
        response = requests.get(ZENQUOTES_URL, timeout=4)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return {"content": data[0]["q"], "author": data[0]["a"]}
    except (requests.RequestException, KeyError, IndexError):
        return None


def fetch_from_dummyjson(category=None):
    """Busca citação no acervo DummyJSON filtrando por tag se aplicável."""
    try:
        if category:
            url = f"{DUMMYJSON_URL}/tag/{category}"
            response = requests.get(url, timeout=4)
            response.raise_for_status()
            data = response.json()
            quotes = data.get("quotes", [])
            if quotes:
                selected = random.choice(quotes)
                return {"content": selected["quote"], "author": selected["author"]}
        else:
            url = f"{DUMMYJSON_URL}/random"
            response = requests.get(url, timeout=4)
            response.raise_for_status()
            data = response.json()
            return {"content": data["quote"], "author": data["author"]}
    except (requests.RequestException, KeyError, IndexError):
        return None


def load_local_quote(category=None):
    """Carrega citação do acervo JSON local."""
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
    """Tenta obter citações via provedores online em ordem e faz fallback local."""
    # Se uma categoria específica for pedida, consulta via DummyJSON
    if category:
        quote = fetch_from_dummyjson(category)
        if quote:
            return quote
    else:
        # Modo geral aleatório: tenta ZenQuotes primeiro
        quote = fetch_from_zenquotes()
        if quote:
            return quote
        
        # Tenta DummyJSON se ZenQuotes falhar
        quote = fetch_from_dummyjson()
        if quote:
            return quote

    # Se as APIs falharem ou estiver sem internet, usa o banco local
    return load_local_quote(category)


def format_quote(quote):
    """Aplica formatação com bordas dinâmicas e cores no terminal."""
    if not quote:
        return f"\n{YELLOW}Nenhuma citação encontrada para o filtro selecionado.{RESET}"

    border = "─" * max(len(quote['author']) + 10, 20)
    return (
        f"\n{CYAN}\"{quote['content']}\"{RESET}\n"
        f"{YELLOW}{border}{RESET}\n"
        f"— {GREEN}{BOLD}{quote['author']}{RESET}\n"
    )


def show_menu():
    """Exibe o menu de opções."""
    print(f"\n{BOLD}Escolha uma categoria:{RESET}")
    for key, (_, label) in CATEGORIES.items():
        print(f"[{key}] {label}")


def main():
    print(f"{BOLD}=== Gerador de Citações (Acervo Estendido) ==={RESET}")
    
    while True:
        show_menu()
        choice = input("\nDigite o número da opção (ou Ctrl+C para sair): ").strip()

        if choice not in CATEGORIES:
            print(f"\n{YELLOW}Opção inválida! Digite um número do menu.{RESET}")
            continue

        category_slug, category_label = CATEGORIES[choice]
        print(f"\nObtendo citação ({category_label})...")
        
        quote = get_quote(category_slug)
        print(format_quote(quote))
        
        input(f"\n{BOLD}Pressione ENTER para voltar ao menu...{RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAté logo!")
