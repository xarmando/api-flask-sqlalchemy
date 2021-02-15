from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from models.item import ItemModel


class Item(Resource):
    # make sure the payload come with fields taht we expectes
    # we can parse the payload and handle on this way using reqparser
    # if teh payloa docme with other arguments, after parser it, we wont see them
    # rememner, parser belongs to Item class
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left empty!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id!"
                        )

    # @jwt_required()
    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 400

    @jwt_required
    def post(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            return {"message": "An item with name '{}' already exist.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)  # data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error acourred inserting the item'}, 500

        # on flas_resful, we dont need to parse dictionary to JSON, flask will make for us.
        return item.json(), 201  # other codes 200-OK, 201-CREATED, 202-ACCEPTED

    @jwt_required
    def delete(self, name):

        # its gonna get the data from the request
        # jwt come in throught the request and its goin to extract any claims
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        #updated_item = ItemModel(name, data['price'])
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {'message': 'An error ocurred inserting the item'}, 400
        else:
            try:
                item.price = data['price']
            except:
                return {'message': 'An error ocurred updating the item'}, 500

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required
    def get(self):
        # it is not a good practice use query object on resource .query.all() . Instead, create a funciton  in the mdel
        return {'items': [item.json() for item in ItemModel.find_all()]}
