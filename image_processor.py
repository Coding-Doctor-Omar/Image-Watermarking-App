from PIL import Image, ImageDraw, ImageFont

WATERMARK_PADDING = 5

class ImageProcessor:
    def __init__(self, image):
        self.processed_img = image


    def add_watermark(self, image, text, font_type, color, font_size, opacity, rotation, position):
        if text == "":
            return None

        original_image = image.convert("RGBA")

        watermark_layer = Image.new("RGBA", original_image.size, (255, 255, 255, 0))

        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:], 16)
        a = int(opacity)
        color = (r, g, b, a)
        font_size = (font_size / 100) * self.processed_img.height

        watermark = ImageDraw.Draw(watermark_layer)
        font = ImageFont.truetype(font_type, font_size)
        watermark_textbox = watermark.textbbox((0, 0), text, font=font)
        watermark_width = watermark_textbox[2] - watermark_textbox[0]
        watermark_height = watermark_textbox[3] - watermark_textbox[1]

        positions = {
            "Center": (watermark_layer.width // 2 - watermark_width // 2, watermark_layer.height // 2 - watermark_height // 2),
            "Top Left": (WATERMARK_PADDING, WATERMARK_PADDING),
            "Top": (watermark_layer.width // 2 - watermark_width // 2, WATERMARK_PADDING),
            "Top Right": (watermark_layer.width - watermark_width - WATERMARK_PADDING, WATERMARK_PADDING),
            "Left": (WATERMARK_PADDING, watermark_layer.height // 2 - watermark_height // 2),
            "Right": (watermark_layer.width - watermark_width - WATERMARK_PADDING, watermark_layer.height // 2 - watermark_height // 2),
            "Bottom Left": (WATERMARK_PADDING + 5, watermark_layer.height - watermark_height - WATERMARK_PADDING - 5),
            "Bottom": (watermark_layer.width // 2 - watermark_width // 2, watermark_layer.height - watermark_height - WATERMARK_PADDING),
            "Bottom Right": (watermark_layer.width - watermark_width - WATERMARK_PADDING - 5, watermark_layer.height - watermark_height - WATERMARK_PADDING - 5),
        }

        watermark_position = positions[position]
        watermark_color = color

        center_point = (int(watermark_position[0]) + watermark_width // 2, int(watermark_position[1]) + watermark_height // 2)


        watermark.text(watermark_position, text=text, font=font, fill=watermark_color)

        watermark_layer = watermark_layer.rotate(rotation, center=center_point)

        self.processed_img = Image.alpha_composite(original_image, watermark_layer)

    def save_final_image(self, path):
        self.processed_img.convert("RGB").save(path)