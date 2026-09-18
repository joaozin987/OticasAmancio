import os
from PIL import Image

PASTA_IMG = "img"
LARGURA_MAX = 1600  # ajuste se quiser imagens maiores/menores
QUALIDADE = 75      # 0-100, 75-80 é um bom equilíbrio pra web

total_antes = 0
total_depois = 0

for nome_arquivo in os.listdir(PASTA_IMG):
    caminho = os.path.join(PASTA_IMG, nome_arquivo)
    if not os.path.isfile(caminho):
        continue
    if not nome_arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    tamanho_antes = os.path.getsize(caminho)
    total_antes += tamanho_antes

    try:
        img = Image.open(caminho)
        # Converte pra RGB (evita erro com PNGs com transparência ao salvar como JPEG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Redimensiona só se for maior que o limite, mantendo proporção
        if img.width > LARGURA_MAX:
            proporcao = LARGURA_MAX / img.width
            nova_altura = int(img.height * proporcao)
            img = img.resize((LARGURA_MAX, nova_altura), Image.LANCZOS)

        img.save(caminho, "JPEG", quality=QUALIDADE, optimize=True)

        tamanho_depois = os.path.getsize(caminho)
        total_depois += tamanho_depois
        print(f"{nome_arquivo}: {tamanho_antes/1024/1024:.1f}MB -> {tamanho_depois/1024/1024:.1f}MB")
    except Exception as e:
        print(f"ERRO em {nome_arquivo}: {e}")

print(f"\nTotal antes: {total_antes/1024/1024:.1f}MB")
print(f"Total depois: {total_depois/1024/1024:.1f}MB")