import discord

# 비속어 감지 기능을 분리한 함수
async def check_profanity(message: discord.Message):
    # 감지할 비속어 리스트. 여기에 계속 추가 하면 됨 비속어들 
    profanities = profanities = [
    # 짧은 형태
    "ㅅㅂ", "ㅆㅂ", "ㅈㄹ", "ㄲㅈ", "ㅈㄴ", "ㅈ같네", "ㅄ", "ㅂㅅ", "ㅁㅊ", "ㅂㅅ같은", "ㄷㅊ", "ㅗ", "ㄱㅅㄲ", "ㄳㄲ",
    
    # 단어 형태
    "시발", "씨발", "씨바", "씨빨", "씨파", "썅", "쌍놈", "쌍년", "미친놈", "미친년", "또라이", "개새끼", 
    "개자식", "개년", "개소리", "개같은", "개판", "개씹", "개같다", "개독", "걸레같은", "병신", "멍청이", 
    "멍충이", "한심한놈", "역겨운", "재수없는", "돌아이", "미친자식", "나쁜놈", "나쁜년", "천박한", 
    "더러운", "쓰레기같은", "잡놈", "잡년", "꼴값", "꼴보기싫은", "지랄"
    
    # 로마자/변형
    "tlqkf", "sibal", "ssibal", "shibal", "gae", "gaesekki", "byungsin", "wrkxsp", 
    
    # 문장 형태
    "꺼져", "닥쳐", "입 닥쳐", "죽어", "지랄하지마", "혀 깨물어", "얼굴 좀 봐", "더러워",
    "찌질하다", "더럽게", "고약한놈", "미친놈이야", "사람새끼냐",
]

    
    # 비속어가 포함된 경우 처리
    for profanity in profanities:
        if profanity in message.content:
            await message.channel.send(f'{message.author}님의 비속어 감지!')
            return True
    return False
