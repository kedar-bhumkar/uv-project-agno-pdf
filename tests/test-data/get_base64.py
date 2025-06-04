import base64

def get_base64_encoding():
    with open('tests/test-data/test_image.png', 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        print("Base64 encoded string:")
        print(encoded_string)

if __name__ == "__main__":
    get_base64_encoding() 