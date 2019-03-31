from django.views.generic import ListView

from .models import Feedback


class FeedbackList(ListView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 5
    queryset = Feedback.objects.filter(is_active=True).prefetch_related(
        'residental_complex').prefetch_related(
        'residental_complex__type_of_complex'
    ).prefetch_related('social_media_links')
