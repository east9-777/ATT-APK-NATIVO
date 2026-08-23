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

## 3. Troque SEU_USUARIO e SEU_REPO
Em `update.json`, `data_lists/full_list.json`, `data_lists/lite_list.json` e
`images/previews.json`, troque `SEU_USUARIO/SEU_REPO` pelo seu usuário e nome real do
repositório. O `full_list.json` e `lite_list.json` anexados já foram gerados a partir
dos seus 254 arquivos reais (114 MB) — só falta trocar essa parte da URL.

Dica: no app do GitHub (ou até pelo navegador do celular), dá pra usar "editar arquivo"
e um find & replace rápido em cada JSON.

## 4. Atualize o Utils.java
Já apliquei as mudanças no arquivo `Utils.java` anexado (pasta `utils/`). Ele agora
aponta pro `https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/`. Substitua
o arquivo original do projeto por esse, e troque lá dentro também o placeholder
`SEU_USUARIO`/`SEU_REPO`, e o link do Discord (`SEU_CONVITE`).

## 5. Sobre a texdb (pasta grande que faltou)
GitHub bloqueia arquivos individuais maiores que 100 MB num push normal (sem Git LFS).
Quando for subir a texdb:
- Se os arquivos dela forem menores que 100 MB cada, pode subir direto no mesmo repo,
  dentro de `game_files/texdb/`, e rodar `gerar_lista.py` de novo apontando pra pasta
  completa (com texdb) pra atualizar o `full_list.json`.
- Se algum arquivo passar de 100 MB, aí é melhor hospedar como asset de uma
  **GitHub Release** (aceita até 2 GB por arquivo) e ajustar a `url` desse arquivo
  específico no JSON manualmente para apontar pro link do Release.

## 6. Teste
Depois de subir tudo, abra `https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/update.json`
no navegador do celular. Se aparecer o JSON puro (não erro 404), o app já vai conseguir
ler. Nesse momento os 3 problemas somem: `app_status: true` derruba a mensagem de
"App server is down", e o `full_list_url`/`lite_list_url` fazem o download funcionar.

## 7. Assinatura (problema 1, pendente)
Isso é independente do resto — quando quiser resolver de verdade (não só a chave de
teste), me chama que a gente monta o keystore + GitHub Actions, do mesmo jeito que
fizemos com o EAS Build no PRF app.
