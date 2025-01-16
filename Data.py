from pymongo import MongoClient
import os #깃허브에 올렸을 때 사람들이 데이터베이스 정보 못보게 하기 위함(pip 필요없음)
from dotenv import load_dotenv

load_dotenv()  #<- .env 파일 생성해서 민감한 정보 숨겨서 저장 이걸로 토큰도 숨길수 있을 듯? https://hyunhp.tistory.com/718
               #여기서 생성한 .env파일을 깃에서  push할 때 못 올리게 gitignore를 만들어서 숨겨줄거임 https://velog.io/@jisu243/env%ED%8C%8C%EC%9D%BC-.gitignore%EB%A1%9C-%EC%95%88%EB%B3%B4%EC%9D%B4%EA%B2%8C-%EB%A7%8C%EB%93%A4%EA%B8%B0