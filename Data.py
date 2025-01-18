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

        database = client["User"]
        collection = database["UserInfo"]

        server_id = str(message.guild.id)
        user_id = str(message.author.id)

        try:
            user = collection.find_one({"user_id": user_id,"server_id": server_id})
            if user:
                # 기존 유저의 포인트 증가
                new_points = user.get("Points", 0) + 1
                collection.update_one(
                    {"server_id": server_id, "user_id": user_id},
                    {"$set": {"Points": new_points}}
                )
                print(f"Updated points for user {user_id} in server {server_id} to {new_points}.")

                if new_points in {50, 100, 200, 500, 1000, 10000}:
                    db.Update_rank(server_id, user_id, new_points)
            else:
                user_data = {
                    "user_id": user_id,
                    "server_id": server_id,
                    "Points": 1,
                    "Tier": "Unranked"
                }
                collection.insert_one(user_data)
                print(f"Added new user {user_id} in server {server_id} with 1 point.")
        except Exception as e:
            print(f"Error updating or inserting user: {e}")

    @staticmethod
    def Get_rank(server_id, user_id):
        client = db.connect_mongodb()
        if not client:
            return None

        database = client["User"]
        collection = database["UserInfo"]

        try:
            user = collection.find_one({"user_id": str(user_id),"server_id": str(server_id)})
            if user:
                return user.get("Tier")
            else:
                print(f"No rank found for user {user_id} in server {server_id}.")
                return None
        except Exception as e:
            print(f"Error fetching rank for user {user_id}: {e}")
            return None

    @staticmethod
    def Update_rank(server_id, user_id, points):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return

        database = client["User"]
        collection = database["UserInfo"]

        if points > 9999:
            new_tier = "Master"
        elif points > 999:
            new_tier = "Diamond"
        elif points > 499:
            new_tier = "Platinum"
        elif points > 199:
            new_tier = "Gold"
        elif points > 99:
            new_tier = "Silver"
        elif points > 49:
            new_tier = "Bronze"
        else:
            return 

        try:
            collection.update_one(
                {"user_id": str(user_id),"server_id": str(server_id),},
                {"$set": {"Tier": new_tier}}
            )
            print(f"Updated rank for user {user_id} in server {server_id} to {new_tier}.")
        except Exception as e:
            print(f"Error updating rank for user {user_id}: {e}")

    @staticmethod
    def Get_points(server_id, user_id):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return None

        database = client["User"]
        collection = database["UserInfo"]

        try:
            user = collection.find_one({"user_id": str(user_id),"server_id": str(server_id)})
            if user:
                return user.get("Points")
            else:
                print(f"No points found for user {user_id} in server {server_id}.")
                return None
        except Exception as e:
            print(f"Error fetching points for user {user_id}: {e}")
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
