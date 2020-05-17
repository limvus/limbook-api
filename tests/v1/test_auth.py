import secrets
from datetime import datetime, timedelta
from unittest import main

from flask import json

from limbook_api.v1.users import generate_user, generate_role, User
from tests.base import BaseTestCase, api_base


class UserTestCase(BaseTestCase):
    """This class represents the test case for Users"""
    # Helper methods -------------------------
    def login_random_user(self):
        user = generate_user(password="password")
        login_data = {
            "email": user.email,
            "password": "password",
        }

        return self.client().post(
            api_base + '/login',
            json=login_data
        )

    def assert_successful_login(self, res):
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))

    # Auth Token and Permission Tests -----------------------------

    def test_cannot_access_protected_route_without_token(self):
        # make request
        res = self.client().get(
            api_base
            + '/secure-route'
        )

        # assert
        self.assertEqual(res.status_code, 401)

    def test_cannot_access_protected_route_with_invalid_token(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_INVALID_TOKEN')}

        # make request
        res = self.client().get(
            api_base
            + '/secure-route',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'invalid_header')

    def test_cannot_access_protected_route_with_expired_token(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}

        # make request
        res = self.client().get(
            api_base
            + '/secure-route',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'token_expired')

    def test_cannot_access_protected_route_without_correct_permission(self):
        # request
        res = self.client().get(
            api_base
            + '/secure-route?mock_token_verification=True&permission='
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_access_protected_route_with_correct_permission(self):
        # request
        res = self.client().get(
            api_base
            + '/secure-route'
            + '?mock_token_verification=True&permission=read:secure_route'
        )

        # assert
        self.assertEqual(res.status_code, 200)

    # Auth User Tests ----------------------------------------------

    def test_user_can_register(self):
        # request
        generate_role(
            name="Unverified User Role",
            slug="unverified_user",
            permissions=[]
        )
        user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "phone_number": "9982938838",
            "password": "password",
            "confirm_password": "password"
        }

        res = self.client().post(
            api_base + '/register',
            json=user
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('user'))

    def test_user_can_send_verification_email(self):
        # request
        user = generate_user()

        res = self.client().post(
            api_base + '/send-verification-email',
            json={"email": user.email}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_user_can_verify_email(self):
        # given
        user = generate_user(
            email_verif_code=secrets.token_hex(8),
            email_verif_code_expires_on=datetime.now() + timedelta(hours=1)
        )

        res = self.client().post(
            api_base + '/verify-email',
            json={"verification_code": user.email_verif_code}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_user_can_send_reset_password_email(self):
        # request
        user = generate_user()

        res = self.client().post(
            api_base + '/send-reset-password-email',
            json={"email": user.email}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_user_can_reset_password(self):
        # Reset password -----------------------------------------
        # given
        user = generate_user(
            password_reset_code=secrets.token_hex(8),
            password_reset_code_expires_on=datetime.now() + timedelta(hours=1)
        )
        data = {
            "email": user.email,
            "password_reset_code": user.password_reset_code,
            "password": "new_password",
            "confirm_password": "new_password"
        }

        res = self.client().post(
            api_base + '/reset-password',
            json=data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

        # Assert login with new password ---------------------------
        user = User.query.first()
        login_data = {
            "email": user.email,
            "password": "new_password",
        }

        res = self.client().post(
            api_base + '/login',
            json=login_data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))

    def test_user_can_login(self):
        res = self.login_random_user()
        self.assert_successful_login(res)

    def test_user_can_refresh_access_token(self):
        # login random user and get tokens
        res = self.login_random_user()
        data = json.loads(res.data)
        refresh_token = data.get('refresh_token')

        # given
        headers = {'Authorization': 'Bearer ' + refresh_token}

        # make request
        res = self.client().get(
            api_base
            + '/refresh-token',
            headers=headers
        )

        # assert
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data.get('refresh_token'), refresh_token)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
