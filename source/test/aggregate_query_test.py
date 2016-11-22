import os.path
import unittest
import uuid
from flask import current_app, json
from aggregate_query import create_app, db
from aggregate_query.api.schema import *


class AggregateQueryTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_aggregate_queries(self):
        payloads = [
                {
                    "model": "a = b + c"
                },
                {
                    "model": "a^2 = sqrt(b^2 + c^2)"
                }
            ]

        for payload in payloads:
            response = self.client.post("/aggregate_queries",
                data=json.dumps({"aggregate_query": payload}),
                content_type="application/json")
            data = response.data.decode("utf8")

            self.assertEqual(response.status_code, 200, "{}: {}".format(
                response.status_code, data))


    def test_get_aggregate_queries(self):
        response = self.client.get("/aggregate_queries")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_queries" in data)
        self.assertEqual(data["aggregate_queries"], [])

        self.post_aggregate_queries()

        response = self.client.get("/aggregate_queries")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_queries" in data)

        queries = data["aggregate_queries"]

        self.assertEqual(len(queries), 2)


    def test_get_aggregate_query(self):
        self.post_aggregate_queries()

        response = self.client.get("/aggregate_queries")
        data = response.data.decode("utf8")
        data = json.loads(data)
        queries = data["aggregate_queries"]
        query = queries[0]
        uri = query["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_query" in data)

        self.assertEqual(data["aggregate_query"], query)

        self.assertTrue("id" not in query)
        self.assertTrue("posted_at" not in query)

        self.assertTrue("model" in query)
        self.assertEqual(query["model"], "a = b + c")

        self.assertTrue("status" in query)
        self.assertEqual(query["status"], "draft")

        self.assertTrue("_links" in query)

        links = query["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_aggregate_query(self):
        self.post_aggregate_queries()

        response = self.client.get("/aggregate_queries")
        data = response.data.decode("utf8")
        data = json.loads(data)
        queries = data["aggregate_queries"]
        query = queries[0]
        uri = query["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_empty_aggregate_query(self):
        payload = {
            }
        response = self.client.post("/aggregate_queries",
            data=json.dumps({"aggregate_query": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

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


    def test_post_aggregate_query(self):
        payload = {
                "model": "a = b + c"
            }
        response = self.client.post("/aggregate_queries",
            data=json.dumps({"aggregate_query": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_query" in data)

        query = data["aggregate_query"]

        self.assertTrue("id" not in query)
        self.assertTrue("posted_at" not in query)

        self.assertTrue("model" in query)
        self.assertEqual(query["model"], "a = b + c")

        self.assertTrue("status" in query)
        self.assertEqual(query["status"], "draft")

        self.assertTrue("_links" in query)

        links = query["_links"]

        self.assertTrue("self" in links)
        self.assertTrue("collection" in links)


    def test_post_bad_request(self):
        response = self.client.post("/aggregate_queries")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/aggregate_queries",
            data=json.dumps({"aggregate_query": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
