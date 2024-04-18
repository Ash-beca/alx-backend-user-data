#!/usr/bin/env python3
from models.user import User
from models.user_session import UserSession

# Load all users from file storage
User.load_from_file()
UserSession.load_from_file()
