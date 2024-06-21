from flask_restx import Namespace, Resource, fields

from src.api.carriers.crud import (  # isort:skip
    get_all_carriers,
    get_carrier_by_id,
)

carriers_namespace = Namespace("carriers")


carrier = carriers_namespace.model(
    "Carrier",
    {
        "id": fields.Integer(readOnly=True),
        "name": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


class CarriersList(Resource):
    @carriers_namespace.marshal_with(carrier, as_list=True)
    def get(self):
        """Returns all carriers."""
        return get_all_carriers(), 200


class Carriers(Resource):
    @carriers_namespace.marshal_with(carrier)
    @carriers_namespace.response(200, "Success")
    @carriers_namespace.response(404, "Carrier <carrier_id> does not exist")
    def get(self, carrier_id):
        """Returns a single carrier."""
        carrie = get_carrier_by_id(carrier_id)
        if not carrie:
            carriers_namespace.abort(404, f"Carrier {carrier_id} does not exist")
        return carrie, 200


carriers_namespace.add_resource(CarriersList, "")
carriers_namespace.add_resource(Carriers, "/<int:carrier_id>")
