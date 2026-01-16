"""
Student Management System - API Test Script

This script demonstrates how to interact with the Student Management System API
using Python's requests library.

Usage:
    python test_api.py

Make sure:
1. The Django server is running (python manage.py runserver)
2. You have created a superuser account
3. Update USERNAME and PASSWORD below with your credentials
"""

import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"
USERNAME = "admin"  # Change this to your username
PASSWORD = "admin"  # Change this to your password

# Create authentication object
auth = HTTPBasicAuth(USERNAME, PASSWORD)


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def test_list_students():
    """Test: List all students"""
    response = requests.get(f"{BASE_URL}/students/", auth=auth)
    print_response("LIST ALL STUDENTS", response)
    return response


def test_create_student():
    """Test: Create a new student"""
    new_student = {
        "name": "API Test Student",
        "email": f"apitest{requests.get(f'{BASE_URL}/students/', auth=auth).json()['count']}@example.com",
        "phone": "9999999999",
        "course": "API Testing",
        "date_of_joining": "2026-01-15"
    }
    
    response = requests.post(
        f"{BASE_URL}/students/",
        json=new_student,
        auth=auth
    )
    print_response("CREATE STUDENT", response)
    return response


def test_get_student(student_id):
    """Test: Get student details"""
    response = requests.get(f"{BASE_URL}/students/{student_id}/", auth=auth)
    print_response(f"GET STUDENT (ID: {student_id})", response)
    return response


def test_update_student(student_id):
    """Test: Update student (partial)"""
    update_data = {
        "phone": "8888888888"
    }
    
    response = requests.patch(
        f"{BASE_URL}/students/{student_id}/",
        json=update_data,
        auth=auth
    )
    print_response(f"UPDATE STUDENT (ID: {student_id})", response)
    return response


def test_search_students():
    """Test: Search students"""
    response = requests.get(
        f"{BASE_URL}/students/",
        params={"search": "API"},
        auth=auth
    )
    print_response("SEARCH STUDENTS (query: 'API')", response)
    return response


def test_filter_by_course():
    """Test: Filter students by course"""
    response = requests.get(
        f"{BASE_URL}/students/",
        params={"course": "API Testing"},
        auth=auth
    )
    print_response("FILTER BY COURSE (course: 'API Testing')", response)
    return response


def test_statistics():
    """Test: Get statistics"""
    response = requests.get(f"{BASE_URL}/students/statistics/", auth=auth)
    print_response("GET STATISTICS", response)
    return response


def test_bulk_create():
    """Test: Bulk create students"""
    bulk_data = {
        "students": [
            {
                "name": "Bulk Student 1",
                "email": "bulk1@example.com",
                "phone": "1111111111",
                "course": "Bulk Testing",
                "date_of_joining": "2026-01-15"
            },
            {
                "name": "Bulk Student 2",
                "email": "bulk2@example.com",
                "phone": "2222222222",
                "course": "Bulk Testing",
                "date_of_joining": "2026-01-15"
            }
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/students/bulk_create/",
        json=bulk_data,
        auth=auth
    )
    print_response("BULK CREATE STUDENTS", response)
    return response


def test_delete_student(student_id):
    """Test: Delete student"""
    response = requests.delete(f"{BASE_URL}/students/{student_id}/", auth=auth)
    print_response(f"DELETE STUDENT (ID: {student_id})", response)
    return response


def main():
    """Run all API tests"""
    print("\n" + "="*60)
    print("STUDENT MANAGEMENT SYSTEM - API TESTS")
    print("="*60)
    
    try:
        # Test 1: List students
        test_list_students()
        
        # Test 2: Create a student
        create_response = test_create_student()
        if create_response.status_code == 201:
            student_id = create_response.json()['id']
            
            # Test 3: Get student details
            test_get_student(student_id)
            
            # Test 4: Update student
            test_update_student(student_id)
            
            # Test 5: Get updated student
            test_get_student(student_id)
        
        # Test 6: Search students
        test_search_students()
        
        # Test 7: Filter by course
        test_filter_by_course()
        
        # Test 8: Get statistics
        test_statistics()
        
        # Test 9: Bulk create (commented out to avoid cluttering database)
        # test_bulk_create()
        
        # Test 10: Delete student (commented out to preserve test data)
        # if create_response.status_code == 201:
        #     test_delete_student(student_id)
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60)
        print("\nNote: Some tests are commented out to preserve data.")
        print("Uncomment them in the script to test delete and bulk operations.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Make sure the Django server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    main()
