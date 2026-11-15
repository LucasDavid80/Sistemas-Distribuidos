from app.database.session import SessionLocal
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserRole
from app.services.user_service import create_user

EMAIL = "demo.seller@c216.local"


def main() -> None:
    with SessionLocal() as db:
        repository = UserRepository(db)
        seller = repository.get_by_email(EMAIL)
        if seller is None:
            seller = create_user(
                db,
                UserCreate(
                    nome="Vendedor Demo",
                    email=EMAIL,
                    idade=30,
                    role=UserRole.SELLER,
                ),
            )
            print(f"Vendedor demo criado: id={seller.id}")
        else:
            print(f"Vendedor demo já existe: id={seller.id}")
        print(f"VITE_USER_ID={seller.id}")


if __name__ == "__main__":
    main()
