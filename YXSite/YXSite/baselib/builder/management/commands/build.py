import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import reverse
from django.test.client import Client


def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith('.html'):
            yield name[:-5]


class Command(BaseCommand):
    help = 'Build static site output.'
    leave_locale_alone = True

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')

    def handle(self, *args, **options):
        """Request pages and build output."""
        settings.DEBUG = False
        settings.COMPRESS_ENABLED = True
        if args:
            pages = args
            available = list(get_pages())
            invalid = []
            for page in pages:
                if page not in available:
                    invalid.append(page)
            if invalid:
                msg = 'Invalid pages: {}'.format(', '.join(invalid))
                raise CommandError(msg)
        else:
            pages = get_pages()
            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)

        os.makedirs(settings.STATIC_ROOT, exist_ok=True)

        call_command('collectstatic', interactive=False, clear=True, verbosity=0)
        # call_command('compress', interactive=False, force=True)
        call_command('compress', force=True)

        client = Client()
        for page in pages:
            url = reverse('page', kwargs={'slug': page})
            response = client.get(url)

            if page == 'index':
                output_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
                f.write(response.content)


####################################################################################
# 一个快速简单的例子
####################################################################################

# class Command(BaseCommand):
#
#     def add_arguments(self, parser):
#
#         parser.add_argument(
#             '-n',
#             '--name',
#             action='store',
#             dest='name',
#             default='close',
#             help='name of author.',
#         )
#
#     def handle(self, *args, **options):
#         try:
#             if options['name']:
#                 print
#                 'hello world, %s' % options['name']
#
#             self.stdout.write(self.style.SUCCESS('命令%s执行成功, 参数为%s' % (__file__, options['name'])))
#         except Exception, ex:
#             self.stdout.write(self.style.ERROR('命令执行出错'))
