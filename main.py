import discord
import os
import pymysql
from discord.ext import commands
from discord import app_commands
from profanity_filter import check_profanity  # 비속어 감지 모듈 import
from dotenv import load_dotenv
from dotenv import load_dotenv
from Data import Connection #Data.py에서 만든 class사용하기 위해해

load_dotenv()
Connection = Connection()

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
        #만약 메세지의 내용이 ('ㄲㅈ')로 시작한다면, 그 채널에 메세지 전송 sout같은 느낌 
        check = await check_profanity(message)

        if check :
            s


intents = discord.Intents.all()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)


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


client.run(os.getenv("TOKEN")) #이러면 토큰 숨기면서 쓸수 있을 듯듯