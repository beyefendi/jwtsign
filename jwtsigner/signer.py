import logging
import os
import sys

import jwt

JWT_ALGORITHM = "RS256"
JWT_ISSUER = "http://localhost:5000/static/keys.pub"


logger = logging.getLogger(__name__)

def load_public_key(public_key_path=None):
    """Load the RSA public key from file."""
    if public_key_path:
        key_path = public_key_path
    elif os.environ.get("JWT_PUBLIC_KEY_PATH"):
        key_path = os.environ["JWT_PUBLIC_KEY_PATH"]
    else:
        # Use a path relative to the current working directory
        key_path = os.path.join("tests", "keys", "public.txt")
        print(f"Using default public key path: {os.path.abspath(key_path)}")
    try:
        with open(key_path, 'r') as key_file:
            return key_file.read()
    except FileNotFoundError:
        logger.error(f"Public key file not found: {key_path}")
        print("\n" + "=" * 70)
        print("ERROR: Public key file not found!")
        print("=" * 70)
        print(f"\nLooking for: {os.path.abspath(key_path)}\n")
        print("To fix this issue, you have two options:\n")
        print("1. Generate a new RSA key pair:")
        print("   openssl genrsa -out private_key.pem 2048")
        print("   openssl rsa -in private_key.pem -pubout -out public_key.pem")
        print("2. Specify a custom key file path:")
        print("   export JWT_PUBLIC_KEY_PATH=/path/to/your/public_key.pem")
        print("   jwtsigner\n")
        print("=" * 70)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error loading public key: {str(e)}")
        raise

def load_private_key(private_key_path=None):
    """Load the RSA private key from file."""
    if private_key_path:
        key_path = private_key_path
    elif os.environ.get("JWT_PRIVATE_KEY_PATH"):
        key_path = os.environ["JWT_PRIVATE_KEY_PATH"]
    else:
        # Use a path relative to the current working directory
        key_path = os.path.join("tests", "keys", "private.txt")
        print(f"Using default private key path: {os.path.abspath(key_path)}")
    try:
        with open(key_path, 'r') as key_file:
            return key_file.read()
    except FileNotFoundError:
        logger.error(f"Private key file not found: {key_path}")
        print("\n" + "=" * 70)
        print("ERROR: Private key file not found!")
        print("=" * 70)
        print(f"\nLooking for: {os.path.abspath(key_path)}\n")
        print("To fix this issue, you have two options:\n")
        print("1. Generate a new RSA key pair:")
        print("   openssl genrsa -out private_key.pem 2048")
        print("2. Specify a custom key file path:")
        print("   export JWT_PRIVATE_KEY_PATH=/path/to/your/private_key.pem")
        print("   jwtsigner\n")
        print("=" * 70)
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

def decode_jwt_token(token, public_key_path=None, verify_signature=True):
    try:
        key = load_public_key(public_key_path)
        verified = False
        try:
            payload = jwt.decode(token, key, algorithms=JWT_ALGORITHM, options={"verify_signature": verify_signature})
            verified = verify_signature
        except jwt.exceptions.InvalidSignatureError:
            payload = jwt.decode(token, key, algorithms=JWT_ALGORITHM, options={"verify_signature": False})
            verified = False
        header = jwt.get_unverified_header(token)
        if verify_signature:
            if verified:
                print("JWT verification: \033[92mVERIFIED\033[0m")
            else:
                print("JWT verification: \033[91mNOT VERIFIED\033[0m")
        else:
            print("JWT verification: \033[93mSIGNATURE NOT CHECKED\033[0m")
        return header, payload
    except Exception as e:
        logger.error(f"Failed to decode JWT token: {str(e)}")
        print(f"JWT verification: \033[91mNOT VERIFIED\033[0m (error: {str(e)})")
        raise

def edit_jwt_token(token, set_payload=None, set_iss=None, private_key_path=None, public_key_path=None, verify_signature=True):
    try:
        # Use public key to verify/decode, private key to sign
        private_key = load_private_key(private_key_path)
        public_key = load_public_key(public_key_path)
        verified = False
        try:
            payload = jwt.decode(token, public_key, algorithms=JWT_ALGORITHM, options={"verify_signature": verify_signature})
            verified = verify_signature
        except jwt.exceptions.InvalidSignatureError:
            payload = jwt.decode(token, public_key, algorithms=JWT_ALGORITHM, options={"verify_signature": False})
            verified = False
        header = jwt.get_unverified_header(token)
        if verify_signature:
            if verified:
                print("JWT verification: \033[92mVERIFIED\033[0m")
            else:
                print("JWT verification: \033[91mNOT VERIFIED\033[0m")
        else:
            print("JWT verification: \033[93mSIGNATURE NOT CHECKED\033[0m")
        if set_payload:
            for k, v in set_payload:
                payload[k] = v
        if set_iss:
            header['iss'] = set_iss
        new_token = jwt.encode(payload, private_key, algorithm=JWT_ALGORITHM, headers=header)
        return new_token
    except Exception as e:
        logger.error(f"Failed to edit JWT token: {str(e)}")
        print(f"JWT verification: \033[91mNOT VERIFIED\033[0m (error: {str(e)})")
        raise


logger = logging.getLogger(__name__)

# Add reusable JWT signing and verification functions here
