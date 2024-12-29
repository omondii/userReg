#!/usr/bin/env python3
"""
Test cases for the get_user function.
FIXTURES:
Client: Test client
db: DB test object
access_token: JWT protected test object
reg_user:
"""


def test_get_wrong_user(client, db, access_token):
    """
    GIVEN: An api configured for testing
    WHEN: `url` receives a non-existent user id
    THEN: Check that user is correctly returned
    """
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/user/22', headers=headers)
    data = response.get_json()
    assert response.status_code and data['statusCode'] == 404
    assert data['message'] == 'User Not Found'


def test_existing_user(client, db, access_token, reg_users):
    """
    GIVEN: An api configured for testing
    WHEN: `url` receives a correct request with existing
    THEN: Check that user is
    """
    headers = {'Authorization': f'Bearer {access_token}'}

    response = client.get('/api/user/78', headers=headers)
    data = response.get_json()

    assert response.status_code and data['statusCode'] == 200
    assert data['message'] == 'Success'
    assert data['firstName'] == 'Jane'
