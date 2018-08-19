from .models import UserData


def remove_credits(user, credits_to_remove, printing_complete):
    data = UserData.objects.get(id=user)
    if data.credits - credits_to_remove >= 0:
        if printing_complete:
            data.credits -= credits_to_remove
            data.save()
        return True
    return False
