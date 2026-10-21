import unittest

from service.init import create_app


class AccountsApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["application"], "accounts")

    def test_create_list_read_update_delete(self):
        created = self.client.post(
            "/accounts",
            json={"name": "Ada Lovelace", "email": "ada@example.com"},
        )
        self.assertEqual(created.status_code, 201)
        account_id = created.get_json()["id"]

        listed = self.client.get("/accounts")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(len(listed.get_json()), 1)

        read = self.client.get(f"/accounts/{account_id}")
        self.assertEqual(read.status_code, 200)
        self.assertEqual(read.get_json()["name"], "Ada Lovelace")

        updated = self.client.patch(
            f"/accounts/{account_id}", json={"name": "Ada"}
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["name"], "Ada")

        deleted = self.client.delete(f"/accounts/{account_id}")
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(
            self.client.get(f"/accounts/{account_id}").status_code, 404
        )

    def test_create_requires_name(self):
        response = self.client.post("/accounts", json={"email": "x@example.com"})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
