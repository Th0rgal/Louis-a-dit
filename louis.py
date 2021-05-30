from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype('./src/louis_sans_ms.ttf', 42)

def create_image(text):
    img = Image.open("./src/base.jpg")
    drawable = ImageDraw.Draw(img)

    lines = []
    line = ""
    for word in text.split():
        (width, baseline), (offset_x, offset_y) = font.font.getsize(line + word + " ")
        if width > 414:
            (prev_width, prev_baseline), (offset_x, offset_y) = font.font.getsize(line)
            lines.append((line, prev_baseline))
            line = word + " "
        else:
            line += word + " "
    (prev_width, prev_baseline), (offset_x, offset_y) = font.font.getsize(line)
    lines.append((line, prev_baseline))

    x, y = 40, 40
    for line, h in lines:
        drawable.text((x, y), line, fill =(0, 0, 0), font=font)
        y += h
    img.save("latest.jpg")

import discord
from config import TomlConfig

config = TomlConfig("config.toml", "config.template.toml")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('louis a dit '):
        
        txt = message.content[12:]
        create_image(txt)
        await message.channel.send(file=discord.File("./src/latest.jpg"))


client.run(config.token)
