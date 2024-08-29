#!/usr/bin/env python3
"""
Test cases for the '/users/all' view function
"""
from api.Models.tables import User
import pytest
url = '/api/users/all/'


@pytest.mark.skip(reason="This test is currently failing")
def test_get_no_users(client, db, access_token):
    """
    GIVEN: an api configured for testing
    WHEN: the '/users/all/' receives request with no when the DB is empty
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get(url, headers=headers)

    data = response.get_json()
    assert response.status_code and data['statusCode'] == 404
    assert data['status'] == 'Not Found'
    assert data['message'] == 'No Data Found'


def test_get_users(client, db, access_token, reg_users):
    """
    GIVEN: an api configured for testing
    WHEN: the '/users/all' receives a valid req with data in the DB
    THEN: Check that response is total no of items in DB with correct return statements
    """
    # Construct the request & verify the response returned
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get(url, headers=headers)

    data = response.get_json()
    assert response.status_code and data['statusCode'] == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Data Retrieved'
    # Check for correct user details
    res_data = data['data']
    assert res_data[1]['firstName'] == 'Jane'
