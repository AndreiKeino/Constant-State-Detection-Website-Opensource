from django.conf import settings


def get_max_upload_file_size_bytes() -> int:
    return settings.MAX_POINTS_CSD * 24


def get_max_upload_file_size_kb() -> int:
    return (settings.MAX_POINTS_CSD * 24) // 1024
