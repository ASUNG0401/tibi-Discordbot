from pymongo import MongoClient
import os #깃허브에 올렸을 때 사람들이 데이터베이스 정보 못보게 하기 위함(pip 필요없음)
from dotenv import load_dotenv

load_dotenv()  #<- .env 파일 생성해서 민감한 정보 숨겨서 저장 이걸로 토큰도 숨길수 있을 듯? https://hyunhp.tistory.com/718
               #여기서 생성한 .env파일을 깃에서  push할 때 못 올리게 gitignore를 만들어서 숨겨줄거임 https://velog.io/@jisu243/env%ED%8C%8C%EC%9D%BC-.gitignore%EB%A1%9C-%EC%95%88%EB%B3%B4%EC%9D%B4%EA%B2%8C-%EB%A7%8C%EB%93%A4%EA%B8%B0
class db :
    def connect_mongodb():
        uri = (os.getenv("URI"))   
        client = MongoClient(uri)
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            return client
        except Exception as e:
            print(e)
            return None
    def add_point(message):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return

        # 데이터베이스와 컬렉션 설정
        database = client["User"]
        collection = database["UserInfo"]

        # 사용자 검색
        try:
            user = collection.find_one({"user_id": str(message.author.id)})
            if user:
                # 기존 유저의 Points 값을 증가
                new_points = user.get("Points", 0) + 1
                collection.update_one(
                    {"user_id": str(message.author.id)},
                    {"$set": {"Points": new_points}}
                )
                print(f"Updated points for user {message.author.id} to {new_points}.")
            else:
                # 새로운 유저 데이터 추가
                user_data = {
                    "user_id": str(message.author.id),
                    "Points": 1,
                    "Tier": "Unranked"
                }
                collection.insert_one(user_data)
                print(f"Added new user {message.author.id} with 1 point.")
        except Exception as e:
            print(f"Error updating or inserting user: {e}")

    def find_User(id):
        client = db.connect_mongodb()

        database = client["User"]
        collection = database["UserInfo"]
        
        try:
            user = collection.find_one({"user_id":str(id)})
            if user:
                return True
            else:
                return False
        except Exception as e:
            return None
    


    