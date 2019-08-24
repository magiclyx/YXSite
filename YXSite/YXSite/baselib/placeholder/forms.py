from django import forms
from django.core.cache import cache
from PIL import Image, ImageDraw
from io import BytesIO


class ImageForm(forms.Form):
    """Form to validate requested placeholder image."""

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    @staticmethod
    def draw_watermark(image, width, height):

        draw = ImageDraw.Draw(image)
        width = image.size[0]
        height = image.size[1]

        # draw border
        draw.rectangle([0, 0, width-1, height-1], fill=None, outline='red', width=1)
        text = '{} X {}'.format(width, height)
        text_width, text_height = draw.textsize(text)

        # draw arc
        draw.arc([0, 0, width-1, height-1], 0, 360, fill='red')  # box, 起始度数， 结束度数

        # draw cross curve
        draw.line([0, 0, width-1, height-1], fill='red')
        draw.line([width-1, 0, 0, height-1], fill='red')

        # draw size text
        if text_width < width and text_height < height:
            text_top = (height - text_height) // 2
            text_left = (width - text_width) // 2
            draw.text((text_left, text_top), text, fill='red')

    def generate(self, image_format='PNG'):
        """Generate an image of the given type and return as raw bytes."""
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']

        key = '{}.{}.{}'.format(width, height, image_format)
        content = cache.get(key)
        if content is None:
            # 颜色值可以是 'red', 'white' 等， 也可以是 [255, 255, 255]
            image = Image.new('RGB', (width, height), color='white')

            # 绘制展位图的十字线
            self.draw_watermark(image, width, height)

            content = BytesIO()
            image.save(content, image_format)
            content.seek(0)
            cache.set(key, content, 60 * 60)

        return content

