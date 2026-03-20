from fastapi import APIRouter
from models.user_model import User

user_route = APIRouter(tags=["User"])

# 모든 데이터 보기
@user_route.get("/all")
async def all_user():
    users = User.find_all()
    print("users : ", users)
    data = await users.to_list() # db에서 조회한 데이터를 리스트로 변환
    print("실제 데이터 : ", data)
    return data

# 데이터 추가
@user_route.post("/insert")
async def insert(user : User):
    await user.create()
    return {"id":str(user.id)}

# 특정 데이터 보기(id로)
@user_route.get("/one/{user_id}")
async def one_user(user_id : str):
    user = User.get(user_id)
    if user:
        return await user
    return {"msg":"데이터 없음"}

#특정 데이터 보기(name으로(User 컬렉션의 name과 사용자가 입력한 name 비교))
@user_route.get("/name/{user_name}")
async def one_user(user_name : str):
    user = await User.find_one(User.name == user_name)
    if user:
        return user
    return {"msg":"데이터 없음"}

# 데이터 삭제
@user_route.delete("/del/{user_name}")
async def del_user(user_name : str):
    count = await User.find_one(User.name == user_name).delete()
    return {"msg" : f"삭제 된 수 : {count}"}

# 데이터 수정
@user_route.put("/update/{user_name}")
async def update_user(user_name:str, new_age:int):
    user = await User.find_one(User.name == user_name)
    user.age = new_age
    await user.save()
    return {"msg": "수정 성공", "user" : user}