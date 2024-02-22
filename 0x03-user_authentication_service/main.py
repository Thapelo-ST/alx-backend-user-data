#!/usr/bin/env python3
"""
Main file
"""
from db import DB
from user import User

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

my_db = DB()

# Test Case 1: Valid user
user = my_db.add_user("test@test.com", "PwdHashed")
print(user.id)
print("\n user Added!! \n")

find_user = my_db.find_user_by(email="test@test.com")
print(find_user.id)
print("\n Test case {} done !! \n".format(1))

# Test Case 2: User not found
try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")
print("\n Test case {} done !! \n".format(2))

# Test Case 3: Invalid query argument
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
print("\n Test case {} done !! \n".format(3))

# Additional Test Cases:

# Test Case 4: Multiple valid users with the same email (should raise InvalidRequestError)
my_db.add_user("duplicate@test.com", "PwdHashed1")
my_db.add_user("duplicate@test.com", "PwdHashed2")
try:
    find_user = my_db.find_user_by(email="duplicate@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
print("\n Test case {} done !! \n".format(4))

# Test Case 5: Invalid query with additional arguments (should raise InvalidRequestError)
try:
    find_user = my_db.find_user_by(email="test@test.com", invalid_arg="test")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
print("\n Test case {} done !! \n".format(5))

# Test Case 6: Invalid query with no arguments
try:
    find_user = my_db.find_user_by()
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
print("\n Test case {} done !! \n".format(6))

# Test Case 7: Invalid query with unknown attribute
try:
    find_user = my_db.find_user_by(invalid_attr="test")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")
print("\n Test case {} done !! \n".format(7))

# Test Case 8: User not found with valid query
try:
    find_user = my_db.find_user_by(email="nonexistent@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not found")
print("\n Test case {} done !! \n".format(8))

# Test Case 9: User not found with invalid query attribute
try:
    find_user = my_db.find_user_by(invalid_attr="test")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid query attribute")
except NoResultFound:
    print("Not found")
print("\n Test case {} done !! \n".format(9))