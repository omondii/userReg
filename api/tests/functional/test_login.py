#!/usr/bin/env python3
"""
Pytest functional tests for the login view
"""

url = '/auth/login'


def test_login(client, db):
    """
    GIVEN: an api configured for functional testing
    WHEN: the '/login' route receives a POST with correct details
    THEN: Check that the user is logged in and expected response is received
    """
    register = client.post('/auth/register', json={
        'userId': '5',
        'firstName': 'Tester',
        'lastName': 'Log',
        'email': 'log2@gmail.com',
        'password': 'test2',
        'phone': '234734555433'
    })
    assert register.status_code == 201

    login = client.post(url, json={
        'email': 'log2@gmail.com',
        'password': 'test2'
    })
    assert login.status_code == 200
    data = login.get_json()
    assert 'accessToken' in data['data']
    assert data['message'] == 'Login successful'


def test_wrong_pass(client, db):
    """
    GIVEN: an api configured for functional testing
    WHEN: the '/login' route receives a POST with wrong pass
    THEN: Check that the login attempt fails & it returns the expected response
    """
    register = client.post('/auth/register', json={
        'userId': '6',
        'firstName': 'Tester',
        'lastName': 'Wrong',
        'email': 'Nomail@gmail.com',
        'password': 'test23',
        'phone': '23423454433'
    })
    assert register.status_code == 201

    login = client.post(url, json={
        'email': 'Nomail@gmail.com',
        'password': 'test2'
    })
    assert login.status_code == 401
    data = login.get_json()
    assert data['status'] == 'Bad request'
    assert data['message'] == 'Authentication failed'


def test_missing_param(client, db):
    """
    GIVEN: an api configured for functional testing
    WHEN: the '/login' route receives a POST with missing parameters
    THEN: Check that the login attempt fails & it returns the expected response
    """
    register = client.post('/auth/register', json={
        'userId': '7',
        'firstName': 'Nopass',
        'lastName': 'Wrong',
        'email': 'pass1@gmail.com',
        'password': 'test23',
        'phone': '234234245433'
    })
    assert register.status_code == 201

    login = client.post(url, json={
        'email': 'Nomail@gmail.com',
    })
    assert login.status_code == 400
    data = login.get_json()
    assert data['status'] == 'Bad request'
    assert data['message'] == 'Missing required filed/s'
