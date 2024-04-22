import invoke
import saritasa_invocations


@invoke.task
def build(
    context: invoke.Context,
) -> None:
    """Build python environ."""
    if (
        saritasa_invocations.python.get_python_env()
        == saritasa_invocations.python.PythonEnv.LOCAL
    ):
        saritasa_invocations.poetry.install(context)
    else:
        saritasa_invocations.docker.buildpack(context)


@invoke.task
def init(
    context: invoke.Context,
    clean: bool = False,
) -> None:
    """Prepare env for working with project."""
    saritasa_invocations.print_success("Setting up project")
    saritasa_invocations.git.setup(context)
    saritasa_invocations.print_success("Initial assembly of all dependencies")
    if clean:
        saritasa_invocations.docker.clear(context)
    saritasa_invocations.system.copy_local_settings(context)
    saritasa_invocations.system.copy_vscode_settings(context)
    build(context)
    saritasa_invocations.django.migrate(context)
    saritasa_invocations.django.set_default_site(context)
    saritasa_invocations.django.createsuperuser(context)
    saritasa_invocations.print_success("Project setup is completed")


@invoke.task
def init_from_scratch(
    context: invoke.Context,
) -> None:
    """Build project from scratch.

    This command should be run once on project start, it should be deleted
    after that.

    """
    saritasa_invocations.print_success(
        "Prepare project from scratch, run just once",
    )
    saritasa_invocations.system.copy_local_settings(context)
    saritasa_invocations.system.copy_vscode_settings(context)
    build(context)
    saritasa_invocations.django.makemigrations(context)
    init(context)
