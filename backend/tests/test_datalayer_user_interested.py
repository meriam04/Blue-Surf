import sys
import pytest
import logging

from .test_datalayer import test_client

sys.path.append("../")
from app import app, db
from datalayer_user_interested import UserInterestedLayer
from datalayer_user import UserDataLayer
from datalayer_event import EventDataLayer
from datalayer_tag import TagDataLayer
from models import User, Event, UserInterestedEvent

def test_user_interested_event(test_client):
    user = UserDataLayer()
    event = EventDataLayer()
    tag = TagDataLayer()

    try: 
        user.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password_hash="testpassword",
            password_salt="testpassword",
        )
        tag.add_tag("Tag 1")
        event.create_event(
            title="Event 1",
            description="Kickoff event 1 for club 1",
            location="Toronto",
            start_time="2023-10-03 3:30:00",
            end_time="2023-10-03 4:00:00",
            author_name='testuser1',
            is_published=True,
            image=None,
            tags=["Tag 1"]
        )
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None

    with app.app_context():
        event_exists = Event.query.filter_by(title='Event 1').first()
        assert event_exists is not None
        user_exists = User.query.filter_by(username='testuser1').first()
        assert user_exists is not None

    user_interested_event = UserInterestedLayer()
    try:
        user_interested_event.create_user_interested_by_id(user_id=user_exists.id, event_id=event_exists.id)
    except ValueError as value_error: 
        logging.debug(f'Error: {value_error}')
        assert value_error == None
    except TypeError as type_error:
        logging.debug(f'Error: {type_error}')
        assert type_error == None

    with app.app_context():
        assert UserInterestedEvent.query.filter_by(user_id=user_exists.id, event_id=event_exists.id).first() != None
        event_exists = Event.query.filter_by(title='Event 1').first()
        assert event_exists.like_count == 1
    



        



    
    