import os.path
import unittest
import uuid
from flask import current_app, json
from emis_aggregate_query import create_app, db
from emis_aggregate_query.api.schema import *


class AggregateQueryMessageTestCase(unittest.TestCase):


    def setUp(self):
        self.app = create_app("test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        self.query1 = uuid.uuid4()
        self.query2 = uuid.uuid4()
        self.query3 = uuid.uuid4()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def post_aggregate_query_messages(self):

        # query1
        # query2
        # query3
        payloads = [
                {
                    "id": self.query1,
                    "message": "Error 1"
                },
                {
                    "id": self.query2,
                    "message": "Error 2"
                },
                {
                    "id": self.query3,
                    "message": "Error 3"
                },
            ]

        for payload in payloads:
            response = self.client.post("/aggregate_query_messages",
                data=json.dumps({"aggregate_query_message": payload}),
                content_type="application/json")
            data = response.data.decode("utf8")

            self.assertEqual(response.status_code, 201, "{}: {}".format(
                response.status_code, data))

    # def do_test_get_aggregate_queries_by_user(self,
    #         user_id,
    #         nr_messages_required):

    #     self.post_aggregate_query_messages()

    #     response = self.client.get("/aggregate_query_messages/{}".format(user_id))
    #     data = response.data.decode("utf8")

    #     self.assertEqual(response.status_code, 200, "{}: {}".format(
    #         response.status_code, data))

    #     data = json.loads(data)

    #     self.assertTrue("aggregate_query_messages" in data)

    #     messages = data["aggregate_query_messages"]

    #     self.assertEqual(len(messages), nr_messages_required)


    # def test_get_aggregate_queries_by_user1(self):
    #     self.do_test_get_aggregate_queries_by_user(self.query1, 2)


    # def test_get_aggregate_queries_by_user2(self):
    #     self.do_test_get_aggregate_queries_by_user(self.query2, 1)


    # def test_get_aggregate_queries_by_user3(self):
    #     self.do_test_get_aggregate_queries_by_user(self.query3, 0)


    def test_get_all_aggregate_query_messages1(self):
        # No messages posted.
        response = self.client.get("/aggregate_query_messages")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_query_messages" in data)
        self.assertEqual(data["aggregate_query_messages"], [])


    def test_get_all_aggregate_query_messages2(self):
        # Some messages posted.
        self.post_aggregate_query_messages()

        response = self.client.get("/aggregate_query_messages")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_query_messages" in data)

        messages = data["aggregate_query_messages"]

        self.assertEqual(len(messages), 3)


    def test_get_aggregate_query_message(self):
        self.post_aggregate_query_messages()

        response = self.client.get("/aggregate_query_messages")
        data = response.data.decode("utf8")
        data = json.loads(data)
        messages = data["aggregate_query_messages"]
        message = messages[0]
        uri = message["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")
        uri = message["_links"]["self"]
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 200, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("aggregate_query_message" in data)

        self.assertEqual(data["aggregate_query_message"], message)

        self.assertTrue("id" in message)
        self.assertEqual(message["id"], str(self.query1))

        self.assertTrue("message" in message)
        self.assertEqual(message["message"], "Error 1")

        self.assertTrue("posted_at" not in message)

        self.assertTrue("_links" in message)

        links = message["_links"]

        self.assertTrue("self" in links)
        self.assertEqual(links["self"], uri)

        self.assertTrue("collection" in links)


    def test_get_unexisting_aggregate_query_message(self):
        self.post_aggregate_query_messages()

        response = self.client.get("/aggregate_query_messages")
        data = response.data.decode("utf8")
        data = json.loads(data)
        messages = data["aggregate_query_messages"]
        message = messages[0]
        uri = message["_links"]["self"]
        # Invalidate uri
        uri = os.path.join(os.path.split(uri)[0], str(uuid.uuid4()))
        response = self.client.get(uri)

        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_bad_request(self):
        response = self.client.post("/aggregate_query_messages")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 400, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


    def test_post_unprocessable_entity(self):
        payload = ""
        response = self.client.post("/aggregate_query_messages",
            data=json.dumps({"aggregate_query_message": payload}),
            content_type="application/json")
        data = response.data.decode("utf8")

        self.assertEqual(response.status_code, 422, "{}: {}".format(
            response.status_code, data))

        data = json.loads(data)

        self.assertTrue("message" in data)


if __name__ == "__main__":
    unittest.main()
