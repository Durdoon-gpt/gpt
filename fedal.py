import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Définir le chemin vers Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Dictionnaire des questions et réponses
questions_and_answers = {
    "combien font 5 + 2 ?": "7",
    "quelle est la capitale de la France ?": "Paris",
    # Ajoutez d'autres questions et réponses ici
}


@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user.name}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == 1108850921171058688:
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    image_path = f"images/{attachment.filename}"
                    await attachment.save(image_path)
                    print("Image enregistrée :", image_path)

                    image = Image.open(image_path)

                    try:
                        question = pytesseract.image_to_string(image)
                        print("Question :", question)

                        response = questions_and_answers.get(question, "Je ne connais pas la réponse.")
                        print("Réponse :", response)

                        await message.channel.send(response)

                        # Envoyer le texte de la photo et la réponse en messages privés à l'utilisateur
                        user = message.author
                        dm_channel = await user.create_dm()

                        await dm_channel.send(f"Question : {question}")
                        await dm_channel.send(f"Réponse : {response}")

                    except Exception as e:
                        print("Erreur lors de l'extraction du texte :", e)

                    # Supprimer l'image après avoir donné le texte
                    os.remove(image_path)

                    # Supprimer le message contenant l'image
                    await message.delete()

                    break

    await bot.process_commands(message)


bot.run('MTEwODgxODU5MzcwNzIwMDY3NQ.G0GS0U.5juE3KuvfxD2VuQtBeBG_H7b3fJND-7acuKMak')
