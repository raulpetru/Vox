from ninja import NinjaAPI, Schema
from ninja.security import APIKeyQuery

from app_transcription.models import APIClient, Recording

api = NinjaAPI()


class ApiKey(APIKeyQuery):
    param_name = "api_key"

    def authenticate(self, request, key):
        try:
            return APIClient.objects.get(api_key=key)
        except APIClient.DoesNotExist:
            pass


api_key = ApiKey()


@api.get("/pending_transcriptions", auth=api_key)
def pending_transcriptions(request):
    assert isinstance(request.auth, APIClient)

    pending_list = Recording.objects.filter(transcription_status='Pending').order_by('upload_date_time').all()
    new_pending_list = {f'{recording.id}': f'{request.build_absolute_uri(recording.audio_file.url)}' for recording in
                        pending_list}
    return new_pending_list


class Transcript(Schema):
    id: int
    data: str


@api.post('/transcript', auth=api_key)
def load_transcript(request, transcript: Transcript):
    assert isinstance(request.auth, APIClient)
    try:
        recording = Recording.objects.filter(id=transcript.id).first()
        recording.transcription_data = transcript.data
        recording.transcription_status = 'Processed'
        recording.save()
    except:
        pass
    return transcript
