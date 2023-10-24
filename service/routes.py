"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    location_url = url_for("get_accounts", account_id=account.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################

# ... place you code here to LIST accounts ...
@app.route("/accounts", methods=["GET"])
def get_accounts():
    """
    This endpoint will return the list of all accounts in the database
    """
    app.logger.info("Request to retrieve account list")
    check_content_type("application/json")
    account = Account()
    list_of_accounts = account.all()

    return make_response(
        jsonify(account_list =[acc.serialize() for acc in list_of_accounts]), status.HTTP_200_OK
    )



######################################################################
# READ AN ACCOUNT
######################################################################

# ... place you code here to READ an account ...
@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """
    This endpoint will return a detailed view of a specific account
    """
    app.logger.info("Request to retrieve specific account")
    check_content_type("application/json")
    account = Account()
    specific_account = account.find(account_id)
    if specific_account is None:
        abort(404, f"Account with ID {account_id} not found")

    serialized_account = specific_account.serialize()
    return make_response(
        jsonify(serialized_account), status.HTTP_200_OK
    )

######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################

# ... place you code here to UPDATE an account ...
@app.route("/accounts/<account_id>", methods=["PUT"])
def update_account(account_id):
    """
    This endpoint will update a specific account
    """
    app.logger.info("Request to update specific account")
    check_content_type("application/json")
    account = Account()
    specific_account = account.find(account_id)
    if specific_account is None:
        abort(404, f"Account with ID {account_id} not found")

    specific_account.deserialize(request.get_json())
    specific_account.update()
    message = specific_account.serialize()
    return make_response(
        jsonify(message), status.HTTP_200_OK
    )
    

######################################################################
# DELETE AN ACCOUNT
######################################################################

# ... place you code here to DELETE an account ...
@app.route("/accounts/<account_id>", methods=["DELETE"])
def delete_account(account_id):
    """
    This endpoint will delete a specific account
    """
    app.logger.info("Request to delete specific account")
    check_content_type("application/json")
    account = Account()
    specific_account = account.find(account_id)
    if specific_account is None:
        abort(404, f"Account with ID {account_id} not found")

    specific_account.delete()
    return make_response(
        jsonify(""), status.HTTP_204_NO_CONTENT
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
