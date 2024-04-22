"""Configuration file for pytest."""

from django.conf import settings

import pytest


def pytest_configure() -> None:
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.

    """
    settings.DEBUG = False
    settings.RESTRICT_DEBUG_ACCESS = True
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/dev/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(scope="session", autouse=True)
def django_db_setup(django_db_setup) -> None:  # noqa: PT004, ANN001
    """Set up test db for testing."""


@pytest.fixture(autouse=True)
def _enable_db_access_for_all_tests(django_db_setup, db) -> None:  # noqa: ANN001
    """Enable access to DB for all tests."""


@pytest.fixture(scope="session", autouse=True)
def _temp_directory_for_media(tmp_path_factory) -> None:  # noqa: ANN001
    """Fixture that set temp directory for all media files.

    This fixture changes default STORAGE to filesystem and provides temp dir
    for media. PyTest cleans up this temp dir by itself after few test runs.

    """
    settings.STORAGES["default"]["BACKEND"] = (
        "django.core.files.storage.FileSystemStorage"
    )
    settings.MEDIA_ROOT = tmp_path_factory.mktemp("tmp_media")
