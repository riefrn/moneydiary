#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moneydiary.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
#!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys
# # from django.core.management import call_command
# import time

# #

# Apply monkey-patch if we are running the huey consumer.


# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patrol.settings')
#     try:
#         from django.core.management import execute_from_command_line, call_command
#         execute_from_command_line(sys.argv)
#         call_command('run_huey')

#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()
#     if 'run_huey' in sys.argv:
#         from gevent import monkey

#         monkey.patch_all()
