from fastapi import APIRouter, Body
from pydantic import BaseModel
from starlette.responses import JSONResponse

router = APIRouter(tags=["Auth"])


class LoginRequest(BaseModel):
    login: str
    password: str


# main auth endpoints
@router.post("/login")
def login(body: LoginRequest = Body(...)):
    print(body)
    return JSONResponse(content={"message": "Login endpoint"}, status_code=200)


@router.post("/logout")
def logout():
    return {"message": "Logout endpoint"}


# tokent related endpoints
@router.post("/check-token")
def check_token():
    return {"message": "Check token endpoint"}


@router.post("/check-token")
def check_token():
    return {"message": "Check token endpoint"}


# user related endpoints
@router.get("/user")
def get_user():
    return {"message": "User info"}


@router.post("/user/priveleges")
def user_priveleges():
    return {"message": "User priveleges endpoint"}


@router.patch("/user/update-password")
def user_upate_password():
    return {"message": "user_upate_password"}
