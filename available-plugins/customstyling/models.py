from uuid import uuid4

from django.db import models
from django.db.models.signals import m2m_changed

from utils import shared


def generate_stylesheet_name():
    return '{}.css'.format(uuid4())


class CrossJournalStylesheet(models.Model):
    stylesheet_name = models.CharField(
        max_length=40,
        default=generate_stylesheet_name,
    )
    journals = models.ManyToManyField(
        'journal.Journal',
    )


def clear_cache_if_m2m_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action in ['post_add', 'post_remove']:
        # Clear the cache if we've added or removed an instance.
        shared.clear_cache()


m2m_changed.connect(clear_cache_if_m2m_change, sender=CrossJournalStylesheet.journals.through)
