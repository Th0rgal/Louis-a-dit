from PIL import Image, ImageDraw, ImageFont


def optimize_text(user_width, user_height, text):
    font_size = 21

    lines = []
    final_height = 0
    while final_height < user_height:
        final_height = 0
        font_size += 1
        font = ImageFont.truetype('./src/louis_sans_ms.ttf', font_size)
        previous_lines = lines
        lines = []
        line = ""
        for word in text.split():
            (width, baseline), (offset_x, offset_y) = font.font.getsize(line + word + " ")
            if width > user_width:

                if not line:
                    return ImageFont.truetype('./src/louis_sans_ms.ttf', font_size-1), previous_lines

                (prev_width, prev_baseline), (offset_x, offset_y) = font.font.getsize(line)
                lines.append((line, prev_baseline))
                line = word + " "
                final_height += prev_baseline
            else:
                line += word + " "
        (prev_width, prev_baseline), (offset_x, offset_y) = font.font.getsize(line)
        final_height += prev_baseline
        lines.append((line, prev_baseline))

    return ImageFont.truetype('./src/louis_sans_ms.ttf', font_size-1), previous_lines

def create_image(text, user):
    image_file = user["image"]
    img = Image.open(f"./src/{image_file}")
    drawable = ImageDraw.Draw(img)

    font, lines = optimize_text(user["width"], user["height"], text)
    x, y = user["x"], user["y"]
    for line, h in lines:
        drawable.text((x, y), line, fill =(0, 0, 0), font=font)
        y += h
    img.save("~output.jpg")

import re
import discord
from config import TomlConfig

config = TomlConfig("config.toml", "config.template.toml")
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content == "":
        return

    for username in config.users:
        user = config.users[username]
        if message.clean_content.lower().startswith(user["prefix"]):
            await message.delete()
            await send_message(message.channel,  message.clean_content[len(user["prefix"]):], message.attachments, user)
            return
    
        if user["id"] == message.author.id:
            await message.delete()
            await send_message(message.channel, message.clean_content, message.attachments, user)

async def send_message(channel, content, attachments, user):
        urls = re.findall('https?://[^\s]+', content)
        for attachment in attachments:
            urls.append(attachment.url)
        create_image(content, user)
        await channel.send(file=discord.File("~output.jpg"))
        if urls:
            embedVar = discord.Embed(title="Ressources:", color=0x336EFF)
            for i, url in enumerate(urls):
                embedVar.add_field(name=url, value="\u200b", inline=False)
            await channel.send(embed=embedVar)

client.run(config.token, bot=config.bot)
