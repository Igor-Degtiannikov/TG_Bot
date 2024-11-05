from PIL import Image
import qrcode
from pyzbar.pyzbar import decode


qr = qrcode.QRCode(
    version = None,
    error_correction = qrcode.constants.ERROR_CORRECT_L,
    box_size = 10,
    border = 4,
)

qr.add_data('Hello, I am learning to decode a QR code')
qr.make(fit=True)

img = qr.make_image(fill_color = 'red', back_color = 'white')
img.save('my_qrcode.png')

def decode_qr_code(image_path):
    img = Image.open(image_path)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        print('Type', obj.type)
        print('Decoded data', obj.data.decode('utf-8'))

decode_qr_code('my_qrcode.png')