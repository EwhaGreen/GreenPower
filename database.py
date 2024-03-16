import pyrebase
import json
import hashlib

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

    def add_dummy_data(self):
        # 여러 사용자의 더미 데이터 정의
        users_data = {
            "user1": {
                "id": "greenpower",
                "password": self.hash_password("aaaa"),
                "name": "김이화",
                "department": "컴퓨터공학과",
                "student_id": "2171019",
                "career": "백엔드 개발자"
            },
            "user2": {
                "id": "1234",
                "password": self.hash_password("bbbb"),
                "name": "이하나",
                "department": "차세대기술공학부",
                "student_id": "2372020",
                "career": "임베디드 시스템 개발자"
            },
            "user3": {
                "id": "4567",
                "password": self.hash_password("cccc"),
                "name": "박지민",
                "department": "휴먼기계바이오공학부",
                "student_id": "2170021",
                "career": "로봇 공학자"
            },
            "user4": {
                "id": "91011",
                "password": self.hash_password("dddd"),
                "name": "정수빈",
                "department": "통계학과",
                "student_id": "1829022",
                "career": "화학 분석가"
            },
            "user5": {
                "id": "121314",
                "password": self.hash_password("eeee"),
                "name": "최율하",
                "department": "문헌정보학과",
                "student_id": "2183023",
                "career": "데이터 분석가"
            },
            "user6": {
                "id": "151617",
                "password": self.hash_password("ffff"),
                "name": "정유하",
                "department": "경영학과",
                "student_id": "2185024",
                "career": "기획자"
            }
        }

        # 더미 데이터를 Firebase Realtime Database에 추가
        self.db.child("users").set(users_data)

    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def find_user(self, id, password_hash):
        users = self.db.child("users").get()
        for user in users.each():
            if user.val()['id'] == id and user.val()['password'] == password_hash:
                return True, user.val()['name']
        return False, None

# DBhandler 인스턴스 생성
db_handler = DBhandler()

# 더미 데이터 추가 함수 호출
db_handler.add_dummy_data()
