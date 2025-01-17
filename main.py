import discord
import os
from discord.ext import commands
from discord import app_commands
from profanity_filter import check_profanity  # 비속어 감지 모듈 import
from dotenv import load_dotenv
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Data import db

load_dotenv()

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
        
        check = await check_profanity(message)
        if check:
            db.add_point(message)
        
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
        color=0x580068,  # 골드 색상
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
        color=0x580068,  # 골드 색상
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    embed.add_field(name="• /티어리스트", value="모든 티어를 확인합니다!", inline=False)
    embed.add_field(name="• /현재티어", value="본인의 티어를 확인합니다!", inline=False)
    embed.add_field(name="• /티어랭킹", value="비속어 사용 TOP5 랭킹을 보여줍니다!", inline=False)
    embed.add_field(name="• /도움말", value="모든 명령어를 확인합니다!", inline=False)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="현재티어", description="본인의 티어를 확인합니다!")
async def present_tier(interaction: discord.Interaction):
    Tier = db.Get_rank(interaction.user.id)     #Get_rank에서 유저 id로 Tier가지고옴옴
    point = db.Get_points(interaction.user.id)
    if Tier !=None:                             #return값으로 유저가 있는지 없는 지 확인
        embed = discord.Embed(                  #있으면 티어 보여주고 없으면 else로로
            title="현재 티어 :" + Tier,
            description=f"\n욕 한 횟수: {point} 회",   #상위 몇 퍼센트 인지 어케 구하는지 생각할 필요 
            color=0x580068,  # 골드 색상
        )
    else:
        embed = discord.Embed(
        title="욕쟁이를 찾을 수 없습니다" ,         #글 전부 다 임시임 그냥 생각나는대로 적은거라라
        description="욕설을 한 번도 사용하지 않으셨군요 :)",   
        color=0x580068,  # 골드 색상
        )
    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    await interaction.response.send_message(embed=embed)

@client.tree.command(name="티어랭킹", description="비속어 사용 TOP5 랭킹을 보여줍니다!")
async def tier_ranking(interaction: discord.Interaction):
    server_id = interaction.guild.id
    ranking = db.get_server_ranking(server_id)
    Tier = db.Get_rank(interaction.user.id)

    if not ranking:
        await interaction.response.send_message("현재 서버에 랭킹 데이터가 없습니다!")
        return

    embed = discord.Embed(
        title="티어 랭킹",
        description="현재 순위는 다음과 같습니다!",
        color=0x580068,  # 골드 색상
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    for i, user in enumerate(ranking):
        user_id = int(user["user_id"])
        points = user["Points"]
        tier = user["Tier"]

        # 사용자 닉네임 가져오기
        member = interaction.guild.get_member(user_id)
        if member:
            username = member.display_name  # 서버 내 닉네임
        else:
            try:
                # 서버 멤버가 아니면 글로벌 닉네임 가져오기
                fetched_user = await client.fetch_user(user_id)
                username = fetched_user.name
            except Exception:
                username = "알 수 없는 사용자"

        embed.add_field(
            name=f"{i + 1}등 {username}",
            value=f"티어: {Tier}, 점수: {points}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)





client.run(os.getenv("TOKEN")) #이러면 토큰 숨기면서 쓸수 있을 듯듯