
import discord
import requests
import os
from discord.ext import commands
# Discord bot token
TOKEN = 'nil'


ROBLOX_SECURITY_TOKEN = 'nil'

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(command_prefix='!', intents=intents)


def download_file(url, file_name, roblox_security_token):
    headers = {
        'Cookie': f'.ROBLOSECURITY={roblox_security_token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        os.rename(file_name, file_name + ".rbxm")
        return True
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return False

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):

    print(f'Message received from {message.author}: {message.content}')


    if message.author == bot.user:
        return

    try:
        asset_id = int(message.content)
    except ValueError:
        return


    url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"


    file_name = f"asset_{asset_id}.dat"
    success = download_file(url, file_name, ROBLOX_SECURITY_TOKEN)


    if success:
        with open(file_name + ".rbxm", 'rb') as f:
            await message.author.send(file=discord.File(f))


        os.remove(file_name + ".rbxm")


    await bot.process_commands(message)


bot.run(TOKEN)
