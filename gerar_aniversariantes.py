from pathlib import Path
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def localizar_pastas():
    if getattr(sys, "frozen", False):
        pasta_base = Path(sys.executable).resolve().parent
        pasta_projeto = pasta_base.parent
    else:
        pasta_base = Path(__file__).resolve().parent
        pasta_projeto = pasta_base

    return pasta_base, pasta_projeto


def localizar_fonte(tamanho=38):
    caminhos = [
        "C:/Windows/Fonts/calibrib.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]

    for caminho in caminhos:
        if os.path.exists(caminho):
            return ImageFont.truetype(caminho, tamanho)

    return ImageFont.load_default()


def gerar_imagem(data_text, pasta_saida=None, arquivo_modelo=None):
    pasta_base, pasta_projeto = localizar_pastas()

    if pasta_saida is None:
        pasta_saida = pasta_projeto / "ImagensGeradas"
    if arquivo_modelo is None:
        arquivo_modelo = pasta_base / "modelo.png"

    pasta_saida.mkdir(parents=True, exist_ok=True)

    img = Image.open(arquivo_modelo)
    draw = ImageDraw.Draw(img)

    fonte = localizar_fonte(38)
    cor = "#13A8C8"

    x = 940
    y = 475
    draw.text((x, y), data_text, fill=cor, font=fonte)

    arquivo_saida = pasta_saida / f"Aniversariantes_{data_text.replace('/', '-')}.png"
    img.save(arquivo_saida)
    return str(arquivo_saida)


def main():
    nova_data = input("Digite a data (ex: 29/08): ").strip()
    arquivo_saida = gerar_imagem(nova_data)
    print(f"\n✅ Arquivo gerado: {arquivo_saida}")

    if os.name == "nt" and hasattr(os, "startfile"):
        os.startfile(arquivo_saida)


if __name__ == "__main__":
    main()