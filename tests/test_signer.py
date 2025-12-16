
import os
import pytest
from jwtsigner import signer

EXAMPLE_PRIVATE_KEY = "tests/keys/private.txt"
EXAMPLE_PUBLIC_KEY = "tests/keys/public.txt"

def get_example_private_key():
    # Use a test key or generate one for testing
    if os.path.exists(EXAMPLE_PRIVATE_KEY):
        with open(EXAMPLE_PRIVATE_KEY) as f:
            return f.read()
    pytest.skip("Test private key not found")

def test_create_jwt_token():
    token = signer.create_jwt_token(private_key_path=EXAMPLE_PRIVATE_KEY, issuer="http://localhost:5000/static/keys.pub", approve='false')
    print(f"\nCreated JWT Token: {token}")
    assert token.count('.') == 2

def test_read_jwt_token():
    token = signer.create_jwt_token(private_key_path=EXAMPLE_PRIVATE_KEY, issuer="http://localhost:5000/static/keys.pub", approve='false')
    print(f"\nToken for read test: {token}")
    header, payload = signer.decode_jwt_token(token, key=get_example_private_key(), verify_signature=False)
    print(f"Header: {header}")
    print(f"Payload: {payload}")
    assert header['alg'] == 'RS256'
    assert header['iss'] == "http://localhost:5000/static/keys.pub"
    assert header['typ'] == 'JWT'
    assert payload['username'] == 'admin'
    assert payload['approve'] == 'false'


def test_edit_jwt_token():
    token = signer.create_jwt_token(private_key_path=EXAMPLE_PRIVATE_KEY, issuer="http://localhost:5000/static/keys.pub", approve='false')
    print(f"\nToken before edit: {token}")
    new_token = signer.edit_jwt_token(token, set_payload=[('approve', 'true')], set_iss="http://localhost:5000/uploads/admin/public.txt", private_key_path=EXAMPLE_PRIVATE_KEY)
    print(f"\nToken after edit: {new_token}")
    header, payload = signer.decode_jwt_token(new_token, key=get_example_private_key(), verify_signature=False)
    print(f"Header after edit: {header}")
    print(f"Payload after edit: {payload}")
    assert header['alg'] == 'RS256'
    assert header['iss'] == "http://localhost:5000/uploads/admin/public.txt"
    assert header['typ'] == 'JWT'
    assert payload['username'] == 'admin'
    assert payload['approve'] == 'true'
