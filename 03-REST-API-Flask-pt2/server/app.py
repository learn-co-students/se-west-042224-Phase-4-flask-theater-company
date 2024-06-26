#!/usr/bin/env python3
# 📚 Review With Students:
# REST
# Status codes
# Error handling
# Set up:
# cd into server and run the following in the terminal
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5000
# flask db init
# flask db revision --autogenerate -m'Create tables'
# flask db upgrade
# python seed.py
from flask import Flask, abort, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import CastMember, Production, db

# 1.✅ Import NotFound from werkzeug.exceptions for error handling
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

Api.error_router = lambda self, handler, e: handler(e)
api = Api(app)


class Productions(Resource):
    def get(self):
        production_list = [p.to_dict() for p in Production.query.all()]
        response = make_response(
            production_list,
            200,
        )

        return response

    def post(self):
        req_json = request.get_json()
        new_production = Production(
            title=req_json["title"],
            genre=req_json["genre"],
            budget=int(req_json["budget"]),
            image=req_json["image"],
            director=req_json["director"],
            description=req_json["description"],
            ongoing=bool(req_json["ongoing"]),
        )

        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        response = make_response(
            response_dict,
            201,
        )
        return response


api.add_resource(Productions, "/productions")


class ProductionByID(Resource):
    def get(self, id):
        production = Production.query.filter_by(id=id).first()
        # 3.✅ If a production is not found raise the NotFound exception
        # 3.1 AND/OR use abort() to create a 404 with a customized error message
        if not production:
            # abort(404)
            raise NotFound

        production_dict = production.to_dict()
        response = make_response(production_dict, 200)

        return response

    # 4.✅ Patch
    # 4.1 Create a patch method that takes self and id
    def patch(self, id):
        # 4.2 Query the Production from the id
        production = db.session.get(Production, id)
        # 4.3 If the production is not found raise the NotFound exception AND/OR use abort() to create a 404 with a customized error message
        if not production:
            raise NotFound
        # 4.4 Loop through the request.json object and update the productions attributes. Note: Be cautions of the data types to avoid errors.
        form_json = request.get_json()
        for key, value in form_json.items():
            setattr(production, key, value)
        # 4.5 add and commit the updated production
        db.session.add(production)
        db.session.commit()
        # 4.6 Create and return the response
        return make_response(production.to_dict(), 202)

    # 5.✅ Delete
    # 5.1 Create a delete method, pass it self and the id
    def delete(self, id):

        # 5.2 Query the Production
        production = db.session.get(Production, id)
        # 5.3 If the production is not found raise the NotFound exception AND/OR use abort() to create a 404 with a customized error message
        if not production:
            raise NotFound
        # 5.4 delete the production and commit
        db.session.delete(production)
        db.session.commit()
        # 5.5 create a response with the status of 204 and return the response
        return make_response("", 204)


api.add_resource(ProductionByID, "/productions/<int:id>")


class CastMembers(Resource):
    def get(self):
        members = [
            member.to_dict(
                rules=(
                    "-production.budget",
                    "-production.ongoing",
                    "-production.created_at",
                    "-production.updated_at",
                )
            )
            for member in CastMember.query.all()
        ]
        return make_response(members, 200)

    def post(self):
        # new_member = CastMember(
        #     name=request.get_json()["name"],
        #     role=request.get_json()["role"],
        #     production_id=request.get_json()["production_id"],
        # )
        member_json = request.get_json()
        """we can do mass assignment with a post request
        with mass assignment, it is crucial that the keys of the request body json all match exactly with properties of the model object"""
        # new_member = CastMember()
        # for key, value in member_json.items():
        #     setattr(new_member, key, value)
        new_member = CastMember(**member_json)
        db.session.add(new_member)
        db.session.commit()
        return make_response(new_member.to_dict(), 201)


class CastMemberById(Resource):
    def get(self, id):
        member = db.session.get(CastMember, id)
        if not member:
            raise NotFound
        return make_response(member.to_dict(), 200)


api.add_resource(CastMembers, "/cast_members")
api.add_resource(CastMemberById, "/cast_members/<int:id>")


# 2.✅ use the @app.errorhandler() decorator to handle Not Found
# 2.1 Create the decorator and pass it NotFound
@app.errorhandler(NotFound)
def handle_not_found(e):
    return make_response(
        f"Not found: Sorry the {request.path.strip('/1234567890').title()} resource you are looking for doesn't exist",
        404,
    )


# 2.2 Use make_response to create a response with a message and the status 404
# 2.3 return the response

app.register_error_handler(404, handle_not_found)


# To run the file as a script
if __name__ == "__main__":
    app.run(port=5555, debug=True)
