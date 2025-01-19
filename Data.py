from pymongo import MongoClient
import os
from dotenv import load_dotenv
import discord

load_dotenv()  

class db:
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
    async def add_point(message):
        client = db.connect_mongodb()
        if not client:
            print("Database connection failed.")
            return

        database = client["User"]
        collection = database["UserInfo"]

        server_id = str(message.guild.id)
        user_id = str(message.author.id)

        try:
            user = collection.find_one({"user_id": user_id, "server_id": server_id})
            if user:
                new_points = user.get("Points", 0) + 1
                collection.update_one(
                    {"server_id": server_id, "user_id": user_id},
                    {"$set": {"Points": new_points}}
                )
                print(f"Updated points for user {user_id} in server {server_id} to {new_points}.")

                # 티어 변경이 필요한 경우
                new_tier = db.Update_rank(server_id, user_id, new_points)
                if new_tier:
                    await message.channel.send(
                        f"🎉 <@{user_id}> 님이 **{new_tier}** 티어로 승급했습니다! 축하합니다! 🎉"
                    )
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
            return new_tier;
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
        if not client:
            print("Database connection failed.")
            return []
        database = client["User"]
        collection = database["UserInfo"]

        try:
            users = collection.find({"server_id": str(server_id)}).sort("Points", -1).limit(5)
            return list(users)
        except Exception as e:
            print(f"Error fetching ranking for server {server_id}: {e}")
            return []
