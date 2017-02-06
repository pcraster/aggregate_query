import datetime
import unittest
import uuid
from emis_aggregate_query import create_app
from emis_aggregate_query.api.schema import *


class AggregateQueryMessageSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AggregateQueryMessageSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a aggregate_query_message key"]
        })


    def test_empty2(self):
        client_data = {
                "aggregate_query_message": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "id": ["Missing data for required field."],
                "message": ["Missing data for required field."]
            })


    def test_invalid_id(self):
        client_data = {
                "aggregate_query_message": {
                    "id": "blah",
                    "message": "blih"
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "id": ["Not a valid UUID."]
            })


    def test_empty_message(self):
        client_data = {
                "aggregate_query_message": {
                    "id": uuid.uuid4(),
                    "message": ""
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "message": ["Shorter than minimum length 1."]
            })


    def test_use_case1(self):
        query_id = uuid.uuid4()

        client_data = {
                "aggregate_query_message": {
                    "id": query_id,
                    "message": "Something went very wrong"
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))
        self.assertEqual(data.id, query_id)

        self.assertTrue(hasattr(data, "message"))
        self.assertEqual(data.message, "Something went very wrong")

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))


        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("aggregate_query_message" in data)

        message = data["aggregate_query_message"]

        self.assertTrue("id" in message)
        self.assertEqual(message["id"], str(query_id))

        self.assertTrue("message" in message)
        self.assertEqual(message["message"], "Something went very wrong")

        self.assertTrue("posted_at" not in message)

        self.assertTrue("_links" in message)

        links = message["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
