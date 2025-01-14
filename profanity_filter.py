import discord

# 비속어 감지 기능을 분리한 함수
async def check_profanity(message: discord.Message):
    # 감지할 비속어 리스트. 여기에 계속 추가 하면 됨 비속어들 
    profanities = ['ㄲㅈ', 'ㅅㅂ', '시발', '병신', 'ㅈ같네', 'tlqkf', 'qudtls', "꺼져", "ㅄ"] 
    
    # 비속어가 포함된 경우 처리
    for profanity in profanities:
        if message.content.startswith(profanity):
            await message.channel.send(f'{message.author}님의 비속어 감지!')
            break
