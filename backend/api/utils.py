from ..models import User


def check_role(username, role):
    user = User.query.filter_by(username=username).first()
    if user.role == role:
        return True
    else:
        return False