"""
Gera full_list.json e lite_list.json a partir da pasta de dados do jogo.

Como usar:
1. Coloque este script na raiz de uma pasta que contenha a pasta "files"
   (a mesma estrutura de DATA/ro.alynsampmobile.launcher/files que você já tem).
2. Ajuste BASE_URL abaixo para apontar pro seu usuário/repositório do GitHub.
3. Rode: python3 gerar_lista.py
4. Ele vai criar full_list.json e lite_list.json prontos para subir no repo,
   dentro da pasta data_lists/.
5. Suba a pasta "files" inteira (renomeada para "game_files") no mesmo repo,
   pra que as URLs geradas realmente existam.

Se algum dia você separar arquivos "lite" (sem texturas em alta, sem texdb
completa) dos "full", é só rodar o script duas vezes com pastas diferentes.
"""

import os
import json

BASE_URL = "https://raw.githubusercontent.com/east9-777/ATT-APK-NATIVO/main/game_files/"
RELEASE_URL = "https://github.com/east9-777/ATT-APK-NATIVO/releases/download/texdb-v1/"
LIMITE_GITHUB_MB = 90  # margem de seguranca abaixo do limite de 100MB do GitHub
DATA_DIR = "files"  # pasta com os arquivos do jogo
OUTPUT_DIR = "data_lists"

def gerar_lista(pasta):
    arquivos = []
    grandes = []  # arquivos que precisam ir pra uma Release
    for root, _, files in os.walk(pasta):
        for f in files:
            caminho_completo = os.path.join(root, f)
            caminho_relativo = os.path.relpath(caminho_completo, pasta).replace("\\", "/")
            tamanho = os.path.getsize(caminho_completo)
            tamanho_mb = tamanho / 1024 / 1024

            if tamanho_mb > LIMITE_GITHUB_MB:
                # nome sugerido para subir na Release, sem colisao entre pastas
                nome_release = caminho_relativo.replace("/", "__")
                url = RELEASE_URL + nome_release
                grandes.append({
                    "path": caminho_relativo,
                    "tamanho_mb": round(tamanho_mb, 1),
                    "nome_sugerido_na_release": nome_release,
                    "url_gerada": url
                })
            else:
                url = BASE_URL + caminho_relativo

            arquivos.append({
                "name": f,
                "path": caminho_relativo,
                "size": tamanho,
                "url": url,
                "gpu": "all"
            })
    return {"files": arquivos}, grandes

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lista, grandes = gerar_lista(DATA_DIR)

    with open(os.path.join(OUTPUT_DIR, "full_list.json"), "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUTPUT_DIR, "lite_list.json"), "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

    total_mb = sum(x["size"] for x in lista["files"]) / 1024 / 1024
    print(f"{len(lista['files'])} arquivos | {total_mb:.1f} MB no total")
    print("Arquivos gerados em data_lists/full_list.json e data_lists/lite_list.json")

    if grandes:
        with open(os.path.join(OUTPUT_DIR, "arquivos_para_release.json"), "w", encoding="utf-8") as f:
            json.dump(grandes, f, indent=2, ensure_ascii=False)
        print(f"\n{len(grandes)} arquivo(s) passam de {LIMITE_GITHUB_MB}MB e NAO devem ir pro repo normal.")
        print("Veja data_lists/arquivos_para_release.json: cada item tem o nome sugerido")
        print("pra subir na Release e a URL que ja foi escrita no full_list.json/lite_list.json.")
        print("So falta: 1) subir esses arquivos na Release com esse nome exato")
        print("          2) conferir se a tag da Release bate com RELEASE_URL no topo do script")
