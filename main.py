import discord
import os
from discord.ext import commands
from discord import app_commands
from profanity_filter import check_profanity  # 비속어 감지 모듈 import
from dotenv import load_dotenv
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()




uri = (os.getenv("URI"))

client = MongoClient(uri)
db = client.user_messages
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

class Client(commands.Bot):
    async def on_ready(self):
        print(f'온라인 됨 {self.user}!')
        try:
            synced = await self.tree.sync()  # 슬래시 커맨드 동기화
            print(f"슬래시 커맨드 {len(synced)}개 동기화 완료!")
        except Exception as e:
            print(f"동기화 중 오류 발생: {e}")

    async def on_message(self, message):
        if message.author == self.user:  # 무한 반복 방지 코드.
            return 

        db.server_messages_log.insert_one(
            {
                "message": message.content,
                "author": message.author.id,
            }
        )
        await check_profanity(message)
intents = discord.Intents.all()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

#1. 도움말 코맨드 
#2. 티어 (본인 현재 티어 및 욕 횟수 보여주기)
#3. 티어 랭킹
#4. 특정 욕 순위 

@client.tree.command(name="티어리스트", description="모든 티어를 확인합니다!")
async def tierlist(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🏆 티어 리스트",
        description="각 티어의 조건과 달성 여부를 확인하세요!",
        color=0xFFD700,  # 골드 색상
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    embed.set_image(url="https://mblogthumb-phinf.pstatic.net/MjAyMjA2MjVfNjcg/MDAxNjU2MTUyMTk5NTE4.H-5iKkgvc3pUjoWHlaP1BHfVL4oa062eU371X0peVhcg.Wou7mfryOQZjeXn6FIU--6OWJUYCqzzeezLtmIH2-pgg.PNG.didcjddns/ranked-infographic-league-of-legends-season-12-for-Loc-2-of-5_KR.png?type=w800")
    embed.add_field(name="🔰 브론즈", value="50회 욕설 사용", inline=False)
    embed.add_field(name="🥈 실버", value="100회 욕설 사용", inline=False)
    embed.add_field(name="🥇 골드", value="200회 욕설 사용", inline=False)
    embed.add_field(name="💎 플래티넘", value="500회 욕설 사용", inline=False)
    embed.add_field(name="🔥 다이아몬드", value="1000회 욕설 사용", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="도움말", description="모든 명령어를 확인합니다!")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="명령어 리스트",
        description="다음과 같은 명령어가 존재합니다!",
        color=0xFFD700,  # 골드 색상
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    embed.add_field(name="티어리스트", value="모든 티어를 확인합니다!", inline=False)
    embed.add_field(name="현재티어", value="본인의 티어를 확인합니다!", inline=False)
    embed.add_field(name="티어랭킹", value="욕 티어 TOP5 랭킹을 보여줍니다!", inline=False)
    embed.add_field(name="도움말", value="모든 명령어를 확인합니다!", inline=False)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="현재티어", description="본인의 티어를 확인합니다!")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="현재 티어 :" + "(데이터베이스 티어 보여줘야함)",
        description="당신은 현재 상위 %입니다!",
        color=0xFFD700,  # 골드 색상
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    await interaction.response.send_message(embed=embed)

@client.tree.command(name="티어랭킹", description="욕 티어 TOP5 랭킹을 보여줍니다!")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="티어 랭킹",
        description="현재 순위는 다음과 같습니다!",
        color=0xFFD700,  # 골드 색상
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    embed.add_field(name="1등 (닉네임)", value="(티어)", inline=False)
    embed.add_field(name="2등 (닉네임)", value="(티어)", inline=False)
    embed.add_field(name="3등 (닉네임)", value="(티어)", inline=False)
    embed.add_field(name="4등 (닉네임)", value="(티어)", inline=False)
    embed.add_field(name="5등 (닉네임)", value="(티어)", inline=False)

    await interaction.response.send_message(embed=embed)





client.run(os.getenv("TOKEN")) #이러면 토큰 숨기면서 쓸수 있을 듯듯