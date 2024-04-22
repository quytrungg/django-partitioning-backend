import pathlib

import invoke
import saritasa_invocations

FRONTEND_REPO_NAME = "django-partitioning-frontend"
FRONTEND_REPO_PATH = pathlib.Path(f"../{FRONTEND_REPO_NAME}")
FRONTEND_REPO_LINK = f"git@github.com:saritasa-nest/{FRONTEND_REPO_NAME}.git"


@invoke.task
def run(
    context: invoke.Context,
    frontend_repo_path: pathlib.Path = FRONTEND_REPO_PATH,
    backend_port: int = 8000,
    rebuild: bool = True,
    clean_build: bool = True,
    branch: str = "develop",
) -> None:
    """Run frontend locally.

    Params:
    - `--no-rebuild` param to just run `npm start` without reinstalling
    dependencies;
    - `--no-clean-build` to use `npm install` instead of `npm
    ci` during installing node packages;

    """
    if rebuild:
        saritasa_invocations.print_success("Preparing frontend directory...")
        saritasa_invocations.git.clone_repo(
            context,
            repo_link=FRONTEND_REPO_LINK,
            repo_path=frontend_repo_path,
            branch=branch,
        )
        install_dependencies(context, frontend_repo_path, clean_build)
        create_env_file(frontend_repo_path, backend_port)

    npm(context, command="start", frontend_repo_path=frontend_repo_path)


def install_dependencies(
    context: invoke.Context,
    frontend_repo_path: pathlib.Path,
    clean_build: bool,
) -> None:
    """Install frontend dependencies via `npm ci`.

    `clean_build` param allows to choose strategy of updating dependencies. If
    True use `npm ci` otherwise use `npm install`

    """
    saritasa_invocations.print_success("Installing frontend dependencies...")
    command = "ci" if clean_build else "install"
    npm(context, command=command, frontend_repo_path=frontend_repo_path)


def create_env_file(
    frontend_repo_path: pathlib.Path,
    backend_port: int,
) -> None:
    """Set up .env file for frontend.

    Set both `NG_APP_API_URL` and `REACT_APP_API_URL` to work with both the
    Angular/React framework in different projects. `VITE_API_URL` is required
    for React projects.

    """
    saritasa_invocations.print_success("Creating env file...")
    env_file = pathlib.Path(frontend_repo_path) / ".env.development.local"
    possible_framework_prefixes = ("NG_APP", "REACT_APP", "VITE")
    backend_api_url_env_vars = "\n".join(
        f"{prefix}_API_URL='http://localhost:{backend_port}/api/v1/'"
        for prefix in possible_framework_prefixes
    )
    env_file.write_text(
        f"{backend_api_url_env_vars}\n",
        # Here you can add other settings for local frontend
    )


def npm(
    context: invoke.Context,
    command: str,
    frontend_repo_path: pathlib.Path,
) -> None:
    """Call `npm` inside frontend dir with passed command."""
    with context.cd(frontend_repo_path):
        context.run(f"npm {command}")
