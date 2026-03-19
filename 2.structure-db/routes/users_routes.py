from fastapi import APIRouter, HTTPException, status, Depends
from models.users_models import User, UserSignIn
from database.connection import get_session

user_router = APIRouter(tags=["User"])

users = []

@user_router.get("/test")
async def test() -> dict:
    return {"msg":"test"}
#회원추가
@user_router.post("/signup", status_code=201)
async def insert(data : User, session = Depends(get_session)) -> dict:
    # users = [User{email:111}, User{email:222}]
    # data{email:..., pwd:...}
    
    # if any(user.email == data.email for user in users): 
    #     raise HTTPException(
    #         status_code= status.HTTP_409_CONFLICT,
    #         detail="존재하는 email"
    #     )
    
    for user in users:
        if data.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="존재하는 email"
            )
    #users.append(data)
    session.add(data)
    session.commit()

    session.refresh(data)
    print("refresh : ", data)
    
    return {"msg":"가입 성공"}

@user_router.post("/signin")
async def siginin_user(data : UserSignIn) -> dict:
    # email, pwd 비교
    print("signin : ", data)
    for user in users:
        if data.email == user.email:
            if data.password == user.password:
                return {"msg":"인증 성공"} # 인증 성공
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="비밀번호 틀림" # 인증 실패(pwd 틀림)
                )
    raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 email"
        )