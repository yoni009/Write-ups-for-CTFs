from PIL import Image

img = Image.open("primary_extracted.jpg").convert("RGB")
pixels = img.load()

# Let's check the bottom or top rows where authors often hide text/flags
width, height = img.size
print(f"Image dimensions: {width}x{height}")