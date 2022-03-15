from django.utils import timezone


def directory_path(instance, filename):
    # today = timezone.now()
    # today_path = today.strftime("%Y/%m/%d")
    # return f'uploads/rit/routine_upload/{instance}/{today_path}/{filename}'
    return f'uploads/rit/routine_upload/{filename}'

def rit_directory_path(instance, filename):
    return f'uploads/rit/bb/{filename}'
