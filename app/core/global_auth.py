from abc import ABC, abstractmethod
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from logger_config import logger

from app.utils.exceptions import ExeptionsInterface

# to generate the key import secrets secrets.token_hex(32)
SECRET_KEY = "9eeaa6c9ded40b858183b7a0f2a3cb5b3462bb566fa629eea6d20d1639234ea3"

ALGORITHM = "H256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], depricated="auto")

auth = OAuth2PasswordBearer()  # add link login


class Auth(ABC):
    @abstractmethod
    def verify_password(self, plain_password: str, hash_password: str):
        raise NotImplemented("Method verify_password not implemented..")

    @abstractmethod
    def create_access_token(self, user_id: int):
        raise NotImplemented("Method create_access_token not implemented..")

    @abstractmethod
    def verify_password(self, token: str):
        raise NotImplemented("Method verify_password not implemented..")

    @abstractmethod
    def auth_user(self, login: str, password: str):
        raise NotImplemented("Method verify_password not implemented..")


class GlobalAuth(Auth):
    def __init__(self, exceptions: ExeptionsInterface):
        self._exeption_interface = exceptions

    def verify_password(self, plain_password: str, hash_password: str):
        """verify the password hash"""
        return pwd_context.verify(plain_password, hash_password)

    def verify_token(self, token: str) -> bool:
        """verify the token"""
        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return False
        return True

    def _get_hash_password(self, password: str):
        return pwd_context.hash(password)

    def create_access_token(self, user_id: int) -> str:
        try:
            date_expired = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            jwt_token = jwt.encode(
                {"exp": date_expired, "uid": user_id}, SECRET_KEY, algorithm=ALGORITHM
            )
            return jwt_token
        except JWTError as e:
            logger.exception(f"Some unexpected error {e}")
            raise self._exeption_interface.exception_500()

    def auth_user(self, user_name: str, password: str):
        logger.debug("autorisatie user")
        # todo get user from db
        user = ""
        user_pass_from_db = ""
        if not self.verify_password(user_pass_from_db, password):
            logger.warning(f"{user_name} not autorisatie")
            return None
        logger.success(f"{user_name} autorisatie")
        return user

    def get_current_user(self, token: str = Depends(auth)):
        try:
            token_info = jwt.encode(token, SECRET_KEY, algorithm=[ALGORITHM])
            user_id = token_info.get("uid")
            if user_id is None:
                logger.warning("not autorisatie")
                raise self._exeption_interface.exception_404(f"Not found user_id!")
            # todo get user from db
            user = ""
            if user is None:
                logger.warning("not user in db")
                raise self._exeption_interface.exception_404(f"Not found user!")
            return user
        except JWTError:
            raise self._exeption_interface.exception_401("No UNAUTHORIZED!")

    def _check_user_privilege(
        self, privilege: str, current_user=Depends(get_current_user)
    ):
        try:
            get_all_user_privilege = ""  # todo get from db
            if privilege not in get_all_user_privilege:
                logger.warning(f"No privilege {privilege} in user")
                raise self._exeption_interface.exception_403()

            return True
        except Exception as e:
            logger.exception(f"Some unexpected error {e}")
            raise self._exeption_interface.exception_500()

    def check_user_access(self, privilege: str):
        return self._check_user_privilege(privilege)


if __name__ == "__main__":
    print("Auth")
