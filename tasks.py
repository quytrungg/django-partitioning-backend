import invoke
import saritasa_invocations

import invocations

ns = invoke.Collection(
    invocations.project,
    invocations.frontend,
    invocations.ci,
    saritasa_invocations.docker,
    saritasa_invocations.django,
    saritasa_invocations.open_api,
    saritasa_invocations.git,
    saritasa_invocations.pre_commit,
    saritasa_invocations.python,
    saritasa_invocations.system,
    saritasa_invocations.k8s,
    saritasa_invocations.db,
    saritasa_invocations.poetry,
    saritasa_invocations.mypy,
    saritasa_invocations.pytest,
    saritasa_invocations.cruft,
    saritasa_invocations.celery,
)


# Configurations for run command
ns.configure(
    {
        "run": {
            "pty": True,
            "echo": True,
        },
        "saritasa_invocations": saritasa_invocations.Config(
            project_name="django-partitioning-backend",
            django=saritasa_invocations.DjangoSettings(
                app_boilerplate_link="git@github.com:saritasa-nest/saritasa-python-boilerplate-django.git",
            ),
            docker=saritasa_invocations.DockerSettings(
                main_containers=(
                    "postgres",
                    "redis",
                ),
                buildpack_builder=(
                    "public.ecr.aws/saritasa/buildpacks/paketo/builder:latest"
                ),
                buildpack_runner=(
                    "public.ecr.aws/saritasa/buildpacks/paketo/runner:latest"
                ),
            ),
            k8s_defaults=saritasa_invocations.K8SDefaultSettings(
                proxy="teleport.saritasa.rocks",
                secret_file_path_in_pod="/workspace/app/config/settings/.env",
                db_config=saritasa_invocations.K8SDBSettings(
                    namespace="utils",
                    pod_selector="app=saritasa-rocks-psql",
                ),
            ),
        ),
    },
)
