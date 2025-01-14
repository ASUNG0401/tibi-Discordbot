import discord
from discord.ext import commands
from discord import app_commands
from profanity_filter import check_profanity  # 비속어 감지 모듈 import

class Client(commands.Bot):
    async def on_ready(self):
        print(f'온라인 됨 {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return 
        #만약 메세지의 내용이 ('ㄲㅈ')로 시작한다면, 그 채널에 메세지 전송 sout같은 느낌 
        await check_profanity(message)

    # async def on_reaction_add(self, reaction, user):
    #     await reaction.message.channel.send('반응함 :)')  

    

intents = discord.Intents.all()
intents.message_content = True
client = Client(command_prefix="!", intents = intents) 

@client.tree.command(name="test1", description="test2")
async def test3(interaction: discord.Interaction):
    embed = discord.Embed(title="test4", color=0x00ff00)
    embed.add_field(name="test5", value="test6", inline=False)
    await interaction.response.send_message(embed=embed)

#슬래시 코맨드 작성법 ex) !음악 !스킵 (슬래시 코맨드란 !해서 입력하는 코맨드 명령어)
@client.tree.command(name = "hello", description="say hello")  #무슨 커맨드인지 이거로 예시를 들자면 !hello 하고 밑에 설명에 무슨 커맨드인지 description
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("hi there!") #

client.run('')