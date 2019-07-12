from PIL import Image, ImageFont, ImageDraw
import json

with open('kaiku.json', 'r') as file:
    courses = json.load(file)

for course in courses:
    img = Image.new('RGB', (64, 64), color='#171f28')
    ide = course["id"]
    code = course["instances"][-1]["code"]
    grade = str(course["instances"][-1]["grade"])
    codefnt = ImageFont.truetype('/Library/Fonts/OpenSans-Regular.ttf', 10)
    gradefnt = ImageFont.truetype('/Library/Fonts/Righteous-Regular.ttf', 20)

    d = ImageDraw.Draw(img)
    w1, h1 = d.textsize(grade, font=gradefnt)
    w2, h2 = d.textsize(code, font=codefnt)

    d.text(((64-w1)/2, 10), grade, font=gradefnt, fill=(255, 255, 255))
    d.text(((64-w2)/2, 40), code, font=codefnt, fill=(255, 255, 255))

    img.save('site/thumbnails/' + ide + ".jpg", "JPEG")


