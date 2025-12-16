# JWT Signer

A simple JWT token signing utility using RS256 algorithm. Note that in JWT context, there is no encryption & decryption logic but signing & verification. That is why to create a token, data signed with a private key and signature verified by public key.


## Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenSSL (for generating RSA keys)

### Generate RSA Key Pair (Optional)

Before installation, generate your RSA key pair:

```bash
# Generate private key (2048-bit)
openssl genrsa -out private_key.pem 2048

# Generate public key (for verification)
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

⚠️ If you need to use publicly known public and private key pair (test/keys/), one very common is also provided that can be used to create vulnerable tokens.

## Installation Methods

### Method 0: Modern PEP 517/518 Installation (Recommended)

If you have a modern version of `pip` (>=21.3), you can install directly from the source using the `pyproject.toml` file:

```bash
# Getting the code
cd /location/you-want-to-install
git clone https://github.com/beyefendi/jwtsigner.git
cd jwtsigner

# (Optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable/development mode
pip install -e .

# Or install normally (builds from pyproject.toml)
pip install .
```

Or, to build a wheel and install:
```bash
pip install build
python -m build
pip install dist/jwtsigner-*.whl
```

You can also install development dependencies:
```bash
pip install .[dev]
```

### Method 1: User Installation

You can install the package using the provided `requirements.txt` file:

#### Step 1: Getting the Code

```bash
cd /location/you-want-to-install
git clone https://github.com/beyefendi/jwtsigner.git
cd jwtsigner
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
# Activate environment
source .venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Method 2: System-wide Deployment

This method installs the package in a central location accessible to all users (including AI agents).

#### Step 1: Getting the Code

```bash
cd /opt
sudo git clone https://github.com/beyefendi/jwtsigner.git
cd jwtsigner/
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
# Activate environment
source .venv/bin/activate
```

#### Step 3: Install Package

```bash

# Install jwtsigner
pip install -r requirements.txt

# Deactivate when done
deactivate
```

#### Step 4: Create Wrapper Script

Create `/usr/local/bin/jwtsigner`:

```bash
#!/bin/bash

# Path to virtual environment
VENV_PATH="/opt/jwtsigner/.venv"

# Activate and run
source "$VENV_PATH/bin/activate"
python -m jwtsigner.cli "$@"
deactivate
```

#### Step 5: Make Executable

```bash
sudo chmod +x /usr/local/bin/jwtsigner
```


### Method 3: Development Installation

For local development or single-user systems.

#### Step 1: Navigate to Project Directory

```bash
cd /location/you-want-to-install
git clone https://github.com/beyefendi/jwtsigner.git
cd jwtsigner
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
# Activate environment
source .venv/bin/activate
```

#### Step 3: Install Package

Development mode (editable):
```bash
pip install -e .
```

Or regular installation:
```bash
pip install .
```

## Command Line Usage

### Configuration

The tool uses RS256 algorithm and requires a private and public key pair.
You can provide configuration via environment variables or command-line options:

- **`JWT_PRIVATE_KEY_PATH`**: Path to your RSA private key file (optional, can also use `--private-key` argument)
  - Default: `private.key` in `tests/keys/` directory
- **`JWT_ISSUER`**: Token issuer URL (optional, can also use `--issuer` argument)
  - Default: `http://localhost:5000/static/keys.pub`

### Token Details

The generated JWT token includes:

**Header:**
- `typ`: JWT
- `alg`: RS256
- `iss`: Token issuer URL (not the address of the public/private key files)

**Payload:**
- `username`: admin
- `approve`: true

### 1. Create a JWT Token (default)

```bash
# Create a new JWT token
jwtsigner create

# With custom private key
jwtsigner create --private-key /path/to/your/private_key.pem

# With custom private key in environment variables
JWT_PRIVATE_KEY_PATH="/opt/jwtsigner/tests/keys/private.txt" && jwtsigner create

# With custom issuer
jwtsigner create --issuer "https://yourdomain.com/keys.pub"

# With custom private key and issuer in environment variables
JWT_PRIVATE_KEY_PATH="/etc/ssl/private/jwt_key.pem" \
JWT_ISSUER="https://auth.example.com/keys.pub" \
jwtsigner create
```

### 2. Read/Decode a JWT Token

```bash
# View the header and payload of a JWT token
jwtsigner read --token <JWT_TOKEN>

# With public key verification
jwtsigner read --token <JWT_TOKEN> --public-key public_key.pem

# Example
jwtsigner read --token eyJhbGciOiJSUzI1NiIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC9zdGF0aWMva2V5cy5wdWIiLCJ0eXAiOiJKV1QifQ.eyJ1c2VybmFtZSI6ImFkbWluIiwiYXBwcm92ZSI6ZmFsc2V9.3YlEEiBH7CiEy6cSuXE4TKsWonLaxuXeFBoHsdZDSwubfDJQCtVtYnRG_zeZA6H0Eveez1V3Rr8mZrFq4rHTWUMzWcK4lHnu4X2sY8wqDWs5jg2UQVhRXQ1fnRHgpvtl16f0AIUGS_zBAjTTxpmt1CDHGhbVuxgRYoYB61xdtqQVS1LBmmCilq1vS2OLKiD_xuI1EOeAKmlz7asHnYgLYkC0IudN37ZFv110gdK_-gKxOtrfoAR9ArNQ_t9V1sK1qTa_rqfevs2P7x2J_w2VZf85J0iOqFqLXtZzbDLk6IOdpI-FqJ7Z5vNUrv9CmAhrD1R92YYDa4KQDX7sKwl9dg --public-key public.txt

# Output
Header:
{'alg': 'RS256', 'iss': 'http://localhost:5000/static/keys.pub', 'typ': 'JWT'}
Payload:
{'username': 'admin', 'approve': False}

# Example 2
jwtsigner read --token eyJhbGciOiJSUzI1NiIsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMC91cGxvYWRzL2FkbWluL3B1YmxpYy50eHQiLCJ0eXAiOiJKV1QifQ.eyJ1c2VybmFtZSI6ImFkbWluIiwiYXBwcm92ZSI6InRydWUifQ.l6EoWm87BlqXrd09njeWYdWFgIuT5HNK2MzQjCLKjqG2v3cPNutjGIbrneV5jaNytG2XRTOotVKC83rRDNfJdySkDY7OyacQNo7jGxOUlpbU52TWlPNmxqtQw3xPnguUuAVoT75l3WhdxK-uCGkERr8dJqNS06Ub8K7XUANzJAgpg73amUX7MXOnYQ1_utfQd7j21gi2cFQjzJxKwHo-j8ALn-_08TPOhDbWITwhDScyx0u8zwdQNGGe0ErdDHoco7uZXEGH_vqUsir7f0W-0oacnbrsQdi22TTNGIwP0gLVH9N3oe6KqULKQ6Pu_PGjZrgj8dgwixTkLHLkc-Lbig --public-key public.txt

# Output
Header:
{'alg': 'RS256', 'iss': 'http://localhost:5000/uploads/admin/public.txt', 'typ': 'JWT'}
Payload:
{'username': 'admin', 'approve': 'true'}
```

### 3. Edit a JWT Token (payload or 'iss' in header)

```bash
# Change payload fields (e.g., username and approve)
jwtsigner edit --token <JWT_TOKEN> --set-payload username newuser --set-payload approve false

# Change only the 'iss' field in the header
jwtsigner edit --token <JWT_TOKEN> --set-iss "https://newissuer.com/keys.pub"

# Change both payload and header
jwtsigner edit --token <JWT_TOKEN> --set-payload username newuser --set-iss "https://newissuer.com/keys.pub"

# With custom private key
jwtsigner edit --token <JWT_TOKEN> --set-payload approve true --set-iss "http://localhost:5000/uploads/admin/public.txt" --private-key private.txt
```

## Maintenance

### Updating

For user or system-wide installation:
```bash
pip install . --upgrade
```

For development, you do not need anything to do:


### Uninstalling

```bash
pip uninstall jwtsigner
```


For system-wide deployment, also remove the wrapper script:
```bash
sudo rm /usr/local/bin/jwtsigner
```

## Troubleshooting

### Permission Denied

For system-wide installation, ensure you have sudo privileges:
```bash
sudo chmod 755 /opt/jwtsigner
sudo chown -R $(whoami):$(whoami) /opt/jwtsigner
```

## Security Notes

- **Never commit** `private_key.pem` to version control
- Store private keys securely with appropriate file permissions (600)
- Use environment-specific keys for production
- Rotate keys periodically

```bash
# Set secure permissions
chmod 600 private_key.pem
```
