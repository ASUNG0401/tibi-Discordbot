import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f'온라인 됨 {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return 
        #만약 메세지의 내용이 ('ㄲㅈ')로 시작한다면, 그 채널에 메세지 전송 sout같은 느낌 
        if message.content.startswith('ㄲㅈ'): 
            await message.channel.send(f'{message.author}님의 비속어 감지!')
        if message.content.startswith('ㅅㅂ'):
            await message.channel.send(f'{message.author}님의 비속어 감지!')     
        if message.content.startswith('시발'):
            await message.channel.send(f'{message.author}님의 비속어 감지!')       
        if message.content.startswith('병신'):
            await message.channel.send(f'{message.author}님의 비속어 감지!')
        if message.content.startswith('ㅈ같네'):
            await message.channel.send(f'{message.author}님의 비속어 감지!')

    # async def on_reaction_add(self, reaction, user):
    #     await reaction.message.channel.send('반응함 :)')  

    

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents = intents) 

#슬래시 코맨드 작성법 ex) !음악 !스킵 (슬래시 코맨드란 !해서 입력하는 코맨드 명령어)
@client.tree.command(name = "hello", description="say hello")  #무슨 커맨드인지 이거로 예시를 들자면 !hello 하고 밑에 설명에 무슨 커맨드인지 description
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("hi there!") #
    
client.run('')