from app.auth.jwt import verify_password
import pytest

def test_verify_password():
    assert verify_password("password", "$2b$12$6J66JipbF6ok37vj3LRm.OWsOmomz0v1uuQbawDEOTv/3O4bH1yzK")
    assert not verify_password("wrong_password", "$2b$12$Kb6vlfMV36Qg1T0DDZJP2uGZyHDUxSjtZJN.MEKEYE3iS1wBxM7Ae")