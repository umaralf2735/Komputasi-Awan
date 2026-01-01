from PIL import Image, ImageDraw

def create_test_image():
    img = Image.new('RGB', (1000, 1000), color = 'red')
    d = ImageDraw.Draw(img)
    d.text((10,10), "Hello World", fill=(255,255,0))
    img.save('test_image.jpg')
    print("test_image.jpg created")

if __name__ == "__main__":
    create_test_image()
