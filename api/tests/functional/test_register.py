#!/usr/bin/env python3
"""
Tests for the routes module:
pytest
"""
import pytest

url = '/auth/register'


def test_post_user(client, db):
    """
    GIVEN: an api configured for testing
    WHEN: the '/register' page receives a POST with the correct required data
    THEN: Check that user is created and correct output received
    """
    response = client.post(url, json={
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
    WHEN: the '/register' page receives a POST with missing user data
    THEN: Check that user registration fails with correct message
    """
    response = client.post(url, json={
        'userId': '2',
        'firstName': 'Test',
        'lastName': 'system',
        'email': 'tester1@gmail.com',
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'Bad request'
    assert data['message'] == 'All fields are required'


def test_post_same_data(client, db):
    """
    WHEN: an api configured for testing
    WHEN: the '/register' page with details of an existing user
    THEN: check that 2nd user registration fails with the correct message
    """
    response = client.post(url, json={
        'userId': '3',
        'firstName': 'Test',
        'lastName': 'wrong',
        'email': 'testwr@gmail.com',
        'password': 'testwrong',
        'phone': '254789767644'
    })

    response2 = client.post(url, json={
        'userId': '3',
        'firstName': 'Test',
        'lastName': 'wrong',
        'email': 'testwr@gmail.com',
        'password': 'testwrong',
        'phone': '25478979098'
    })
    assert response.status_code == 201
    assert response2.status_code == 400
    data = response2.get_json()
    assert data['status'] == 'Bad request'
    assert data['message'] == 'User exists!'
