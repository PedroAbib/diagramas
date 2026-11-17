# diagramas

Diagramas do meu fluxo de trabalho, em Excalidraw. O link abre o desenho direto no site, sem
precisar baixar nem importar arquivo.

| Diagrama | Abrir |
| --- | --- |
| Hub interno, três cenários | [Excalidraw](https://excalidraw.com/#url=https%3A%2F%2Fraw.githubusercontent.com%2FPedroAbib%2Fdiagramas%2Fmain%2Fhub-interno-cenarios.excalidraw) |

## Como um diagrama entra aqui

1. O arquivo `.excalidraw` fica na raiz, com nome `tema-assunto`, minúsculo e sem acento.
2. `python3 scripts/checar.py` precisa passar. Ele roda sozinho no commit e no push.
3. A linha entra na tabela acima, com o link no formato
   `https://excalidraw.com/#url=<endereço do arquivo>`.

## O que nunca entra

O repositório é público. Segredo, credencial, dado pessoal, nome de cliente, valor de contrato
e identificador de infraestrutura ficam de fora. Em diagrama, use papel em vez de nome de
pessoa: coordenação, campo, cliente, entrevistador.

Em dúvida, não publica.

## Editar

O link carrega a versão atual do arquivo, então a edição é livre. Para gravar de volta, use
Export no Excalidraw e substitua o arquivo, ou peça a leitura da cena aberta na aba.

## Link direto

O Excalidraw aceita `#url=<endereço>`, busca o arquivo na hora e monta a cena. Ao carregar, ele
limpa o endereço e volta para `excalidraw.com`, então guarde o link, e não o histórico da aba.
