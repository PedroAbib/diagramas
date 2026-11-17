#!/usr/bin/env python3
"""Barra conteúdo sensível nos diagramas antes de publicar.

O repositório é público. Este script extrai todo o texto dos arquivos
.excalidraw e recusa a publicação quando encontra o que não pode sair daqui:
segredo, credencial, dado pessoal, dinheiro e identificador de infraestrutura.

Uso:
    python3 scripts/checar.py            # confere todos os diagramas
    python3 scripts/checar.py --texto    # também imprime todo o texto lido

Saída 0 passa, saída 1 bloqueia.
"""

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# (nome do que é, expressão)
BLOQUEIOS = [
    ("valor de credencial", re.compile(
        r"(?<![A-Za-z0-9])(secret|token|api[_-]?key|password|senha|passwd|chave)\b\s*[:=]\s*\S{3,}", re.I)),
    ("token em uso", re.compile(r"\bbearer\s+[A-Za-z0-9._\-]{12,}", re.I)),
    ("chave do GitHub", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}")),
    ("chave de API", re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}")),
    ("chave privada", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
    ("credencial em endereço", re.compile(r"://[^/\s:@]+:[^/\s@]+@")),
    ("e-mail", re.compile(r"[\w.+\-]+@[\w\-]+\.[\w.]{2,}")),
    ("CPF", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("CNPJ", re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")),
    ("telefone", re.compile(r"\b\(?\d{2}\)?\s?9?\d{4}[\- ]\d{4}\b")),
    ("dinheiro", re.compile(r"R\$\s?\d")),
    ("endereço de IP", re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")),
    ("identificador único", re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)),
    ("hash longo", re.compile(r"\b[0-9a-f]{32}\b", re.I)),
    ("host de banco", re.compile(r"\b(database|db)\.[\w\-]+\.[a-z]{2,4}\b", re.I)),
    ("Supabase", re.compile(r"\bsupabase\.co\b", re.I)),
    ("bucket público", re.compile(r"\br2\.dev\b", re.I)),
]

AVISOS = [
    ("imagem embutida", None),  # tratado à parte, pelo campo files
    ("endereço completo", re.compile(r"https?://\S+", re.I)),
]


def mascarar(trecho):
    trecho = trecho.strip().replace("\n", " ")
    if len(trecho) <= 3:
        return "*" * len(trecho)
    return trecho[:2] + "…" + str(len(trecho)) + " caracteres"


def textos_do_arquivo(caminho):
    """Todo texto visível, inclusive o que está dentro de formas."""
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    achados = []
    for i, elemento in enumerate(dados.get("elements", [])):
        if elemento.get("type") != "text":
            continue
        # `text` é o que aparece na tela. `originalText` repete o mesmo conteúdo e
        # faria cada achado ser contado duas vezes.
        valor = elemento.get("text") or elemento.get("originalText") or ""
        if valor.strip():
            achados.append((i, valor))
    return dados, achados


def conferir(caminho):
    problemas = []
    avisos = []

    try:
        dados, textos = textos_do_arquivo(caminho)
    except Exception as erro:
        problemas.append(f"{caminho.name}: não consegui ler o arquivo ({erro})")
        return problemas, avisos

    for indice, valor in textos:
        for nome, padrao in BLOQUEIOS:
            achado = padrao.search(valor)
            if achado:
                problemas.append(
                    f"{caminho.name} · elemento {indice} · {nome} · “{mascarar(achado.group(0))}”")
        for nome, padrao in AVISOS:
            if padrao is None:
                continue
            achado = padrao.search(valor)
            if achado:
                avisos.append(
                    f"{caminho.name} · elemento {indice} · {nome} · “{mascarar(achado.group(0))}”")

    if dados.get("files"):
        problemas.append(f"{caminho.name}: tem imagem embutida, que pode carregar dado junto")

    if "--texto" in sys.argv:
        for _, valor in textos:
            print(f"    | {valor}")

    return problemas, avisos


def principal():
    diagramas = sorted(RAIZ.glob("*.excalidraw"))
    if not diagramas:
        print("Nenhum .excalidraw na raiz.")
        return 0

    problemas = []
    avisos = []
    for caminho in diagramas:
        p, a = conferir(caminho)
        problemas += p
        avisos += a

    if avisos:
        print(f"{len(avisos)} aviso(s), que não bloqueiam:")
        for aviso in avisos:
            print(f"  ~ {aviso}")
        print()

    if problemas:
        print(f"BLOQUEADO. {len(problemas)} achado(s) que não podem sair daqui:")
        for problema in problemas:
            print(f"  x {problema}")
        print("\nTire o conteúdo acima e rode de novo.")
        return 1

    print(f"Limpo. {len(diagramas)} diagrama(s) conferido(s).")
    return 0


if __name__ == "__main__":
    sys.exit(principal())
