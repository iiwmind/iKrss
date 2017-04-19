import unittest
from app.models import IkrssRole,IkrssUser,IkrssUserLog,Permission,AnonymousUser
class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = IkrssUser(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = IkrssUser(password='cat')

        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = IkrssUser(password='cat')

        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = IkrssUser(password='cat')

        u2 = IkrssUser(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        IkrssUser.insert_roles()

        u = IkrssUser(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.SEND))
        self.assertFalse(u.can(Permission.AUTOSEND))

    def test_anonymous_user(self):
        u = AnonymousUser()

        self.assertFalse(u.can(Permission.SEND))