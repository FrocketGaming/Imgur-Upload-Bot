from src.client import MyClient

import pyimgur
import discord
import keyring

TOKEN = keyring.get_password("discord", "token")

intents = discord.Intents.all()
client = MyClient(command_prefix="!", intents=intents)

imgur_id = keyring.get_password("imgur", "id")
im = pyimgur.Imgur(imgur_id)

@client.event
async def on_message(message):
    """This bot allows users to upload images to Imgur by sending an image as an attachment to a Discord Channel.
    It creates a new Imgur post with the image, returning the link to the post. The link is also stored in a text
    file for future reference."""

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message has an attachment
    if message.attachments:
        for attachment in message.attachments:
            # Check if the attachment is an image
            if attachment.filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp")
            ):
                try:
                    img_url = attachment.url

                    # Determining the title of the image
                    if message.content:
                        title = message.content
                    else:
                        title = "Untitled"

                    uploaded_image = im.upload_image(url=img_url, title=title)
                    
                    await message.channel.send("Image uploaded to Imgur:")
                    await message.channel.send(uploaded_image.link)
                    
                    # Store the link of the url that was created
                    # TODO: Store the link in a database and include the image title
                    with open("links.txt", "a") as file:
                        file.write(f"{title} - {uploaded_image.link}\n")
                except ValueError as e:
                    await message.channel.send(f"An error occurred: {e}")
            else:
                await message.channel.send("The file attached is not an image.")

client.run(TOKEN)
