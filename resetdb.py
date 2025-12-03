from sqlalchemy import text

from api.dependencies.database import engine, Base

from api.models import (
    orders,
    order_details,
    payments,
    menu,
    recipes,
    sandwiches,
    resources,
)

def main():
    # turn off FK checks so we can drop in any order
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)

        print("Creating all tables...")
        Base.metadata.create_all(bind=engine)

        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

    print("Done!")

if __name__ == "__main__":
    main()