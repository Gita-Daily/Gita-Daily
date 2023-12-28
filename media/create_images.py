import warnings
warnings.filterwarnings("ignore")

import os
import random
from PIL import Image, ImageDraw, ImageFont
import json

def split_sentence(sentence):
    words = sentence.split()
    sentences = []
    new_sentence = ""

    for word in words:
        if len(new_sentence) + len(word) <= 55:
            new_sentence += " " + word if new_sentence else word
        else:
            sentences.append(new_sentence)
            new_sentence = word

    if new_sentence:
        sentences.append(new_sentence)

    return "\n".join(sentences)

def overlay_text_on_random_image(shloka, translation, shloka_details, chapter_no, shloka_no):
    bg_text = "Bhagavad Gita"
    subscribe_text = "To receive Daily Bhagavad Gita shlokas, \nWhatsApp 'Hare Krishna' to +917022312895"

    image_files = []
    for root, dirs, files in os.walk("all-images-new"):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
                image_files.append(os.path.join(root, file))

    random_image_path = random.choice(image_files)
    img = Image.open(random_image_path)
    width, height = img.size

    margin_x = width * 0.05
    max_width = width - (2 * margin_x)
    max_height = height

    font_size = 100
    font = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', font_size)

    draw = ImageDraw.Draw(img)

    while True:
        translation_width, translation_height = draw.textsize(translation, font=font)
        if translation_width <= max_width and translation_height <= max_height:
            break
        font_size -= 1
        font = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', font_size)  

    shloka_width, shloka_height = draw.textsize(shloka, font=font)
    bg_text_width, bg_text_height = draw.textsize(bg_text, font=font)
    shloka_details_width, shloka_details_height = draw.textsize(shloka_details, font=font)
    subscribe_text_width, subscribe_text_height = draw.textsize(subscribe_text, font=font)

    total_height = translation_height + shloka_height + bg_text_height + shloka_details_height + subscribe_text_height
    # print('total height is ', total_height, 'and max height is ', max_height)

    # 15px margin between bhagavad gita and shloka details
    total_height += 15

    margin_y = (height - total_height) / 5

    bg_text_x = (width - bg_text_width) / 2
    bg_text_y = margin_y

    shloka_details_x = (width - shloka_details_width) / 2
    shloka_details_y = bg_text_y + bg_text_height + 15

    shloka_x = (width - shloka_width) / 2
    shloka_y = shloka_details_y + shloka_details_height + margin_y

    translation_x = (width - translation_width) / 2
    translation_y = shloka_y + shloka_height + margin_y

    subscribe_text_x = (width - subscribe_text_width) / 2
    subscribe_text_y = translation_y + translation_height + margin_y

    # add translucent rectangle behind every text
    padding = 5  

    bg_text_rectangle_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    bg_text_rectangle_draw = ImageDraw.Draw(bg_text_rectangle_img)
    bg_text_rectangle_draw.rounded_rectangle(
        [bg_text_x - padding, bg_text_y - padding,
        bg_text_x + bg_text_width + padding, bg_text_y + bg_text_height + padding],
        radius=10,
        fill=(0,0,0,128)
    )
    img = Image.alpha_composite(img.convert('RGBA'), bg_text_rectangle_img)
    draw = ImageDraw.Draw(img)

    shloka_details_rectangle_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    shloka_details_rectangle_draw = ImageDraw.Draw(shloka_details_rectangle_img)
    shloka_details_rectangle_draw.rounded_rectangle(
        [shloka_details_x - padding, shloka_details_y - padding,
        shloka_details_x + shloka_details_width + padding, shloka_details_y + shloka_details_height + padding],
        radius=10,
        fill=(0,0,0,128)
    )
    img = Image.alpha_composite(img.convert('RGBA'), shloka_details_rectangle_img)
    draw = ImageDraw.Draw(img)

    shloka_rectangle_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    shloka_rectangle_draw = ImageDraw.Draw(shloka_rectangle_img)
    shloka_rectangle_draw.rounded_rectangle(
        [shloka_x - padding, shloka_y - padding,
        shloka_x + shloka_width + padding, shloka_y + shloka_height + padding],
        radius=10,
        fill=(0,0,0,128)
    )
    img = Image.alpha_composite(img.convert('RGBA'), shloka_rectangle_img)
    draw = ImageDraw.Draw(img)

    translation_rectangle_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    translation_rectangle_draw = ImageDraw.Draw(translation_rectangle_img)
    translation_rectangle_draw.rounded_rectangle(
        [translation_x - padding, translation_y - padding, 
        translation_x + translation_width + padding, translation_y + translation_height + padding], 
        radius=10,  
        fill=(0,0,0,128)
    )
    img = Image.alpha_composite(img.convert('RGBA'), translation_rectangle_img)
    draw = ImageDraw.Draw(img)

    subscribe_text_rectangle_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    subscribe_text_rectangle_draw = ImageDraw.Draw(subscribe_text_rectangle_img)
    subscribe_text_rectangle_draw.rounded_rectangle(
        [subscribe_text_x - padding, subscribe_text_y - padding,
        subscribe_text_x + subscribe_text_width + padding, subscribe_text_y + subscribe_text_height + padding],
        radius=10,
        fill=(0,0,0,128)
    )
    img = Image.alpha_composite(img.convert('RGBA'), subscribe_text_rectangle_img)
    draw = ImageDraw.Draw(img)


    draw.text((bg_text_x, bg_text_y), bg_text, fill="white", font=font)
    draw.text((shloka_details_x, shloka_details_y), shloka_details, fill="white", font=font)
    draw.text((shloka_x, shloka_y), shloka, fill="white", font=font)
    draw.text((translation_x, translation_y), translation, fill="white", font=font)
    draw.text((subscribe_text_x, subscribe_text_y), subscribe_text, fill="white", font=font)

    # save the image
    os.makedirs(f"generated_images_new/{chapter_no}", exist_ok=True)

    img_rgb = img.convert("RGB")
    img_rgb.save(f"generated_images_new/{chapter_no}/{shloka_no}.jpg", "JPEG")
    print(f"Generated {chapter_no}/{shloka_no}.jpg")



all_chapters = [
  47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78,
]

total_chapters = len(all_chapters)

for chapter_no in range(1, total_chapters + 1):
    for shloka_no in range(1, all_chapters[chapter_no - 1] + 1):
        chapter_no = str(chapter_no)
        shloka_no = str(shloka_no)

        shloka_details = f'Chapter {chapter_no} Shloka {shloka_no}'

        with open(f'english_{chapter_no}/{shloka_no}.json', 'r') as json_file:
            data = json.load(json_file)

        shloka = data['shloka'][0]
        translation = split_sentence(data['translation'][0])

        overlay_text_on_random_image(shloka, translation, shloka_details, chapter_no, shloka_no)