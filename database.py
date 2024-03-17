import pyrebase
import json
import hashlib
import requests

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

            firebase = pyrebase.initialize_app(config)
            self.db = firebase.database()

# users 더미 데이터 생성
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

# 비밀번호 해시 함수
    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

# 로그인 시 입력 데이터와 더미 데이터 비교
    def find_user(self, id, password_hash):
        users = self.db.child("users").get()
        for user in users.each():
            if user.val()['id'] == id and user.val()['password'] == password_hash:
                return True, user.val()['name']
        return False, None

# 단체 활동 DB로 전송(Create)
    def add_group_activity(self, kind, name):
        new_group_activity = {
            "kind":kind,
            "name":name
        }

        self.db.child("group_activities").push(new_group_activity)

# 개인 활동 DB로 전송(Create)
    def add_personal_activity(self, kind, name):
        new_personal_activity = {
            "kind":kind,
            "name":name
        }

        self.db.child("personal_activities").push(new_personal_activity)

# 단체 활동 DB에서 불러오기(Read)
    def get_group_activities(self):
        # Firebase에서 group_activities 데이터를 조회
        activities = self.db.child("group_activities").get()
        if activities.val():
            # 조회된 데이터를 리스트로 변환하여 반환
            return [{"id": activity.key(), "kind": activity.val()['kind'], "name": activity.val()['name']} for activity in activities.each()]
        else:
            # 데이터가 없는 경우 빈 리스트 반환
            return []

# 개인 활동 DB에서 불러오기(Read)
    def get_personal_activities(self):
         # Firebase에서 personal_activities 데이터를 조회
        activities = self.db.child("personal_activities").get()
        if activities.val():
            # 조회된 데이터를 리스트로 변환하여 반환
            return [{"id": activity.key(), "kind": activity.val()['kind'], "name":activity.val()['name']} for activity in activities.each()]
        else:
            # 데이터가 없는 경우 빈 리스트 반환
            return []
        
# 특정 단체 활동을 ID로 조회(Read)
    def get_group_activity_by_id(self, activity_id):
        activity = self.db.child("group_activities").child(activity_id).get()
        if activity.val():
            return {"id": activity_id, "kind": activity.val().get('kind'), "name": activity.val().get('name')}
        else:
            return None

# 특정 개인 활동을 ID로 조회(Read)
    def get_personal_activity_by_id(self, activity_id):
        activity = self.db.child("personal_activities").child(activity_id).get()
        if activity.val():
            return activity.val()
        else:
            return None
        
# 특정 단체 활동의 todo 리스트 작성(Create)
    def add_group_todo(self, activity_id, task1, task2, task3, takeaway):
        new_group_todo = {
            "activity_id": activity_id,
            "task1": task1,
            "task2": task2,
            "task3": task3,
            "takeaway": takeaway
        }

        self.db.child("group_todos").push(new_group_todo)

# 특정 단체 활동의 모든 todo 리스트 가져오기(Read)
    def get_group_todos_by_activity_id(self, activity_id):
        # Correctly encode the orderBy query
        todos = self.db.child("group_todos").order_by_child("activity_id").equal_to(activity_id).get()
        if todos.val():
            # Process and return todos as a list of dictionaries
            return [{**todo.val(), "id": todo.key()} for todo in todos.each()]
        else:
            # Return an empty list if no todos are found
            return []

    
    # Use this method instead of the one provided by pyrebase if you continue to have issues
    def get_group_todos_by_activity_id(self, activity_id):
        # Construct the URL for the Firebase REST API call
        url = f"https://portodo-9c86a-default-rtdb.firebaseio.com/group_todos.json"
        query = {
            'orderBy': json.dumps("activity_id"),
            'equalTo': json.dumps(activity_id)
        }
        response = requests.get(url, params=query)
    
        # Check if the request was successful
        if response.status_code == 200:
            todos = response.json()
            # Process and return todos as a list of dictionaries
            return [{**todo, "id": key} for key, todo in todos.items() if todo] if todos else []
        else:
            # Handle errors
            print(f"Failed to retrieve todos: {response.text}")
            return []



# DBhandler 인스턴스 생성
db_handler = DBhandler()

# 더미 데이터 추가 함수 호출
db_handler.add_dummy_data()
