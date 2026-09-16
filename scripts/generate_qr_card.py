from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "qr"
URL = "https://quirozstudio.github.io/bodas.otazu/"


def font(size: int, serif: bool = False, italic: bool = False):
    fonts = Path("C:/Windows/Fonts")
    if serif:
        name = "timesi.ttf" if italic else "times.ttf"
    else:
        name = "arial.ttf"
    return ImageFont.truetype(str(fonts / name), size)


def centered(draw, text, y, selected_font, fill, tracking=0):
    if not tracking:
        box = draw.textbbox((0, 0), text, font=selected_font)
        draw.text(((900 - (box[2] - box[0])) / 2, y), text, font=selected_font, fill=fill)
        return
    widths = [draw.textlength(char, font=selected_font) for char in text]
    width = sum(widths) + tracking * (len(text) - 1)
    x = (900 - width) / 2
    for char, char_width in zip(text, widths):
        draw.text((x, y), char, font=selected_font, fill=fill)
        x += char_width + tracking


OUTPUT.mkdir(parents=True, exist_ok=True)
ivory = (246, 242, 234)
ink = (37, 35, 31)
gold = (172, 145, 96)
muted = (109, 103, 94)
wine = (60, 23, 32)

card = Image.new("RGB", (900, 1260), ivory)
draw = ImageDraw.Draw(card)

# Composición editorial asimétrica y un sello propio de la pareja.
draw.rounded_rectangle((34, 34, 866, 1226), radius=8, outline=wine, width=3)
draw.line((108, 101, 108, 1159), fill=gold, width=2)

# Fecha vertical: funciona como lomo de una pequeña edición impresa.
date_layer = Image.new("RGBA", (470, 42), (0, 0, 0, 0))
date_draw = ImageDraw.Draw(date_layer)
date_draw.text((0, 7), "12  ·  10  ·  2026", font=font(17), fill=wine)
date_layer = date_layer.rotate(90, expand=True)
card.paste(date_layer, (67, 384), date_layer)

# Sello A&J inspirado en una marca de lacre, sin invadir el código QR.
draw.ellipse((663, 92, 806, 235), fill=wine, outline=wine, width=2)
draw.ellipse((674, 103, 795, 224), outline=gold, width=2)
draw.text((696, 124), "A", font=font(54, serif=True), fill=ivory)
draw.text((750, 151), "&", font=font(28, serif=True, italic=True), fill=gold)
draw.text((756, 164), "J", font=font(44, serif=True), fill=ivory)

# Pequeña rama de vid dibujada a mano como firma del lugar.
vine = wine
draw.arc((568, 180, 824, 486), 112, 252, fill=vine, width=2)
for x, y, angle in [(724, 256, 20), (688, 310, -24), (670, 365, 18), (690, 418, -20)]:
    leaf = Image.new("RGBA", (54, 34), (0, 0, 0, 0))
    leaf_draw = ImageDraw.Draw(leaf)
    leaf_draw.ellipse((3, 5, 50, 28), outline=vine, width=2)
    leaf_draw.line((6, 17, 47, 17), fill=vine, width=1)
    leaf = leaf.rotate(angle, expand=True)
    card.paste(leaf, (x, y), leaf)

draw.text((153, 112), "UNA HISTORIA", font=font(16), fill=gold)
draw.text((151, 148), "que vuelve", font=font(55, serif=True, italic=True), fill=wine)
draw.text((151, 206), "cada vez que la miramos.", font=font(28, serif=True), fill=muted)
draw.line((153, 275, 374, 275), fill=gold, width=2)

draw.text((153, 323), "ESCANEA Y ENTRA", font=font(16), fill=gold)
draw.text((153, 355), "en nuestro día", font=font(42, serif=True), fill=wine)

qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=4)
qr.add_data(URL)
qr.make(fit=True)
qr_image = qr.make_image(fill_color=wine, back_color=ivory).convert("RGB")
qr_image.thumbnail((500, 500), Image.Resampling.NEAREST)
qr_x = 250
card.paste(qr_image, (qr_x, 464))

draw.text((250, 987), "Apunta con la cámara de tu móvil", font=font(19, serif=True, italic=True), fill=muted)
draw.line((250, 1032, 748, 1032), fill=gold, width=1)
draw.text((250, 1063), "BODEGAS OTAZU", font=font(17), fill=wine)
draw.text((250, 1101), "Otazu · Navarra", font=font(24, serif=True), fill=muted)

# Firma final con carácter de pieza numerada.
draw.text((660, 1071), "A  &  J", font=font(30, serif=True), fill=wine)
draw.text((690, 1110), "2026", font=font(13), fill=gold)
draw.rounded_rectangle((220, 1150, 806, 1201), radius=25, fill=wine)
draw.text((251, 1169), "DISEÑO DIGITAL PARA GUARDAR UN RECUERDO", font=font(10), fill=ivory)
draw.text((714, 1169), "+ QUIROZ", font=font(10), fill=gold)

card_path = OUTPUT / "tarjeta-qr-invitados.png"
qr_path = OUTPUT / "qr-bodas-otazu.png"
card.save(card_path, quality=96, dpi=(300, 300))
qr_image.resize((1000, 1000), Image.Resampling.NEAREST).save(qr_path, quality=100)
print(card_path)
print(qr_path)
