from django.core.management.base import BaseCommand

from trainer.models import Word


class Command(BaseCommand):

    help = 'Load words from txt file'

    def handle(self, *args, **kwargs):

        with open('data/words.txt', 'r', encoding='utf-8') as file:

            for line in file:

                english, russian, example = line.strip().split(',')

                Word.objects.create(
                    english=english,
                    russian=russian,
                    example=example
                )

        self.stdout.write(
            self.style.SUCCESS('Words loaded successfully!')
        )