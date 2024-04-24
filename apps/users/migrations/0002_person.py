# Generated by Django 4.2.11 on 2024-04-22 03:25

from django.db import migrations, models

import psqlextra
from psqlextra.backend.migrations.operations.create_partitioned_model import (
    PostgresCreatePartitionedModel,
)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        PostgresCreatePartitionedModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("birth_date", models.DateField()),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            partitioning_options={
                "method": psqlextra.types.PostgresPartitioningMethod["RANGE"],
                "key": ["birth_date"],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        # PostgresAddDefaultPartition(
        #     model_name='Person',
        #     name='default',
        # ),
    ]
