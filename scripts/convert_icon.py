from PIL import Image

# 1. Load your PowerPoint PNG
img = Image.open('BOMO_Graphic.png') # Make sure your filename matches

# 2. Define standard icon sizes for Windows (16x16 up to 256x256)
# This keeps it crisp on the taskbar and the desktop
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# 3. Save as a true .ico file
img.save('BOMO_Icon.ico', sizes=icon_sizes)
print("BOMO_Icon.ico is ready for the bench!")