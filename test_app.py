import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app, setup_db, User


class RoomeeTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app.secret_key = os.environ.get('SECRET_KEY', 'secret')
        self.username = 'postgres'
        self.password = 'password'
        self.database_name = "roomee_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.username, self.password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test db content read, insert, update and delete
    """
    def test_create_user(self):
        new_user = User(
                first_name='test',
                last_name='user',
                phone_num='000',
                address='Yola',
                email='test@user.com',
                password='password',
                hotel_id=None,
                role_id=None
        )
        new_user.insert()
        user_from_db = User.query.filter_by(first_name='test').first()

        self.assertEqual(user_from_db.phone_num, '000')


    def test_update_user(self):
        existing_user = User.query.filter_by(first_name='test').first()
        existing_user.address = 'test country'
        existing_user.update()

        user_data_from_db = User.query.filter_by(first_name='test').first()

        self.assertEqual(user_data_from_db.address, 'test country')


    def test_delete_user(self):
        new_user = User(
                first_name='test',
                last_name='delete',
                phone_num='000',
                address='Yola',
                email='test@user.com',
                password='password',
                hotel_id=None,
                role_id=None
        )
        new_user.insert()

        user_from_db = User.query.filter_by(last_name='delete').first()
        self.assertEqual(user_from_db.last_name, 'delete')

        user_from_db.delete()
        user_data_from_db = User.query.filter_by(last_name='delete').first()
        self.assertEqual(user_data_from_db, None)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()