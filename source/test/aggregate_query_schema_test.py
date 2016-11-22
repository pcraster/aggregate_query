import datetime
import unittest
from aggregate_query import create_app
from aggregate_query.api.schema import *


class AggregateQuerySchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AggregateQuerySchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty(self):
        client_data = {
                "aggregate_query": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)
        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(data.id is None)

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))

        self.assertTrue(hasattr(data, "model"))
        self.assertEqual(data.model, "")

        self.assertTrue(hasattr(data, "status"))
        self.assertEqual(data.status, "draft")

        data.id = 5
        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("aggregate_query" in data)

        query = data["aggregate_query"]

        self.assertTrue("id" not in query)
        self.assertTrue("posted_at" not in query)

        self.assertTrue("model" in query)
        self.assertEqual(query["model"], "")

        self.assertTrue("status" in query)
        self.assertEqual(query["status"], "draft")

        self.assertTrue("_links" in query)

        links = query["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)
