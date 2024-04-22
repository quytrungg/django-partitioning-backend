from django.core.mail import get_connection

from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import ServiceUnavailable


class EmailHealthCheck(BaseHealthCheckBackend):
    """Check that email backend is working."""

    def check_status(self) -> None:
        """Open and close connection email server."""
        try:
            connection = get_connection(fail_silently=False)
            connection.timeout = 15
            connection.open()
            connection.close()
        except Exception as error:
            self.add_error(
                error=ServiceUnavailable(error),
                cause=error,
            )
