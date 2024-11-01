from PIL import Image, ImageDraw

# Define sizes and filenames
sizes = [(16, 16), (48, 48), (128, 128)]
filenames = ["icon16.png", "icon48.png", "icon128.png"]

for size, filename in zip(sizes, filenames):
    # Create a new image with a white background
    image = Image.new("RGB", size, color="lightblue")
    draw = ImageDraw.Draw(image)
    # Draw a simple placeholder text
    draw.text((size[0] // 4, size[1] // 4), "A", fill="black")
    # Save the image
    image.save(filename)

print("Icons created: icon16.png, icon48.png, icon128.png")
