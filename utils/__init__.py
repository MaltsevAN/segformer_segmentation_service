import random
import io
def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def img2bytes(image):
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return byte_im