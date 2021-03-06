"""
    rest_apiserver.controllers.reviews
    ~~~~~~~~~~~~~~~~~

    APIs to approve Provision and Extension Requests. 

    :license: GPL-3.0, see LICENSE for more details.
"""

import logging
logger = logging.getLogger(__name__)
logger.info("Loaded " + __name__)

import json
from datetime import datetime, timedelta
from eve.utils import str_to_date, date_to_rfc1123
from bson.objectid import ObjectId
from rest_apiserver import app, redis_queue
from rest_apiserver.core.utils import toJSON, failure_resp, create_notification
from flask import jsonify, request, Response

@app.route('/'+app.config['API_VERSION']+'/approveProvisionRequest', methods=['POST'])
def approveProvisionRequest():
    """
    Route for approving or rejecting ```provisionRequest``` 

    Accepts ```{_id: <provision request id>, reviewd_by: <reviewer user id>, status: <"APPROVED"/"REJECTED">}``` 
    as request json argument
    """
    response = {}
    try:
        # Get request parameters and perform sanity check
        if not request.json:
            raise ValueError("Empty json body provided!!!")

        _id = request.json['_id'] if '_id' in request.json else None
        reviewed_by = request.json['reviewed_by'] if 'reviewed_by' in request.json else None
        status = request.json['status'] if 'status' in request.json else None
        logger.debug("_id: " + str(_id) + "   reviewed_by: " + str(reviewed_by) + "   status: " + str(status) )

        if not _id or not reviewed_by or not status in ["APPROVED","REJECTED"]: 
            raise ValueError("Must provide provisionRequest id, reviewer id and approval status!!!")

        # Update provision request 
        provisionRequests = app.data.driver.db['provisionRequests']
        query = { "_id": ObjectId(_id) }
        provision_request = provisionRequests.find_one(query, sort=[("_created", -1)])
        if not provision_request: raise ValueError("Provision Request does not exist")
        if provision_request['status'] not in [ 'REQUESTED' ]: 
            raise ValueError("Provision Request cannot be reviewed in " + str(provision_request['status']) + " state")
        update = {
            "$set":
            {
                "reviewed_by": ObjectId(reviewed_by),
                "status": str(status),
            }
        }
        ret = provisionRequests.update(query, update, upsert = False)
        logger.debug("provision request update response: " + str(ret))

        # Create response object
        response = {
            "status": str(status),
            "_id": str(provision_request['_id'])
        }
        
        # Create notification for developer (requester)
        create_notification(
            title = "Provision Request" + str(status), 
            description = "Your provision request " + str(provision_request["_id"]) + " has been " + str(status),
            user = provision_request["requested_by"]
        )
    except ValueError as e:
        return Response(toJSON(failure_resp(str(e), 400)), 400, mimetype='application/json')
    except Exception as e:
        return Response(toJSON(failure_resp(str(e), 500)), 500, mimetype='application/json')
    return Response(toJSON(response), 200, mimetype='application/json')


@app.route('/'+app.config['API_VERSION']+'/approveExtensionRequest', methods=['POST'])
def approveExtensionRequest():
    """ 
    Approve ```extensionRequest``` 

    Accepts ```{_id: <extension request id>, reviewd_by: <reviewer user id>, status: <"APPROVED"/"REJECTED">}``` 
    as request json argument
    """
    response = {}
    try:
        # Get request parameters and perform sanity check
        if not request.json:
            raise ValueError("Empty json body provided!!!")
        
        _id = request.json['_id'] if '_id' in request.json else None
        reviewed_by = request.json['reviewed_by'] if 'reviewed_by' in request.json else None
        status = request.json['status'] if 'status' in request.json else None
        logger.debug("_id: " + str(_id) + "   reviewed_by: " + str(reviewed_by) + "   status: " + str(status) )

        if not _id or not reviewed_by or not status in ["APPROVED","REJECTED"]: 
            raise ValueError("Must provide extensionRequest id, reviewer id and approval status!!!")

        # Get extension request
        extensionRequests = app.data.driver.db['extensionRequests']
        extension_query = { "_id": ObjectId(_id) }
        extension_request = extensionRequests.find_one(extension_query, sort=[("_created", -1)])
        if not extension_request: raise ValueError("Extension Request does not exist")
        if extension_request['status'] not in [ 'REQUESTED' ]: 
            raise ValueError("Provision Request cannot be reviewed in " + str(extension_request['status']) + " state")
        
        # Get provision request
        provisionRequests = app.data.driver.db['provisionRequests']
        provision_query = { "_id": ObjectId(extension_request['provision_request']) }
        provision_request = provisionRequests.find_one(provision_query, sort=[("_created", -1)])
        if not provision_request: raise ValueError("Provision Request does not exist")
        if provision_request['status'] not in [ 'APPROVED', 'INITIATED', 'DEPLOYED', 'EXPIRED' ]: 
            raise ValueError("Provision Request cannot be extended in state: " + str(provision_request['status']))
        
        # Update provision request if extension "APPROVED"
        if status == "APPROVED":
            # find new expiration time
            expires_by = str_to_date(provision_request['expires_by']) + timedelta(hours=extension_request['extend_by'])
            update = {
                "$set":
                {
                    "status": "EXTENDED",
                    "expires_by": expires_by
                }
            }
            ret = provisionRequests.update(provision_query, update, upsert = False)
            logger.debug("provision request update response: " + str(ret))

        # Update extension request
        update = {
            "$set":
            {
                "reviewed_by": ObjectId(reviewed_by),
                "status": status,
            }
        }
        ret = extensionRequests.update(extension_query, update, upsert = False) 
        logger.debug("extension request update response: " + str(ret))

        # Create response object
        response = {
            "status": status,
            "_id": str(provision_request['_id'])
        }
        
        # Create notification for developer (requester)
        create_notification(
            title = "Provision Request" + str(status),  
            description = "Your provision request " + str(provision_request["_id"]) + " has been " + str(status), 
            user = provision_request["requested_by"]
        )
    except ValueError as e:
        return Response(toJSON(failure_resp(str(e), 400)), 400, mimetype='application/json')
    except Exception as e:
        return Response(toJSON(failure_resp(str(e), 500)), 500, mimetype='application/json')
    return Response(toJSON(response), 200, mimetype='application/json')
