import discord, random
from discord.ext import commands
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
TOKEN = "(아까 복사한 토큰 입력)"

# 로그인
@bot.event
async def on_ready():
    print(f"{bot.user.name} 로그인 성공")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('테스트'))
    
# 인사
@bot.command(name="안녕", help="인사말", aliases=["인사", "하이"])
async def hello(ctx):
  hi = random.randrange(1,4)
  if hi == 1:
    await ctx.channel.send("안녕하세요")
  elif hi == 2:
    await ctx.channel.send("안녕")
  elif hi == 3:
    await ctx.channel.send("네, 안녕하세요")

# 봇 작동
bot.run(TOKEN)