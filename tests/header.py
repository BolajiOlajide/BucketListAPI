"""
Set the headers to be sent when testing.

Contains functions that test_files use
"""
import base64


def create_api_headers(token):
    """
    Create the API header.

    This is going to be sent along with the request for verification.
    """
    auth_type = 'Basic ' + base64.b64encode(token + ":")

    return {
        'Authorization': auth_type,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
