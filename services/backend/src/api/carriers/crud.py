from src.api.carriers.models import Carrier


def get_all_carriers():
    return Carrier.query.all()


def get_carrier_by_id(carrier_id):
    return Carrier.query.filter_by(id=carrier_id).first()
