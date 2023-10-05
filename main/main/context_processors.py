from django.conf import settings

def get_sw_version(*args, **kwargs):
    """function to get version number from settings.py

    :return: version string
    :rtype: str
    """
    return {
        'appVersion': settings.SW_VERSION
        }