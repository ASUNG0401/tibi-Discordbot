# 디스코드 봇: 비속어 감지 티비봇

## 개요
이 디스코드 봇은 부적절한 언어 사용을 감지하고, 누적 점수를 기반으로 티어를 올리는 게임화된 경험을 제공합니다. 사용자는 자신의 순위를 확인하고 그룹 내 다른 사람들과 비교할 수 있어 재미있고 경쟁적인 환경을 조성합니다. Python, Discord API, MongoDB를 사용하여 구축된 이 봇은 안정적이고 확장 가능하며 커뮤니티의 독특한 참여 방식을 지원합니다.

---

## 주요 기능

### 1. **언어 모니터링**
- 부적절한 언어 사용을 감지합니다.
- 감지된 경우 점수를 부여합니다.

### 2. **티어 시스템**
- 점수가 누적되면 사용자의 티어가 상승합니다.

### 3. **리더보드**
- 티어와 점수를 기준으로 사용자 순위를 표시합니다.
- 그룹 전체 순위를 제공합니다.

### 4. **사용자 친화적인 명령어**
- 점수, 티어, 리더보드 순위를 확인할 수 있는 간단한 명령어를 제공합니다.

---

## 사전 준비

### 1. **Python 환경**
- Python 3.8 이상 설치.

### 2. **필수 라이브러리**
아래 명령어를 사용하여 필요한 라이브러리를 설치하세요:
```bash
pip install -r requirements.txt
```

### 3. **MongoDB**
- MongoDB 인스턴스 실행(로컬 또는 클라우드 기반).
- 사용자 데이터를 저장할 데이터베이스와 컬렉션 생성.

---

## 설치 및 설정

1. **레포지토리 클론**
```bash
git clone <repository_url>
cd <repository_folder>
```

2. **환경 변수 설정**
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 추가하세요:
```
DISCORD_TOKEN=your_discord_bot_token
MONGODB_URI=your_mongodb_connection_string
```

3. **봇 실행**
```bash
python bot.py
```

---

## 명령어

| 명령어               | 설명                                         |
|----------------------|---------------------------------------------|
| `/현재티어`           | 현재 티어 및 점수를 확인합니다.               |
| `/티어리스트`         | 모든 티어 및 달성 조건을 확인합니다.           |
| `/티어랭킹`           | 그룹 순위를 표시합니다.                       |
| `/도움말`             | 모든 명령어를 확인합니다.                     |
---

## 기여하기
이 프로젝트에 기여하려면 레포지토리를 포크하고 풀 리퀘스트를 제출하세요. 코드가 기존 규칙을 따르고 적절한 문서를 포함하고 있는지 확인해주세요.

---

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다.

---

## 문의
문의 사항이나 문제가 있을 경우 [kds1644416@gmail.com]으로 연락해주세요.

