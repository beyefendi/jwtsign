import logging
import os
import sys

import jwt

JWT_ALGORITHM = "RS256"
JWT_ISSUER = "http://localhost:5000/static/keys.pub"

logger = logging.getLogger(__name__)

def load_private_key(private_key_path=None):
	"""Load the RSA private key from file."""
	key_path = private_key_path or os.environ.get("JWT_PRIVATE_KEY_PATH", os.path.join(os.path.dirname(__file__), "../private_key.pem"))
	try:
		with open(key_path, 'r') as key_file:
			return key_file.read()
	except FileNotFoundError:
		logger.error(f"Private key file not found: {key_path}")
		print("\n" + "="*70)
		print("ERROR: Private key file not found!")
		print("="*70)
		print(f"\nLooking for: {key_path}\n")
		print("To fix this issue, you have two options:\n")
		print("1. Generate a new RSA key pair:")
		print("   openssl genrsa -out private_key.pem 2048")
		print(f"   (Save it to: {key_path})\n")
		print("2. Specify a custom key file path:")
		print("   export JWT_PRIVATE_KEY_PATH=/path/to/your/private_key.pem")
		print("   jwtsigner\n")
		print("="*70)
		sys.exit(1)
	except Exception as e:
		logger.error(f"Error loading private key: {str(e)}")
		raise

def create_jwt_token(issuer=JWT_ISSUER, private_key_path=None, username="admin", approve=True):
	try:
		private_key = load_private_key(private_key_path)
		token_data = {
			"username": username,
			"approve": approve
		}
		headers = {
			"typ": "JWT",
			"alg": JWT_ALGORITHM,
			"iss": issuer
		}
		token = jwt.encode(token_data, private_key, algorithm=JWT_ALGORITHM, headers=headers)
		logger.info("JWT token created successfully")
		return token
	except Exception as e:
		logger.error(f"Error creating JWT token: {str(e)}")
		raise

def decode_jwt_token(token, key=None, verify_signature=True):
	try:
		payload = jwt.decode(token, key, algorithms=[JWT_ALGORITHM], options={"verify_signature": verify_signature})
		header = jwt.get_unverified_header(token)
		return header, payload
	except Exception as e:
		logger.error(f"Failed to decode JWT token: {str(e)}")
		raise

def edit_jwt_token(token, set_payload=None, set_iss=None, private_key_path=None):
	try:
		key = load_private_key(private_key_path)
		payload = jwt.decode(token, key, algorithms=[JWT_ALGORITHM], options={"verify_signature": False})
		header = jwt.get_unverified_header(token)
		if set_payload:
			for k, v in set_payload:
				payload[k] = v
		if set_iss:
			header['iss'] = set_iss
		new_token = jwt.encode(payload, key, algorithm=JWT_ALGORITHM, headers=header)
		return new_token
	except Exception as e:
		logger.error(f"Failed to edit JWT token: {str(e)}")
		raise
import logging

logger = logging.getLogger(__name__)

# Add reusable JWT signing and verification functions here
