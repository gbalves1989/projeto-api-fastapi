from passlib.context import CryptContext


class Hash:
    def __init__(self) -> None:
        self.crypto: CryptContext = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )
    
    def verify_password(self, password: str, hash_password: str) -> bool:
        return self.crypto.verify(password, hash_password)

    def generate_hash_password(self, password: str) -> str:
        return self.crypto.hash(password)
    