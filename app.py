from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import os

from gerar_aniversariantes import gerar_imagem

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "ImagensGeradas"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/gerar")
def gerar():
    payload = request.get_json(silent=True) or {}
    data_text = (payload.get("data") or request.form.get("data") or "").strip()

    if not data_text:
        return jsonify({"error": "Informe uma data."}), 400

    arquivo_saida = gerar_imagem(data_text, pasta_saida=OUTPUT_DIR)
    nome_arquivo = Path(arquivo_saida).name
    return jsonify({
        "arquivo": nome_arquivo,
        "caminho": f"/arquivos/{nome_arquivo}",
        "success": True,
    })


@app.get("/arquivos/<nome_arquivo>")
def servir_arquivo(nome_arquivo):
    return send_from_directory(OUTPUT_DIR, nome_arquivo, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=False)
