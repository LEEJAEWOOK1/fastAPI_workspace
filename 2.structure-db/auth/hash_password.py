import bcrypt
class HashPassword:
    def create_hash(self, password : str) -> str:
        # 평문(문자열) -> byte 형식으로 -> 비밀번호 해싱(암호화) -> 문자열로 변환 후 저장
        pwd_byte = password.encode("utf-8")
        hashed = bcrypt.hashpw(pwd_byte, bcrypt.gensalt())
        pwd = hashed.decode("utf-8")
        print("저장할 pwd : ", pwd)
        return pwd
    def verify_hash(self, input_pwd:str, db_pwd:str) -> bool:
        #로그인
        #data.password == db.password
        return bcrypt.checkpw(input_pwd.encode("utf-8"), db_pwd.encode("utf-8"))