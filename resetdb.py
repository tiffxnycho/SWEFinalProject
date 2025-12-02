
from api.dependencies.database import engine, Base
from api.models import orders, order_details, menu, recipes, sandwiches, resources


def main():
    print("Dropping tables...")
    Base.metadata.drop_all(bind=engine)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    print("DB reset complete.")


if __name__ == "__main__":
    main()