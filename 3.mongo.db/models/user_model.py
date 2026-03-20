from beanie import Document
from typing import Optional
#컬렉션(Document 상속->MongoDB 컬렉션과 연결)
class User(Document):
    name : str
    email : str
    age : Optional[int] = None #age는 있어도 되고 없어도 된다.

    class Settings: # 저장소
        name = "users"