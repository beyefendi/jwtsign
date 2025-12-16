import argparse
import sys

from .signer import JWT_ISSUER, create_jwt_token, decode_jwt_token, edit_jwt_token


def main():
    parser = argparse.ArgumentParser(description="JWT Signer Utility")
    subparsers = parser.add_subparsers(dest="command", required=False)

    # Create command (default)
    parser_create = subparsers.add_parser("create", help="Create a new JWT token")
    parser_create.add_argument("--private-key", type=str, help="Path to private key file")
    parser_create.add_argument("--issuer", type=str, default=JWT_ISSUER, help="Token issuer URL")
    parser_create.add_argument("--username", type=str, default="admin", help="Username for payload (default: admin)")
    parser_create.add_argument("--approve", type=str, default="True", help="Approve value for payload (default: True)")

    # Read command
    parser_read = subparsers.add_parser("read", help="Read and decode a JWT token")
    parser_read.add_argument("--token", type=str, required=True, help="JWT token to decode")
    parser_read.add_argument("--public-key", type=str, help="Path to public key for RS256 verification (optional)")

    # Edit command
    parser_edit = subparsers.add_parser("edit", help="Edit a JWT token's payload or header (iss only)")
    parser_edit.add_argument("--token", type=str, required=True, help="JWT token to edit")
    parser_edit.add_argument("--private-key", type=str, help="Path to private key file")
    parser_edit.add_argument("--set-payload", nargs=2, action='append', metavar=('KEY', 'VALUE'), help="Set payload key to value (can be used multiple times)")
    parser_edit.add_argument("--set-iss", type=str, help="Set 'iss' in header")

    args = parser.parse_args()

    if args.command in (None, "create"):
        try:
            approve_val = getattr(args, 'approve', None)
            if approve_val is None:
                approve_val = True
            # Convert string to bool if needed
            if isinstance(approve_val, str):
                if approve_val.lower() == "true":
                    approve_val = True
                elif approve_val.lower() == "false":
                    approve_val = False
            token = create_jwt_token(
                issuer=getattr(args, 'issuer', JWT_ISSUER),
                private_key_path=getattr(args, 'private_key', None),
                username=getattr(args, 'username', "admin"),
                approve=approve_val
            )
            print(f"Generated JWT Token:\n{token}")
        except Exception as e:
            print(f"Failed to create JWT token: {str(e)}")
            sys.exit(1)
    elif args.command == "read":
        try:
            key = None
            if args.public_key:
                with open(args.public_key, 'r') as f:
                    key = f.read()
            header, payload = decode_jwt_token(args.token, key, verify_signature=bool(key))
            print("Header:")
            print(header)
            print("Payload:")
            print(payload)
        except Exception as e:
            print(f"Failed to decode JWT token: {str(e)}")
            sys.exit(1)
    elif args.command == "edit":
        try:
            new_token = edit_jwt_token(args.token, set_payload=args.set_payload, set_iss=args.set_iss, private_key_path=getattr(args, 'private_key', None))
            print(f"Edited JWT Token:\n{new_token}")
        except Exception as e:
            print(f"Failed to edit JWT token: {str(e)}")
            sys.exit(1)
