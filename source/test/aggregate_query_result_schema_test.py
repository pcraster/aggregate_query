import datetime
import unittest
import uuid
from emis_aggregate_query import create_app
from emis_aggregate_query.api.schema import *


class AggregateQueryResultSchemaTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()
        self.schema = AggregateQueryResultSchema()


    def tearDown(self):
        self.schema = None

        self.app_context.pop()


    def test_empty1(self):
        client_data = {
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
            "_schema": ["Input data must have a aggregate_query_result key"]
        })


    def test_empty2(self):
        client_data = {
                "aggregate_query_result": {}
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "id": ["Missing data for required field."],
                "uri": ["Missing data for required field."]
            })


    def test_invalid_id(self):
        client_data = {
                "aggregate_query_result": {
                    "id": "blah",
                    "uri": "blih"
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "id": ["Not a valid UUID."]
            })


    def test_empty_uri(self):
        client_data = {
                "aggregate_query_result": {
                    "id": uuid.uuid4(),
                    "uri": ""
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertTrue(errors)
        self.assertEqual(errors, {
                "uri": ["Shorter than minimum length 1."]
            })


    def test_use_case1(self):
        query_id = uuid.uuid4()

        client_data = {
                "aggregate_query_result": {
                    "id": query_id,
                    "uri": "/blah.csv"
                }
            }
        data, errors = self.schema.load(client_data)

        self.assertFalse(errors)

        self.assertTrue(hasattr(data, "id"))
        self.assertTrue(isinstance(data.id, uuid.UUID))
        self.assertEqual(data.id, query_id)

        self.assertTrue(hasattr(data, "uri"))
        self.assertEqual(data.uri, "/blah.csv")

        self.assertTrue(hasattr(data, "posted_at"))
        self.assertTrue(isinstance(data.posted_at, datetime.datetime))


        data, errors = self.schema.dump(data)

        self.assertFalse(errors)
        self.assertTrue("aggregate_query_result" in data)

        result = data["aggregate_query_result"]

        self.assertTrue("id" in result)
        self.assertEqual(result["id"], str(query_id))

        self.assertTrue("uri" in result)
        self.assertEqual(result["uri"], "/blah.csv")

        self.assertTrue("posted_at" not in result)

        self.assertTrue("_links" in result)

        links = result["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


if __name__ == "__main__":
    unittest.main()
