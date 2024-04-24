# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.postgresql",
        "ENGINE": "psqlextra.backend",
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,
    },
}

PSQLEXTRA_PARTITIONING_MANAGER = "apps.users.partitioning.manager"
