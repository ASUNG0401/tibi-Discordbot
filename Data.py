import pymysql #my sql 데이터 베이스 파이썬에서 쓰기위해 (pip insatll pymysql)
import os #깃허브에 올렸을 때 사람들이 데이터베이스 정보 못보게 하기 위함(pip 필요없음)
from dotenv import load_dotenv
import pymysql.cursors #pip install python-dotenv

load_dotenv()  #<- .env 파일 생성해서 민감한 정보 숨겨서 저장 이걸로 토큰도 숨길수 있을 듯? https://hyunhp.tistory.com/718
               #여기서 생성한 .env파일을 깃에서  push할 때 못 올리게 gitignore를 만들어서 숨겨줄거임 https://velog.io/@jisu243/env%ED%8C%8C%EC%9D%BC-.gitignore%EB%A1%9C-%EC%95%88%EB%B3%B4%EC%9D%B4%EA%B2%8C-%EB%A7%8C%EB%93%A4%EA%B8%B0

class Connection:              #데이터 베이스 접근 코드
    def __init__(self):        #초기화
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.conn = None
        self.cur = None

    def connect(self):        #연결 
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            self.cur = self.conn.cursor()
            print("DB연결 완료")
        except pymysql.MySQLError as e:     #연결 실패시시
            print(f"DB연결 실패: {e}")
            self.conn = None

    def add_user(self, user_id, user_name):  # 신규 유저 추가
        if not self.conn:
            self.connect()
        try:
            sql = ""
            self.cur.execute(sql, (user_id, user_name))
            self.conn.commit()
            print(f"유저 추가 완료: {user_name}")
        except pymysql.MySQLError as e:
            print(f"유저 추가 실패: {e}")
    
    def __del__(self):       #연결 해제
        self.conn.close()
        print("DB연결 해제")
    
    def getConnection(self):  #연결이 잘 되있는지 확인하는 코드드
        self.conn.ping()
        return self.conn, self.cur
    