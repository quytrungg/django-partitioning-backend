import invoke
import saritasa_invocations

from . import project


@invoke.task
def prepare(context: invoke.Context) -> None:
    """Prepare ci environment for check."""
    saritasa_invocations.print_success("Preparing CI")
    saritasa_invocations.docker.up(context)
    saritasa_invocations.github_actions.set_up_hosts(context)
    saritasa_invocations.system.copy_local_settings(context)
    project.build(context)
