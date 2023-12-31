import logging

from .test_datalayer import test_client

from ..app import app, db
from ..datalayer.user import UserDataLayer
from ..models import User


def test_user_creation(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None


def test_add_duplicate_username(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "Username testuser1 already exists"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None


def test_add_duplicate_email(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        user.create_user(
            username="testuser2",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "Email testuser1@example.com already exists"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None
        assert User.query.filter_by(username="testuser2").first() == None


def test_null_username(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username=None,
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Username should not be empty"

    with app.app_context():
        assert User.query.filter_by(username=None).first() == None


def test_null_email(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email=None,
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Email should not be empty"

    with app.app_context():
        assert User.query.filter_by(email=None).first() == None


def test_empty_username(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Username should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="").first() == None


def test_empty_email(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Email should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None


def test_null_password_hash(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash=None,
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Password_hash should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None


def test_empty_password_hash(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Password_hash should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None


def test_null_password_salt(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt=None,
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Password_salt should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None


def test_empty_password_salt(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert str(type_error) == "Password_salt should not be empty"

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None


def test_delete_user(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None

    try:
        user.delete_user_by_username("testuser1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() == None


def test_get_user(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testsalt",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None

    try:
        user_retrieved = user.get_user(user_identifier="testuser1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username=user_retrieved.username).first() != None

    try:
        user_retrieved = user.get_user(user_identifier="testuser1@example.com")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(email=user_retrieved.email).first() != None


def test_get_invalid_user(test_client):
    user = UserDataLayer()

    try:
        user.get_user(user_identifier="testuser1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "User with username/email testuser1 does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    try:
        user.get_user(user_identifier="testuser1@example.com")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert (
            str(value_error)
            == "User with username/email testuser1@example.com does not exist"
        )
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None


def test_get_user(test_client):
    user = UserDataLayer()
    try:
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testsalt",
        )
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username="testuser1").first() != None

    try:
        user_retrieved = user.get_user(user_identifier="testuser1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(username=user_retrieved.username).first() != None

    try:
        user_retrieved = user.get_user(user_identifier="testuser1@example.com")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    with app.app_context():
        assert User.query.filter_by(email=user_retrieved.email).first() != None


def test_get_invalid_user(test_client):
    user = UserDataLayer()

    try:
        user.get_user(user_identifier="testuser1")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "User with username/email testuser1 does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    try:
        user.get_user(user_identifier="testuser1@example.com")
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert (
            str(value_error)
            == "User with username/email testuser1@example.com does not exist"
        )
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None


def test_get_user_by_id(test_client):
    user = UserDataLayer()
    user.create_user(
        username="testuser1",
        email="testuser1@example.com",
        password_hash="testpassword",
        password_salt="testsalt",
    )
    try:
        user.get_user_by_id(id=2)
    except ValueError as value_error:
        logging.debug(f"Error: {value_error}")
        assert str(value_error) == "User with id 2 does not exist"
    except TypeError as type_error:
        logging.debug(f"Error: {type_error}")
        assert type_error == None

    try:
        user1 = user.get_user_by_id(id=1)
    except (ValueError, TypeError) as error:
        assert error == None
    assert user1.username == "testuser1"
