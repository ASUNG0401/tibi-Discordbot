from pymongo import MongoClient
import os
from dotenv import load_dotenv
import discord

load_dotenv()  # 환경변수 로드

class db:
    # MongoDB 연결을 한 번만 시도하고 재사용
    client = None

    @staticmethod
    def connect_mongodb():
        if db.client is None:
            uri = os.getenv("URI")
            db.client = MongoClient(uri)
            try:
                db.client.admin.command('ping')
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)
                db.client = None
        return db.client

    @staticmethod
    def add_point(message):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return

        # 데이터베이스와 컬렉션 설정
        database = client["User"]
        collection = database["UserInfo"]

        try:
            # 사용자 검색
            user = collection.find_one({
                "user_id": str(message.author.id),
                "server_id": str(message.guild.id)
                })
            if user:
                # 기존 유저의 Points 값을 증가
                new_points = user.get("Points", 0) + 1
                collection.update_one(
                    {"user_id": str(message.author.id), "server_id": str(message.guild.id)},
                    {"$set": {"Points": new_points}}
                )
                print(f"Updated points for user {message.author.id} to {new_points}.")
                if new_points == 8 or new_points == 10 or new_points == 12 or new_points == 14:
                    db.Update_rank(message, message.author.id, new_points)
            else:
                # 새로운 유저 데이터 추가
                user_data = {
                    "user_id": str(message.author.id),
                    "server_id": str(message.guild.id),  
                    "Points": 1,
                    "Tier": "Unranked"
                }
                collection.insert_one(user_data)
                print(f"Added new user {message.author.id} with 1 point.")
        except Exception as e:
            print(f"Error updating or inserting user: {e}")

    @staticmethod
    def Get_rank(id):
        client = db.connect_mongodb()
        if not client:
            return None

        database = client["User"]
        collection = database["UserInfo"]
        try:
            user = collection.find_one({"user_id": str(id)})    # 고유 ID로 유저 찾기
            if user:
                return user.get("Tier")
            else:
                print(f"No rank found for user: {id}")
                return None
        except Exception as e:
            print(f"Error fetching rank for user {id}: {e}")
            return None

    @staticmethod
    def Update_rank(message, id, points):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return

        database = client["User"]
        collection = database["UserInfo"]

        # 포인트에 따른 새로운 티어 계산
        if points > 13:
            new_tier = "Platinum"
        elif points > 11:
            new_tier = "Gold"
        elif points > 9:
            new_tier = "Silver"
        elif points > 7:
            new_tier = "Bronze"
        else:
            return  # 등급이 변하지 않음

        try:
            # 사용자의 Tier 값을 업데이트
            collection.update_one(
                {"user_id": str(id)},
                {"$set": {"Tier": new_tier}}
            )
            print(f"Updated rank for user {id} to {new_tier}.")
        except Exception as e:
            print(f"Error updating rank for user {id}: {e}")

    def Get_points(id):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return
        database = client["User"]
        collection = database["UserInfo"]
        try:
            user = collection.find_one({"user_id": str(id)})    # 고유 ID로 유저 찾기
            if user:
                return user.get("Points")
            else:
                print(f"No Point found for user: {id}")
                return None
        except Exception as e:
            print(f"Error fetching Point for user {id}: {e}")
            return None
        
    @staticmethod
    def get_server_ranking(server_id):
        client = db.connect_mongodb()
        #mongodb 잘 연결 됐는지 확인하기 위해서 if not client씀 
        if not client:
            print("Database connection failed.")
            return []
        #client에서 유저 그리고 유저안에서 유저인포 가져오기 
        database = client["User"]
        collection = database["UserInfo"]

        try:
            #유저의 서버 아이디를 찾고 (데이터 조회) 그리고 sort로 정렬함 정렬하기 위해서 points를 기준으로 
            # 삼아 정렬하고 -1은 내림차순으로 정렬한다는 의미. 따라서 높은 점수부터 낮은 점수 순으로 정렬됨. 
            # limit(5)은 상위 5명만 가져올거라 5까지 제한둔거
            users = collection.find({"server_id": str(server_id)}).sort("Points", -1).limit(5)
            #그 후, 정렬된 데이터를 리스트로 변환해서 반환함
            return list(users)
        except Exception as e:
            print(f"Error fetching ranking for server {server_id}: {e}")
            return []
