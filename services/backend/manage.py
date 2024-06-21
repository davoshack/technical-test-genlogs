from flask.cli import FlaskGroup

from src import create_app, db
from src.api.carriers.models import Carrier
from src.api.users.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        User(
            username="test_user",
            email="test_user@test.com",
            password="supersecretpassword",
        )
    )
    db.session.add(Carrier(name="Knight-Swift Transport Services"))
    db.session.add(Carrier(name="J.B. Hunt Transport Services Inc"))
    db.session.add(Carrier(name="YRC Worldwide"))
    db.session.add(Carrier(name="XPO Logistics"))
    db.session.add(Carrier(name="Schneider"))
    db.session.add(Carrier(name="Landstar Systems"))
    db.session.add(Carrier(name="UPS Inc"))
    db.session.add(Carrier(name="FedEx Corp"))

    db.session.commit()


if __name__ == "__main__":
    cli()
