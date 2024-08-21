#!/usr/bin/env python3
"""
Tests for the routes module:
pytest
"""


def test_post_user(client, db):
    """
    GIVEN: an api configured for testing
    WHEN: the '/register' page receives a POST with the required data
    THEN: Check that user is created and correct output received
    """
    response = client.post('/auth/register', json={
        'userId': '2',
        'firstName': 'Test',
        'lastName': 'System',
        'email': 'Test2@gmail.com',
        'password': 'test2',
        'phone': '234788555433'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'accessToken' in data['data']
    assert data['message'] == 'Registration successful'


def test_post_user_omit(client, db):
    """
    GIVEN: an api configured for testing
    WHEN: the '/register' page receives a POST with missing data
    THEN: Check that user registration fails with correct message
    """
    response = client.post('/auth/register', json={
        'userId': '2',
        'firstName': 'Test',
        'lastName': 'system',
        'email': 'tester1@gmail.com',
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'Bad request'
    assert data['message'] == 'All fields are required'
