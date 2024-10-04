from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, TemplateView

from app_transcription.forms import RecordingCreateForm, APIClientCreateForm
from app_transcription.models import Recording, APIClient


class RecordingsListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard.html'
    model = Recording
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_recordings'] = Recording.objects.filter(user=self.request.user)

        online_status = cache.get('computing_server_online')
        context['online_status'] = online_status

        if cache.get('computing_server_online') == 1:
            print('server online')

        return context


class RecordingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'app_transcription/create_recording.html'
    model = Recording
    form_class = RecordingCreateForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        if form.is_valid():
            new_recording = form.save(commit=False)
            new_recording.name = new_recording.name.title()
            new_recording.user = self.request.user
            new_recording.save()
        return super().form_valid(form)


class RecordingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'app_transcription/detail_recording.html'
    model = Recording

    def get(self, request, *args, **kwargs):
        recording = Recording.objects.filter(id=self.kwargs['pk']).first()
        if not recording:
            return redirect('dashboard')
        user = self.request.user

        if recording.user != user:
            return redirect('dashboard')

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class RecordingDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'app_transcription/delete_recording.html'
    model = Recording
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):
        recording = Recording.objects.filter(id=self.kwargs['pk']).first()
        if not recording:
            return redirect('dashboard')
        user = self.request.user

        if recording.user != user:
            return redirect('dashboard')

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class APIClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'app_transcription/create_api_client.html'
    model = APIClient
    form_class = APIClientCreateForm
    success_url = reverse_lazy('api_clients_list')
    permission_required = 'app_transcription.api_manage'


class APIClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'app_transcription/api_client_list.html'
    model = APIClient
    context_object_name = 'all_api_clients'
    permission_required = 'app_transcription.api_manage'


class APIClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'app_transcription/delete_api_client.html'
    model = APIClient
    success_url = reverse_lazy('api_clients_list')
    permission_required = 'app_transcription.api_manage'


class AboutView(TemplateView):
    template_name = 'about.html'
