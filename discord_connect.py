import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp 

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN") 
DIFY_KEY = os.getenv("DIFY_API_KEY") 

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

async def get_chat_response(query):
    url = 'https://api.dify.ai/v1/workflows/run'
    headers = {
        'Authorization': f'Bearer {DIFY_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'inputs': {
            'start': query,
            'question': 'レッスンについて'
        },
        'response_mode': 'blocking',
        'user': 'user_identifier',
        'conversation_id': '',
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                json_response = await response.json()
                answer = json_response.get('data', {}).get('outputs', {}).get('text', 'No answer provided.')
                return answer
            else:
                return f'APIエラー: {response.status}, メッセージ: {await response.text()}'

@client.event
async def on_message(message):
    # ボット自身のメッセージには反応しない
    if message.author == client.user:
        return

    # 受け取ったメッセージに対してボットが応答する
    response = await get_chat_response(message.content)
    await message.channel.send(response)

client.run(TOKEN)
