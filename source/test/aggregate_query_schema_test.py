import datetime
import unittest
import uuid
from emis_aggregate_query import create_app
from emis_aggregate_query.api.schema import *


class AggregateQuerySchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app.config["TESTING"] = True

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AggregateQuerySchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
        }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a aggregate_query key"]
        })


    def test_empty2(self):
        client_data = {
                "aggregate_query": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "model": ["Missing data for required field."],
                "user": ["Missing data for required field."]
            })


    def test_invalid_user(self):
        client_data = {
                "aggregate_query": {
                    "user": "meh",
                    "model": {"meh": "mah"}
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "user": ["Not a valid UUID."]
            })


    def test_empty3(self):

        client_data = {
                "aggregate_query": {
                    "user": uuid.uuid4(),
                    "model": {"meh": "mah"}
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))

        self.assertTrue(hasattr(data, "user"))
        self.assertTrue(isinstance(data.user, uuid.UUID))

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        self.assertTrue(hasattr(data, "patched_at"))
        self.assertTrue(isinstance(data.patched_at, datetime.datetime))

        self.assertTrue(hasattr(data, "model"))
        self.assertTrue(isinstance(data.model, dict))
        self.assertEqual(data.model, {"meh": "mah"})

        self.assertTrue(hasattr(data, "edit_status"))
        self.assertEqual(data.edit_status, "draft")

        self.assertTrue(hasattr(data, "execute_status"))
        self.assertEqual(data.execute_status, "pending")

        data.id = uuid.uuid4()
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("aggregate_query" in data)

        query = data["aggregate_query"]

        self.assertTrue("id" in query)
        self.assertTrue("user" in query)
        self.assertTrue("posted_at" in query)
        self.assertTrue("patched_at" in query)

        self.assertTrue("model" in query)
        self.assertTrue(isinstance(query["model"], dict))
        self.assertEqual(query["model"], {"meh": "mah"})

        self.assertTrue("edit_status" in query)
        self.assertEqual(query["edit_status"], "draft")

        self.assertTrue("execute_status" in query)
        self.assertEqual(query["execute_status"], "pending")

        self.assertTrue("_links" in query)

        links = query["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_use_case1(self):
        user_id = uuid.uuid4()

        client_data = {
                "aggregate_query": {
                    "user": user_id,
                    "model": {"meh": "mah"},
                    "edit_status": "final",
                    "execute_status": "queued"
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))
        id = data.id

        self.assertTrue(hasattr(data, "user"))
        self.assertTrue(isinstance(data.user, uuid.UUID))
        self.assertEqual(data.user, user_id)

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        self.assertTrue(hasattr(data, "patched_at"))
        self.assertTrue(isinstance(data.patched_at, datetime.datetime))

        self.assertTrue(hasattr(data, "model"))
        self.assertEqual(data.model, {"meh": "mah"})

        self.assertTrue(hasattr(data, "edit_status"))
        self.assertEqual(data.edit_status, "final")

        self.assertTrue(hasattr(data, "execute_status"))
        self.assertEqual(data.execute_status, "queued")

        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("aggregate_query" in data)

        query = data["aggregate_query"]

        self.assertTrue("id" in query)
        self.assertEqual(query["id"], str(id))

        self.assertTrue("user" in query)
        self.assertEqual(query["user"], str(user_id))

        self.assertTrue("posted_at" in query)
        self.assertTrue("patched_at" in query)

        self.assertTrue("model" in query)
        self.assertEqual(query["model"], {"meh": "mah"})

        self.assertTrue("edit_status" in query)
        self.assertEqual(query["edit_status"], "final")

        self.assertTrue("execute_status" in query)
        self.assertEqual(query["execute_status"], "queued")

        self.assertTrue("_links" in query)

        links = query["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
