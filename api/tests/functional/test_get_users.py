#!/usr/bin/env python3
"""
Test cases for the '/users/all' view function
"""
from api.Models.tables import User
url = '/api/users/all/'


def test_get_no_users(client, db, access_token):
    """
    GIVEN: an api configured for testing
    WHEN: the '/users/all/' receives request with no db
    THEN: Check fails with expected error code
    """
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get(url, headers=headers)

    # print(f"Response status code: {response.status_code}")
    # print(f"Response data: {response.data}")
    data = response.get_json()
    assert response.status_code and data['statusCode'] == 404
    assert data['status'] == 'Not Found'
    assert data['message'] == 'No Data Found'


def test_get_users(client, db, access_token):
    """
    GIVEN: an api configured for testing
    WHEN: the '/users/all' receives a valid req with data in the DB
    THEN: Check that response is total no of items in DB with correct return statements
    """
    # Add Users to the DB
    User1 = client.post('/auth/register', json={
        "userId": "45", "firstName": "John", "lastName": "Doe",
        "email": "john@example.com", "password": "hh34thf",
        "phone": "1234567890"
    })
    user2 = client.post('/auth/register', json={
        "userId": "78", "firstName": "Jane", "lastName": "Smith",
        "email": "jane@example.com", "password": "hh34thf",
        "phone": "0987654321"
    })

    # Construct the request & verify the response returned
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get(url, headers=headers)

    data = response.get_json()
    assert response.status_code == 200
    assert data['statusCode'] == 200
    assert data['status'] == 'success'
    assert data['message'] == 'Data Retrieved'
