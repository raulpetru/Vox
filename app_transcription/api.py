import json

from django.core.cache import cache
from ninja import NinjaAPI, Schema
from ninja.security import APIKeyHeader

from app_transcription.models import APIClient, Recording

api = NinjaAPI(docs_url=None)


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            if not cache.get(f'cached_api_key_{key}'):
                cache.set(f'cached_api_key_{key}', APIClient.objects.get(api_key=key))
            return cache.get(f'cached_api_key_{key}')
        except APIClient.DoesNotExist:
            pass


header_key = ApiKey()


@api.get("/pending_transcriptions", auth=header_key)
def pending_transcriptions(request):
    assert isinstance(request.auth, APIClient)

    if not cache.get('pending_transcriptions_cache'):
        first_in_queue = Recording.objects.filter(transcription_status='Pending').order_by('upload_date_time').first()
        if first_in_queue:
            new_pending_list = {f'{first_in_queue.id}': f'{request.build_absolute_uri(first_in_queue.audio_file.url)}'}
            cache.set('pending_transcriptions_cache', new_pending_list)
        else:
            cache.set('pending_transcriptions_cache', json.dumps({}))
    return cache.get('pending_transcriptions_cache')


class Transcript(Schema):
    id: int
    data: str


@api.post('/transcript', auth=header_key)
def load_transcript(request, transcript: Transcript):
    assert isinstance(request.auth, APIClient)

    recording = Recording.objects.filter(id=transcript.id).first()
    if not recording.transcription_status == 'Processed':
        recording.transcription_data = transcript.data
        recording.transcription_status = 'Processed'
        recording.save()


@api.post('/computing-server-online', auth=header_key)
def computing_server_online(request):
    assert isinstance(request.auth, APIClient)

    cache.set('computing_server_online', 1, 35)
