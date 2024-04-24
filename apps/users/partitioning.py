from dateutil.relativedelta import relativedelta
from psqlextra.partitioning import (
    PostgresCurrentTimePartitioningStrategy,
    PostgresPartitioningManager,
    PostgresTimePartitionSize,
)
from psqlextra.partitioning.config import PostgresPartitioningConfig

from .models import Person

# 3 partitions ahead, each partition is one month
# delete partitions older than 6 months
# partitions will be named `[table_name]_[year]_[3-letter month name]`.
manager = PostgresPartitioningManager(
    [
        PostgresPartitioningConfig(
            model=Person,
            strategy=PostgresCurrentTimePartitioningStrategy(
                size=PostgresTimePartitionSize(years=1),
                count=3,
                max_age=relativedelta(months=6),
            ),
        ),
    ],
)
