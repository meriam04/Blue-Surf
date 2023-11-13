from ..app import app, db
from ..models import User, Event, Tag, event_tags
from .abstract import DataLayer

from datetime import datetime
import logging
from sqlalchemy import or_, and_, func
from PIL import Image
import io

"""
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    is_published = db.Column(db.Boolean, nullable=False, default=False)
    like_count = db.Column(db.Integer, default=0)
    image = db.Column(db.LargeBinary, nullable=True)
    club = db.Column(db.Text)
"""


class EventDataLayer(DataLayer):
    def helper_valid_times(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Given a start and end time, it returns whether both are valid.
        This means that:
        - start_time and end_time are not None
        - they are both valid datetime objects
        - start_time is before end_time
        """
        if start_time is None or end_time is None:
            return False
        try:
            start = datetime(start_time)
            end = datetime(end_time)
        except Exception as e:
            raise e

        if end < start:
            return False

        return True

    def create_event(
        self,
        title,
        description,
        extended_description,
        location,
        start_time,
        end_time,
        author_id,
        is_published,
        club,
        image=None,
        tags=None,
    ):
        """
        Creates an event with the given parameters and adds it to the database.
        Returns the id of the event.
        """
        event = Event()

        if title is None or len(title) == 0:
            logging.info(f"Title {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Title {self.SHOULD_NOT_BE_EMPTY}")
        if len(title) > 255:
            logging.info(f"Title {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
            raise ValueError(f"Title {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
        event.title = title

        # TODO: Implement some checks for description?
        event.description = description

        # TODO: Implement some checks for extended description?
        event.extended_description = extended_description

        if location is None or len(location) == 0:
            logging.info(f"Location {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Location {self.SHOULD_NOT_BE_EMPTY}")
        if len(location) > 255:
            logging.info(f"Location {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
            raise ValueError(f"Location {self.SHOULD_BE_LESS_THAN_255_CHARACTERS}")
        event.location = location

        if start_time is None:
            logging.info(f"Start time {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"Start time {self.SHOULD_NOT_BE_EMPTY}")
        try:
            temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
            raise ValueError(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

        if end_time is None:
            logging.info(f"End time {self.SHOULD_NOT_BE_EMPTY}")
            raise TypeError(f"End time {self.SHOULD_NOT_BE_EMPTY}")
        try:
            temp_end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logging.info(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
            raise ValueError(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

        if temp_end_datetime < temp_start_datetime:
            logging.info("Start time should be after end time")
            raise ValueError("Start time should be after end time")
        event.start_time = temp_start_datetime
        event.end_time = temp_end_datetime

        # TODO: Implement some checks for club?
        event.club = club

        with app.app_context():
            author = User.query.filter_by(id=author_id).first()
            if author is None:
                logging.info(f"User {author_id} {self.UNABLE_TO_POST}")
                raise TypeError(f"User {author_id} {self.UNABLE_TO_POST}")
            event.author_id = author.id

            if is_published is None:
                logging.info(f"Event {self.WAS_NOT_PUBLISHED}")
                raise TypeError(f"Event {self.WAS_NOT_PUBLISHED}")
            event.is_published = is_published

            if image is not None:
                try:
                    Image.open(io.BytesIO(image))
                    event.image = image

                except Exception as e:
                    logging.info(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
                    raise TypeError(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

            # Add the event to the database
            db.session.add(event)
            db.session.commit()

            # Associate tags with the event
            logging.warning(f"Tags is {tags}")

            event.tags = []
            if tags:
                for tag_name in tags:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag is not None:
                        event.tags.append(tag)

            # Commit the changes to the session after adding tags
            db.session.commit()
            return event.id

    def get_search_results_by_keyword(self, keyword):
        keyword_word_pattern = "% {}%".format(keyword)
        keyword_start_pattern = "{}%".format(keyword)
        with app.app_context():
            query = Event.query.filter(
                or_(
                    Event.title.ilike(keyword_word_pattern),
                    Event.club.ilike(keyword_word_pattern),
                    Event.title.ilike(keyword_start_pattern),
                    Event.club.ilike(keyword_start_pattern),
                )
            )
            results = query.all()
            return results

    def update_event(
        self,
        event_id,
        title,
        description,
        extended_description,
        location,
        tags=[],
        image=None,
        is_published=True,
        start_time=None,
        end_time=None,
    ):
        # get the event by event_id
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event is None:
                logging.info(f"Event with id {event_id} does not exist")
                raise ValueError(f"Event with id {event_id} does not exist")

            # UPDATE event in db
            if title is None or len(title) == 0:
                logging.info("Title should not be empty")
                raise TypeError("Title should not be empty")
            if len(title) > 255:
                logging.info("Title should be under 255 characters")
                raise ValueError("Title should be under 255 characters")
            event.title = title

            # TODO: Implement some checks for description?
            event.description = description
            event.extended_description = extended_description

            if location is None or len(location) == 0:
                logging.info("Location should not be empty")
                raise TypeError("Location should not be empty")
            if len(location) > 255:
                logging.info("Location should be under 255 characters")
                raise ValueError("Location should be under 255 characters")
            event.location = location

            event.tags = []
            if tags:
                for tag_name in tags:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag is not None:
                        event.tags.append(tag)

            if image is not None:
                try:
                    Image.open(io.BytesIO(image))
                    event.image = image

                except Exception as e:
                    logging.info(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
                    raise TypeError(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

            db.session.commit()
            try:
                valid_times = self.helper_valid_times(start_time, end_time)
            except Exception as e:
                raise ValueError(e)

            if valid_times:
                event.start_time = start_time
                event.end_time = end_time
            db.session.commit()

            # temp_start_datetime = None
            # temp_end_datetime = None

            # if start_time is not None:
            #     try:
            #         temp_start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            #     except ValueError as e:
            #         logging.info(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")
            #         raise ValueError(f"Start time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")

            # if end_time is not None:
            #     try:
            #         temp_end_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            #     except ValueError as e:
            #         logging.info(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")
            #         raise ValueError(f"End time {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}, {e}")

            # if temp_end_datetime < temp_start_datetime:
            #     logging.info("Start time should be after end time")
            #     raise ValueError("Start time should be after end time")

            # if temp_start_datetime is not None:
            #     logging.warning(type(temp_start_datetime))
            #     event.start_time = temp_start_datetime
            # if temp_end_datetime is not None:
            #     logging.warning(type(temp_start_datetime))
            #     event.end_time = temp_end_datetime

            db.session.commit()

        # with app.app_context():
        #     author = User.query.filter_by(username=author_name).first()
        # if author is None:
        #     logging.info(f"Username {author_name} unable to post")
        #     raise TypeError(f"Username {author_name} unable to post")
        # event.author_id = author.id

        # if is_published is None:
        #     logging.info("Event was not published")
        #     raise TypeError("Event was not published")
        # event.is_published = is_published

    def get_all_events(self):
        """
        Returns all events.
        """
        with app.app_context():
            events = Event.query.all()
            return events

    def get_all_locations(self):
        with app.app_context():
            locations = (
                db.session.query(Event.location)
                .filter(Event.location != "")
                .distinct()
                .order_by(func.lower(Event.location))
                .all()
            )
            return [loc[0] for loc in locations]

    def get_all_clubs(self):
        with app.app_context():
            clubs = (
                db.session.query(Event.club)
                .filter(Event.club != "")
                .order_by(func.lower(Event.club))
                .distinct()
                .all()
            )
            return [club[0] for club in clubs]

    def get_events_by_tag(self, tag_name):
        with app.app_context():
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag is None:
                logging.info(f"Tag does not exist")
                raise ValueError(f"Tag does not exist")
            events = (
                Event.query.join(event_tags).join(Tag).filter(Tag.id == tag.id).all()
            )
            return events

    def get_event_by_id(self, id):
        """
        Returns the event with the given id.
        """
        with app.app_context():
            event = Event.query.filter_by(id=id).first()
            if event is None:
                logging.info(f"Event with id {id} {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event with id {id} {self.DOES_NOT_EXIST}")
            return event

    def delete_event_by_id(self, id):
        """
        Deletes the event with the given event id.
        """
        with app.app_context():
            event = Event.query.filter_by(id=id).first()
            if event is None:
                logging.info(f"Event with id {id} does not exist and cannot be deleted")
                raise ValueError(
                    f"Event with id {id} does not exist and cannot be deleted"
                )
            db.session.delete(event)
            db.session.commit()

    def get_authored_events(self, author_id):
        """
        Returns all events authored by the given author_id.
        """
        with app.app_context():
            events = Event.query.filter_by(author_id=author_id).all()
            if events is None:
                logging.info(f"Event with author_id {author_id} {self.DOES_NOT_EXIST}")
                raise ValueError(f"Event with id {author_id} {self.DOES_NOT_EXIST}")
            return events

    def get_tags_for_event(self, event_id):
        """
        Returns a list of Tag objects that are associated with the given event id.
        """
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if event.tags == None:
                return []
            return event.tags

    def update_image(self, event_id, image):
        with app.app_context():
            event = Event.query.filter_by(id=event_id).first()
            if image is not None:
                try:
                    # make sure the image can be opened (given in correct format)
                    Image.open(io.BytesIO(image))
                except Exception as e:
                    logging.info(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")
                    raise TypeError(f"Image {self.IS_NOT_GIVEN_IN_CORRECT_FORMAT}")

            event.image = image
            db.session.commit()

    def search_filter_sort(
        self,
        tag_name=None,
        location=None,
        club=None,
        start_time=None,
        end_time=None,
        keyword=None,
        sort_by=None,
    ):
        """
        Returns a list of Event objects based on the optional tag name, search keyword, and sort criteria.
        """

        with app.app_context():
            # Base query without any filters
            query = Event.query

            # Add search filters if keyword is provided
            if keyword is not None and len(keyword) > 0:
                keyword_word_pattern = "% {}%".format(keyword)
                keyword_start_pattern = "{}%".format(keyword)
                query = query.filter(
                    or_(
                        Event.title.ilike(keyword_word_pattern),
                        Event.club.ilike(keyword_word_pattern),
                        Event.title.ilike(keyword_start_pattern),
                        Event.club.ilike(keyword_start_pattern),
                    )
                )

            # Add tag filter if tag_name is provided
            if tag_name is not None and tag_name != "All":
                tag = Tag.query.filter_by(name=tag_name).first()
                # if a field doesn't exist, then the result will be empty
                if tag is None:
                    return []
                query = query.join(event_tags).join(Tag).filter(Tag.id == tag.id)

            if location is not None and len(location) > 0 and location != "All":
                query = query.filter(Event.location.ilike("%{}%".format(location)))

            if club is not None and len(club) > 0 and club != "All":
                query = query.filter(Event.club.ilike("%{}%".format(club)))

            if start_time is not None and end_time is not None:
                if " " in str(start_time) and " " in str(end_time):
                    start_datetime = (
                        datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                        if isinstance(start_time, str)
                        else start_time
                    )
                    end_datetime = (
                        datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
                        if isinstance(end_time, str)
                        else end_time
                    )
                    query = query.filter(
                        Event.start_time >= start_datetime,
                        Event.end_time <= end_datetime,
                    )
                else:
                    start_date = datetime.strptime(start_time, "%Y-%m-%d")
                    end_date = datetime.strptime(end_time, "%Y-%m-%d")
                    start_date = (
                        datetime.strptime(start_time, "%Y-%m-%d").date()
                        if isinstance(start_time, str)
                        else start_time.date()
                    )
                    end_date = (
                        datetime.strptime(end_time, "%Y-%m-%d").date()
                        if isinstance(end_time, str)
                        else end_time.date()
                    )
                    query = query.filter(
                        and_(
                            func.date(Event.start_time) >= start_date,
                            func.date(Event.end_time) <= end_date,
                        )
                    )
            elif start_time is not None and end_time is None:
                if " " in start_time:
                    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                    query = query.filter(Event.start_time == start_time)
                else:
                    start_date = datetime.strptime(start_time, "%Y-%m-%d")
                    query = query.filter(
                        func.date(Event.start_time) == func.date(start_date)
                    )

            # Add sorting logic if sortby is provided
            if sort_by == "alphabetical":
                query = query.order_by(func.lower(Event.title))
            elif sort_by == "start time":
                query = query.order_by(Event.start_time)
            elif sort_by == "trending":
                query = query.order_by(Event.like_count.desc())
            else:
                query = query.order_by(Event.id)

            # Execute the query and return the results
            results = query.all()
            return results
