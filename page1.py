from PIL import Image, ImageDraw, ImageFont

# Load images
logo_path = 'path_to_logo.png'
button1_path = 'path_to_button1.png'
button2_path = 'path_to_button2.png'
button3_path = 'path_to_button3.png'

# Create a new white image
width, height = 400, 500
image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

# Define sections
section_height = height // 3

# Section 1: Logo
logo = Image.open(logo_path)
logo = logo.resize((width, section_height), Image.ANTIALIAS)
image.paste(logo, (0, 0))

# Section 2: Buttons
button1 = Image.open(button1_path)
button2 = Image.open(button2_path)
button3 = Image.open(button3_path)

# Assuming buttons are the same size and fit horizontally
button_width = width // 3
button_height = section_height

button1 = button1.resize((button_width, button_height), Image.ANTIALIAS)
button2 = button2.resize((button_width, button_height), Image.ANTIALIAS)
button3 = button3.resize((button_width, button_height), Image.ANTIALIAS)

image.paste(button1, (0, section_height))
image.paste(button2, (button_width, section_height))
image.paste(button3, (2 * button_width, section_height))

# Section 3: Text Label
label_x = 20
label_y = 2 * section_height + 10
label_width = width - 40
label_height = section_height - 20
label_rect = (label_x, label_y, label_x + label_width, label_y + label_height)

# Draw rounded rectangle
radius = 20
draw.rounded_rectangle(label_rect, radius, fill="gray")

# Add text to label
font = ImageFont.load_default()
text = "Your Text Here"
text_width, text_height = draw.textsize(text, font=font)
text_x = label_x + (label_width - text_width) // 2
text_y = label_y + (label_height - text_height) // 2
draw.text((text_x, text_y), text, fill="black", font=font)

# Save the result
image.save('result_image.png')
