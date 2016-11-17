import unittest
# from emis.model import User


class UserModelTestCase(unittest.TestCase):

    pass

    # def test_password_setter(self):
    #     user = User("jan", password="cat")
    #     self.assertTrue(user.password_hash is not None)


    # def test_no_password_getter(self):
    #     user = User("jan", password="cat")
    #     with self.assertRaises(AttributeError):
    #         user.password


    # def test_password_verification(self):
    #     user = User("jan", password="cat")
    #     self.assertTrue(user.verify_password("cat"))
    #     self.assertFalse(user.verify_password("dog"))


    # def test_password_salts_are_random(self):
    #     user1 = User("jan", password="cat")
    #     user2 = User("kees", password="cat")
    #     print(user1, user1.password_hash)
    #     print(user2, user2.password_hash)
    #     self.assertTrue(user1.password_hash != user2.password_hash)


if __name__ == "__main__":
    unittest.main()
