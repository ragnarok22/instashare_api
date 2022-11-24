"""Poetry commands for development
"""
import shlex
import subprocess


def __run_process(command: str) -> str:
    """Run a process

    :param command: command to run
    :return: the stdout of the command
    """
    try:
        process = subprocess.run(shlex.split(command), universal_newlines=True)
        return process.stdout
    except KeyboardInterrupt:
        pass


def runserver():
    """Run Django server"""
    __run_process("python manage.py runserver")


def test():
    """Run test coverages"""
    __run_process("coverage run manage.py test apps")


def celery():
    """Run celery workers"""
    __run_process(
        "celery -A config.celery beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"
    )


def migrate():
    """Apply the migrations"""
    __run_process("python manage.py migrate")


def makemigrations():
    """Make the migrations"""
    __run_process("python manage.py makemigrations")


def migrate_all():
    """Makes the migrations and then migrate it"""
    makemigrations()
    migrate()
