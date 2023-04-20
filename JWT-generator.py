import jwt
import time
import uuid
import secrets

def generate_jwt(payload, secret, headers):
    iat = int(time.time())
    exp = iat + 300000
    payload['iat'] = iat
    payload['exp'] = exp
    token = jwt.encode(payload, secret, algorithm='HS256', headers=headers)
    jwt_str = token.decode('utf-8')
    return jwt_str

secret = "{confidentialClientSecretHere}"
headers = {"alg": "HS256", "typ": "JWT"}

subject     = "{UUID-Here}"
issuer      = "{URL}"
audience    = "{confidentialClientID}"
jti         = str(uuid.uuid4())
# nonce       = secrets.token_hex(16)

payload = {"sub": subject, "iss": issuer, "aud": audience, "jti": jti }

jwt_token = generate_jwt(payload, secret, headers)
print(jwt_token)
