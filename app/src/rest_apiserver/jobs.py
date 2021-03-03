""" This module contains all the mocked consumer jobs """

def analyze_request(self, _id):
    """
    Analyzes the provision request, checks against the quota, 
    and adds remarks to the provision request for the reviewer.
    
    Parameters
    ----------
    _id : str
        id of provisionRequest
    """
    # get quota for user
    # if not found, get quota for user's role
    # calculate total 
    pass

def provision_resource(self, _id): 
    """
    Forks another process, builds the eksctl config from templates and runs eksctl and saves the log

    Parameters
    ----------
    _id : str
        id of provisionRequest
    """
    pass

def purge_resource(self, _id):
    """
    Purges the resources created in the provision request
    Parameters
    ----------
    _id : str
        id of provisionRequest
    """
    pass