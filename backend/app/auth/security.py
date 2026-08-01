from dataclasses import dataclass


@dataclass(slots=True)
class UserPrincipal:
    user_id: str
    email: str
    role: str


class AuthService:
    def authenticate(self, email: str, password: str) -> UserPrincipal | None:
        del password
        if not email:
            return None
        return UserPrincipal(user_id="placeholder", email=email, role="viewer")
