import discord
import os
from discord.ext import commands
from discord import app_commands
from profanity_filter import check_profanity 
from dotenv import load_dotenv
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from Data import db
import aiohttp

load_dotenv()

class Client(commands.Bot):
    async def on_ready(self):
        print(f'온라인 됨 {self.user}!')
        try:
            synced = await self.tree.sync()  
            print(f"슬래시 커맨드 {len(synced)}개 동기화 완료!")
        except Exception as e:
            print(f"동기화 중 오류 발생: {e}")

    async def on_message(self, message):
        if message.author == self.user:  
            return 
        
        check = await check_profanity(message)
        if check:
           await db.add_point(message)
        
intents = discord.Intents.all()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

@client.tree.command(name="봇상태", description="봇의 상태를 확인합니다!")
async def search(interaction: discord.Interaction, query: str):
    url = "https://koreanbots.dev/api/v2/search/bots"  # v2 버전 사용
    params = {
        "query": query,
        "page": 1
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                bots = data["data"]["data"]

                if bots:
                    # 검색 결과 메시지 생성
                    embed = discord.Embed(title=f"'{query}' 검색 결과", color=discord.Color.blue())
                    for bot in bots[:5]:  # 상위 5개만 표시
                        embed.add_field(
                            name=bot["name"],
                            value=f"**설명:** {bot['desc'][:100]}...\n**서버 수:** {bot['servers']}\n**투표 수:** {bot['votes']}",
                            inline=False
                        )
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message("검색 결과가 없습니다.")
            else:
                await interaction.response.send_message(f"API 호출 실패: {response.status}")

async def update_bot_servers(bot_id, server_count):
    url = f"https://koreanbots.dev/api/v2/bots/{1328634323766738944}/servers"
    headers = {
        "Authorization": "YOUR_BOT_API_KEY"
    }
    data = {
        "servers": server_count
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                print("서버 수 업데이트 성공!")
            else:
                print(f"서버 수 업데이트 실패: {response.status}")



@client.tree.command(name="티어리스트", description="모든 티어를 확인합니다!")
async def tierlist(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🏆 티어 리스트",
        description="각 티어의 조건과 달성 여부를 확인하세요!",
        color=0xc27a1b,  
    )
    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    embed.add_field(name="🔰 브론즈", value="50회 비속어 사용", inline=False)
    embed.add_field(name="🥈 실버", value="100회 비속어 사용", inline=False)
    embed.add_field(name="🥇 골드", value="200회 비속어 사용", inline=False)
    embed.add_field(name="💎 플래티넘", value="500회 비속어 사용", inline=False)
    embed.add_field(name="🔥 다이아몬드", value="1000회 비속어 사용", inline=False)
    embed.add_field(name="🏆 마스터", value="10000회 비속어 사용", inline=False)
    await interaction.response.send_message(embed=embed)

@client.tree.command(name="도움말", description="모든 명령어를 확인합니다!")
async def help(interaction: discord.Interaction):

    embed = discord.Embed(
        title="명령어 리스트",
        description="다음과 같은 명령어가 존재합니다!",
        color=0xc27a1b,  
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    embed.add_field(name="• /티어리스트", value="모든 티어를 확인합니다!", inline=False)
    embed.add_field(name="• /현재티어", value="본인의 티어를 확인합니다!", inline=False)
    embed.add_field(name="• /티어랭킹", value="비속어 사용 TOP5 랭킹을 보여줍니다!", inline=False)
    embed.add_field(name="• /도움말", value="모든 명령어를 확인합니다!", inline=False)
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="현재티어", description="본인의 티어를 확인합니다!")
async def present_tier(interaction: discord.Interaction):
    server_id = interaction.guild.id
    
    Tier = db.Get_rank(server_id,interaction.user.id)     
    point = db.Get_points(server_id,interaction.user.id)
    if Tier !=None:                             
        embed = discord.Embed(                 
            title="현재 티어 :" + Tier,
            description=f"\n욕 한 횟수: {point} 회",   
            color=0xc27a1b,  
        )
    else:
        embed = discord.Embed(
        title="욕쟁이를 찾을 수 없습니다" ,      
        description="욕설을 한 번도 사용하지 않으셨군요 :)",   
        color=0xc27a1b,  # 골드 색상
        )
    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    await interaction.response.send_message(embed=embed)

@client.tree.command(name="티어랭킹", description="비속어 사용 TOP5 랭킹을 보여줍니다!")
async def tier_ranking(interaction: discord.Interaction):
    server_id = interaction.guild.id
    ranking = db.get_server_ranking(server_id)

    if not ranking:
        await interaction.response.send_message("현재 서버에 랭킹 데이터가 없습니다!")
        return

    embed = discord.Embed(
        title="티어 랭킹",
        description="현재 순위는 다음과 같습니다!",
        color=0xc27a1b,  
    )

    embed.set_footer(text="요청자: {}".format(interaction.user.display_name))

    for i, user in enumerate(ranking):
        user_id = int(user["user_id"])
        points = user["Points"]
        Tier = db.Get_rank(server_id, user_id)

        member = interaction.guild.get_member(user_id)
        if member:
            username = member.display_name 
        else:
            try:
                fetched_user = await client.fetch_user(user_id)
                username = fetched_user.name
            except Exception:
                username = "알 수 없는 사용자"

        embed.add_field(
            name=f"{i + 1}등 {username}",
            value=f"티어: {Tier}, 횟수: {points}",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

client.run(os.getenv("TOKEN")) 

