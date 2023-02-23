from flask_restful import Api, Resource
from flask import request, Blueprint
from ...models import Offer, OfferSchema, db
from flask_jwt_extended import jwt_required, get_jwt_identity

offer_schema = OfferSchema()
offer_api = Blueprint("offer_api", __name__, url_prefix="/offers")
api = Api(offer_api)

# /offers
class OfferResource(Resource):

    @jwt_required()
    def post(self):       
        userId = userId = get_jwt_identity() 
        postId = request.json["postId"]        
        description = request.json["description"]
        size = request.json["size"]
        fragile = request.json["fragile"]
        offer = request.json["offer"]
      
        if size not in ["LARGE", "MEDIUM", "SMALL"]:
            return "Size only allow LARGE, MEDIUM or SMALL", 412
        
        new_offer = Offer(postId, userId, description, size, fragile, offer)
        db.session.add(new_offer)
        db.session.commit()
        
        return {
            "id" : new_offer.id,
            "userId": new_offer.userId,
            "createdAt": new_offer.createdAt.strftime('%Y-%m-%dT%H:%M:%S. %f%z')
        }, 201

# /offers?post=id&filter=me
class FilterOfferResource(Resource):
    
    @jwt_required()
    def get(self):
        postId = request.args.get("post", None)
        filter =  request.args.get("filter", None)
        userId = get_jwt_identity()
        query = Offer.query.filter()
         
        if(all(v is None for v in [postId,filter])):
            return [offer_schema.dump(offers) for offers in Offer.query.all()]
        
        if filter is not None and filter.upper() == "ME":
             query = query.filter(Offer.userId == userId)
        
        if postId is not None:
            query = query.filter(Offer.postId == postId)  
                
        return [offer_schema.dump(offers) for offers in query.all()]

# /offers/{id}
class GetOfferResource(Resource):

    @jwt_required()
    def get(self, id_offer):
        return offer_schema.dump(Offer.query.get_or_404(id_offer))

# /offers/ping
class PingOfferResource(Resource):

    def get(self):
        return "pong", 200

api.add_resource(OfferResource, '/')
api.add_resource(FilterOfferResource, '/')
api.add_resource(GetOfferResource, '/<id_offer>')
api.add_resource(PingOfferResource, '/ping')