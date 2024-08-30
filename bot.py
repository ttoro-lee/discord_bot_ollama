import os
import discord
from dotenv import load_dotenv
import ollama
import Ex

# 환경 변수를 .env 파일에서 로딩
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
  print(f'We have logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!도움') or message.content.startswith('!help'):
      await message.channel.send(
"""
루미 ver 1.0.1

안녕하세요! 루미아 섬의 루미입니다.

=================명령어=======================================

- !도움 / !help : 명령어 list를 출력합니다.
- !전적 [유저명] : dak.gg 에서 전적을 검색합니다.
- !루미 [질문] : Llama-3.1-8B-Instruct-Q8 기반의 AI가 답변합니다.

==============================================================

제작 : 곰공X (dnsanswkd@naver.com)

""")

    elif message.content.startswith('!전적'):
      try:
        user_name = message.content.split()[1]
        search_url = f"https://dak.gg/er/players/{user_name}"
        await message.channel.send(f"{user_name} 의 전적 : {search_url}")
      except IndexError as e:
        await message.channel.send("!전적 [유저이름] 으로 검색하세요.")
    elif message.content.startswith('!루미'):
      try:
        context = message.content.split("!루미 ")[1]
        response = ollama.chat(model='rumi-llama-3.1-8b', messages=[
          {
            'role': 'user',
            'content': message.content.split("!루미 ")[1],
          },
        ])
        # Send the response as a message
        try:
          await message.channel.send(response['message']['content'])
        except Exception as e:
          await message.channel.send("요청 시간이 오래 걸립니다.")
      except IndexError as e:
        await message.channel.send("!루미 [질문] 으로 요청하세요.")
      

# start the bot
client.run(TOKEN)