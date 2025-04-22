import requests

def search_torrents(query, category="all"):
    base_url = "https://apibay.org/q.php"
    params = {"q": query, "cat": category}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        torrents = response.json()
        
        if not torrents:
            print("Nenhum resultado encontrado.")
            return
        
        for torrent in torrents[:10]:  # Limitar a 10 resultados
            print(f"Nome: {torrent['name']}")
            print(f"Seeders: {torrent['seeders']}")
            print(f"Leechers: {torrent['leechers']}")
            print(f"Magnet: magnet:?xt=urn:btih:{torrent['info_hash']}")
            print("-" * 40)
    except Exception as e:
        print(f"Erro ao buscar torrents: {e}")

if __name__ == "__main__":
    termo = input("Digite o termo de busca: ")
    search_torrents(termo)