from fastapi import FastAPI , APIRouter, Path, Query, HTTPException, status
from PackBook import User

app = FastAPI(title="TEST FASTAPI",
              description="fastapi example",
              version="1.0.0"
              )
router = APIRouter()

users = []

@router.get("/test")
async def test() -> dict:
    return {"msg":"test msg"}
# 회원 추가
@router.post("/insert")
async def insert( user : User ) -> dict:
    #print( user )
    users.append( user )
    return {"msg":"데이터 추가 성공"}
# 회원 전체 리스트 보기
@router.get("/select", response_model=list[User])
async def select() -> list:
    return users
# 특정 리스트 보기(response 직접 구성)
@router.get("/path/{id}",
    responses={
        200: { "description": "successfully",
            "content": {
                "application/json": { "example": {"id": 1, "name": "홍길동"} }
            },
        },
        404: { "description": "User not found",
            "content": {
                "application/json": { "example": {} }
            },
        },
})
# 기본형태 FastAPI가 자동으로 판단
async def get_one(id:int) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return{}
# 실제 응답 데이터 검증(반환값이 User 형태인지 검사, 자동으로 JSON 변환), 자동 필터링, 실제 상태코드 적용됨, Path 명시
@router.get("/path2/{id}", response_model = User, status_code=status.HTTP_201_CREATED)
async def get_one(id:int = Path(..., )) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return{}

@router.get("/query")
async def get_one(id:int) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return{}

@router.get("/query2")
async def get_one(id:int = Query(1, description="사용자 id")) -> dict:
    for user in users:
        if user.id == id:
            return user.dict()
    return{}

@router.put("/update/{id}", status_code = 200)
async def update(u:User, id:int) -> dict:
    for user in users:
        if user.id == id:
            user.name = u.name
            return {"msg":"update succeccfully"}
    raise HTTPException(status_code=404, detail="id 없음")

@router.delete("/delete", status_code= status.HTTP_200_OK)
async def del_all() -> dict:
    users.clear()
    return {"msg":"del succ"}

app.include_router( router )