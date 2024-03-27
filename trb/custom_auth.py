from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class StudentAuthenticationBackend(BaseBackend):
    def authenticate(self, request, name=None, dob=None):
        if name is None or dob is None:
            return None

        try:
            user = User.objects.get(first_name=name)
            student = user.student
            if student.date_of_birth == dob:
                return user
        except User.DoesNotExist:
            pass
        except Student.DoesNotExist:
            pass
        except ValidationError:
            pass

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

