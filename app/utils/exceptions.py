from abc import ABC, abstractmethod
from fastapi import HTTPException, status


class ExeptionsInterface(ABC):
    @abstractmethod
    def exception_401(self, message: str):
        raise NotImplemented("No method exception_401")

    @abstractmethod
    def exception_404(self, message: str):
        raise NotImplemented("No method exception_404")

    def exception_403(self):
        raise NotImplemented("No method exception_403")

    def exception_500(self):
        raise NotImplemented("No method exception_500")


class CustomExceptions(ExeptionsInterface):
    def exception_401(self, message: str):
        raise HTTPException(detail=message, status_code=status.HTTP_401_UNAUTHORIZED)

    def exception_404(self, message: str):
        raise HTTPException(detail=message, status_code=status.HTTP_404_NOT_FOUND)

    def exception_403(self):
        raise HTTPException(
            detail="Access denied", status_code=status.HTTP_403_FORBIDDEN
        )

    def exception_500(self):
        raise HTTPException(
            detail="Server Error. Connect to Admin!",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
