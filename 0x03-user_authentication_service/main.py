#!/usr/bin/env python3
"""
Main file
"""

from db import DB
from user import User

my_db = DB()

# Test Case 1: Adding a valid user
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
assert user_1.id is not None, "User ID should not be None"
print("\nTest Case 1: User added successfully - ID: \n", user_1.id)

# Test Case 2: Adding another valid user
user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
assert user_2.id is not None, "User ID should not be None"
print("\nTest Case 2: Another user added successfully - ID: \n", user_2.id)

# Test Case 3: Adding a user with an empty email (should raise IntegrityError)
try:
    invalid_user = my_db.add_user("", "InvalidHashedPwd")
    print("\nTest Case 3: Unexpected - Empty email should raise IntegrityError\n")
except Exception as e:
    print("\nTest Case 3: Expected -\n", e)

# Test Case 4: Adding a user with an empty password (should raise IntegrityError)
try:
    invalid_user = my_db.add_user("invalid@test.com", "")
    print("\nTest Case 4: Unexpected - Empty password should raise IntegrityError\n")
except Exception as e:
    print("\nTest Case 4: Expected -\n", e)
