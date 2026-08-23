# Passo a passo — migrar o servidor de update pro GitHub

## 1. Crie o repositório novo
No GitHub, crie um repo **público** (raw.githubusercontent.com só funciona com repo público),
por exemplo `nativo-apk-data`.

## 2. Estrutura de pastas dentro do repo

```
/update.json
/servers.json
/banned.json
/faq.json
/changelog.txt
/images/previews.json
/data_lists/full_list.json
/data_lists/lite_list.json
/data_lists/samp_list.json
/game_files/...   <- toda a pasta "files" do seu DATA.zip vai aqui dentro
```

Suba todos os arquivos desta pasta (`repo_files/`) exatamente nessa estrutura.
A pasta `game_files/` deve conter o conteúdo inteiro da sua pasta
`DATA/ro.alynsampmobile.launcher/files` (sem a pasta `texdb`, que você disse ser grande —
veja a seção 5).

## 3. Troque east9-777 e ATT-APK-NATIVO
Em `update.json`, `data_lists/full_list.json`, `data_lists/lite_list.json` e
`images/previews.json`, troque `east9-777/ATT-APK-NATIVO` pelo seu usuário e nome real do
repositório. O `full_list.json` e `lite_list.json` anexados já foram gerados a partir
dos seus 254 arquivos reais (114 MB) — só falta trocar essa parte da URL.

Dica: no app do GitHub (ou até pelo navegador do celular), dá pra usar "editar arquivo"
e um find & replace rápido em cada JSON.

## 4. Atualize o Utils.java
Já apliquei as mudanças no arquivo `Utils.java` anexado (pasta `java/`). Ele agora
aponta pro `https://raw.githubusercontent.com/east9-777/ATT-APK-NATIVO/main/`. Substitua
o arquivo original do projeto por esse, e troque lá dentro também o placeholder
`east9-777`/`ATT-APK-NATIVO`, e o link do Discord (`SEU_CONVITE`). Veja a seção 8 para os
outros dois arquivos novos/alterados (`ArchiveData.java` e `UpdateService.java`).

## 5. Sobre a texdb (arquivos grandes, acima de 100 MB)
GitHub bloqueia arquivos individuais maiores que 100 MB num push normal (sem Git LFS).
O `gerar_lista.py` já foi atualizado pra lidar com isso automaticamente: qualquer
arquivo acima de 90 MB (margem de segurança) é listado à parte, num
`data_lists/arquivos_para_release.json`, com um nome sugerido e a URL já calculada.

Passo a passo (tudo pelo navegador do celular):

1. Abra `https://github.com/east9-777/ATT-APK-NATIVO/releases/new`
2. Em "Tag version" ponha `texdb-v1` (mesmo valor que está em `RELEASE_URL` no script)
3. Em "Release title" ponha algo como `Texturas (texdb)`
4. Toque na área "Attach binaries..." e selecione os arquivos grandes da texdb
5. **Renomeie cada arquivo** ao subir para o nome indicado em
   `nome_sugerido_na_release` (evita colisão, já que Release não tem pastas)
6. Publique a Release
7. Rode `gerar_lista.py` de novo (com a texdb já dentro da pasta `files/`) — o
   `full_list.json`/`lite_list.json` já saem com a URL certa apontando pra Release
   para esses arquivos, e pro repo normal para o resto.

Os arquivos pequenos da texdb (abaixo de 90 MB) continuam indo normalmente dentro de
`game_files/`, junto com o resto.


## 6. Teste
Depois de subir tudo, abra `https://raw.githubusercontent.com/east9-777/ATT-APK-NATIVO/main/update.json`
no navegador do celular. Se aparecer o JSON puro (não erro 404), o app já vai conseguir
ler. Nesse momento os 3 problemas somem: `app_status: true` derruba a mensagem de
"App server is down", e o `full_list_url`/`lite_list_url` fazem o download funcionar.

## 8. Novo: baixar a texdb como .zip único (sem precisar subir arquivo por arquivo)
Como você já publicou o `texdb.zip` inteiro na Release `texdb-v1`, adicionei suporte
no próprio app para baixar esse zip e descompactar sozinho, ao invés de precisar
listar cada arquivo individualmente.

**O que mudou no código (pasta `java/` deste zip):**
- `ArchiveData.java` — arquivo novo. Representa um "pacote" (zip) a ser baixado e extraído.
- `Utils.java` — ganhou o método `extractZip()`, que descompacta um zip com segurança.
- `UpdateService.java` — agora também lê uma chave `"archives"` (além de `"files"`) no
  `full_list.json`/`lite_list.json`, baixa o(s) zip(s) listados lá, descompacta na pasta
  certa, e marca como concluído (não baixa de novo nas próximas checagens, a não ser que
  você troque o zip e o tamanho no JSON).

**Onde colocar esses arquivos no projeto:**
- `ArchiveData.java` → `app/src/main/java/ro/alynsampmobile/launcher/utils/ArchiveData.java` (novo)
- `Utils.java` → substitui o existente em `.../utils/Utils.java`
- `UpdateService.java` → substitui o existente em `.../launcher/UpdateService.java`

**O `full_list.json`/`lite_list.json` já vêm atualizados** com a entrada do seu
`texdb.zip` real:
```json
"archives": [
  {
    "name": "texdb",
    "path": "texdb",
    "size": 314572800,
    "url": "https://github.com/east9-777/ATT-APK-NATIVO/releases/download/texdb-v1/texdb.zip"
  }
]
```
- `path: "texdb"` → o zip é extraído dentro de `files/texdb/`, recriando as pastas
  `gta3`, `gta_int`, `menu`, `mobile`, `player`, `samp`, `txd` e os `.img` que aparecem
  no seu gerenciador de arquivos.
- `size` → coloquei um valor aproximado (300 MB em bytes). Não precisa ser o tamanho
  exato do arquivo — só precisa ser o **mesmo número** toda vez que você não quiser
  forçar o app a baixar de novo. Se um dia você atualizar o `texdb.zip`, troque esse
  número (qualquer valor diferente do anterior já força novo download).

## 7. Assinatura (problema 1, pendente)
Isso é independente do resto — quando quiser resolver de verdade (não só a chave de
teste), me chama que a gente monta o keystore + GitHub Actions, do mesmo jeito que
fizemos com o EAS Build no PRF app.

**Importante:** teste isso num APK de debug antes de distribuir. É código novo, então
vale rodar uma vez e conferir no Logcat/pasta de arquivos se `files/texdb/` realmente
apareceu com as pastas certas depois do update.

