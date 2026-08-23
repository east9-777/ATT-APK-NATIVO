# O que mudou nessa versão

Removi a tela de escolha LITE/FULL e a checagem que causava o "App server is down".
Agora o fluxo é: abre o app → baixa **um único zip** com todos os dados → extrai
sozinho na pasta certa → pronto.

## Por que dava o erro mesmo depois de tudo configurado

O `Utils.appStatus()` fazia uma **segunda chamada de rede**, separada da que já
carregava o `update.json` — e travava o app com aquela mensagem toda vez que essa
chamada extra falhasse, mesmo que o resto estivesse 100% funcionando. Removi essa
chamada de dentro do `SplashActivity.java`. Também tirei a tela LITE/FULL, que só
tinha textos fixos ("900 MB"/"2.3 GB") sem relação com o tamanho real de nada.

## Arquivos alterados (pasta `java/`)

- `SplashActivity.java` → substitui o existente em
  `app/src/main/java/ro/alynsampmobile/launcher/SplashActivity.java`
- `Utils.java`, `UpdateService.java`, `ArchiveData.java` → mesmos de antes (ver
  histórico da conversa), sem mudança nesta etapa.

## Novo esquema de dados: um zip só

Antes: lista de 254+ arquivos individuais, um por um. Agora: **um único
`gamedata.zip`** com a pasta `files` inteira dentro (tudo que estava em
`DATA/ro.alynsampmobile.launcher/files`, incluindo a `texdb`).

### Passo a passo

1. No seu computador/celular, junte tudo que estava em
   `DATA/ro.alynsampmobile.launcher/files/` (data, audio, anim, models, SAMP,
   fonts, **texdb** etc.) dentro de um único `.zip`, com essas pastas soltas na
   raiz do zip (não dentro de mais uma pasta "files/" — o `data/` já deve
   aparecer direto ao abrir o zip).
2. Confira o tamanho — com a texdb isso deve ficar por volta de 400-450 MB,
   bem abaixo do limite de 2 GB por arquivo do GitHub Release.
3. Crie (ou reaproveite) uma Release no GitHub, ex: tag `gamedata-v1`, e suba
   esse `gamedata.zip` como anexo (mesmo processo que você já fez com a texdb).
4. Copie o link do asset, algo como:
   ```
   https://github.com/SEU_USUARIO/SEU_REPO/releases/download/gamedata-v1/gamedata.zip
   ```
5. Abra `data_lists/full_list.json` e `data_lists/lite_list.json` (já vêm
   prontos aqui, com a mesma estrutura) e troque:
   - `url` → o link real do seu asset
   - `size` → o tamanho real do zip em **bytes** (não MB). No Android, ao tocar
     no arquivo no gerenciador de arquivos costuma mostrar o tamanho exato; ou
     multiplique o MB mostrado no GitHub por 1.048.576 pra converter pra bytes.
6. Suba `update.json`, `full_list.json` e `lite_list.json` pro seu repositório,
   nos mesmos caminhos de antes (veja abaixo). Já deixei todos os arquivos deste
   pacote com `east9-777/ATT-APK-NATIVO` preenchido — só falta a `url` e o `size`
   corretos do `gamedata.zip` no passo 5 acima.

Repare que **não precisa mais subir os 254 arquivos individuais** no repositório
— isso simplifica bastante, já que agora é tudo dentro do zip único.

## Estrutura do repositório (atualizada, mais simples)

```
/update.json
/servers.json
/banned.json
/faq.json
/changelog.txt
/images/previews.json
/data_lists/full_list.json
/data_lists/lite_list.json
/data_lists/samp_list.json   <- continua vazio, reservado pro futuro
```

Não existe mais pasta `game_files/` — os dados do jogo agora vivem só dentro do
zip anexado na Release.

## Teste

1. Substitua `SplashActivity.java` no projeto (e os outros 3 arquivos já
   ajustados antes, se ainda não tiver feito).
2. Confira se a `url` e o `size` do `gamedata.zip` em `full_list.json`/
   `lite_list.json` estão certos (usuário e repo já vêm preenchidos).
3. Suba tudo pro repo e gere um APK de debug.
4. Abra o app: ele deve pular direto pra "CHECKING FOR UPDATES" e, se tudo
   estiver certo, baixar o `gamedata.zip` e extrair sem mostrar mais aquela
   tela de erro. Acompanhe pelo Logcat se quiser ver o progresso
   (`UpdateService`, tag "Baixando archive" / "Archive extraido com sucesso").

Se aparecer algum outro erro nessa etapa, me manda o print/log que eu já vejo o
que é.

## Pendente: Assinatura (problema 1)
Continua de fora dessa etapa — quando quiser resolver de verdade, me chama que
a gente monta o keystore + GitHub Actions, do mesmo jeito que fizemos com o EAS
Build no PRF app.
