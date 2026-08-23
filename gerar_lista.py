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

BASE_URL = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/game_files/"
DATA_DIR = "files"  # pasta com os arquivos do jogo
OUTPUT_DIR = "data_lists"

def gerar_lista(pasta):
    arquivos = []
    for root, _, files in os.walk(pasta):
        for f in files:
            caminho_completo = os.path.join(root, f)
            caminho_relativo = os.path.relpath(caminho_completo, pasta).replace("\\", "/")
            tamanho = os.path.getsize(caminho_completo)
            arquivos.append({
                "name": f,
                "path": caminho_relativo,
                "size": tamanho,
                "url": BASE_URL + caminho_relativo,
                "gpu": "all"
            })
    return {"files": arquivos}

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    lista = gerar_lista(DATA_DIR)

    with open(os.path.join(OUTPUT_DIR, "full_list.json"), "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

    with open(os.path.join(OUTPUT_DIR, "lite_list.json"), "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=2, ensure_ascii=False)

    total_mb = sum(x["size"] for x in lista["files"]) / 1024 / 1024
    print(f"{len(lista['files'])} arquivos | {total_mb:.1f} MB no total")
    print("Arquivos gerados em data_lists/full_list.json e data_lists/lite_list.json")
