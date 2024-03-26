from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from app_transcription.models import Recording, APIClient


@receiver([post_delete, post_save], sender=Recording)
def delete_pending_transcriptions_cache(instance, **kwargs):
    print(f'Signal for deleting cache for pending transcriptions.')

    def execute_deletion_after_transaction():
        instance.delete_pending_recordings_cache()

    transaction.on_commit(execute_deletion_after_transaction)


@receiver([post_delete], sender=APIClient)
def delete_api_key_cache(instance, **kwargs):
    print(f'Signal for deleting api key cache.')

    def execute_deletion_after_transaction():
        instance.delete_api_key_cache()

    transaction.on_commit(execute_deletion_after_transaction)
