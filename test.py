# importing Image class from PIL package
from PIL import Image
import time

# creating a object
#im = Image.open(r"C:\Users\Eric\Desktop\Graphics\home.png")
#im = Image.open(r"/mnt/c/Users/Eric/Desktop/Graphics/home.png")

img = Image.new('RGB', (500, 500))
pixels = img.load()
for i in range(100,200):
    pixels[i,i] = (255,0,0)
 
img.show()

time.sleep(2)

for i in range(100,200):
    pixels[i+50,i] = (0,0,255)
 
img.show()
img.save("test2.png")
