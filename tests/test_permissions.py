from app.permissions import PermissionPolicy, Risk

def test_confirmation_policy():
    policy = PermissionPolicy()
    assert policy.requires_confirmation(Risk.ROUTINE) is False
    assert policy.requires_confirmation(Risk.CONSEQUENTIAL) is True
    assert policy.requires_confirmation(Risk.CRITICAL) is True
