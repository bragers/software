from django.views import generic
from .models import Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        queryset = Question.objects.all()

        for_kids = self.request.GET.get('for_kids')
        high_activity = self.request.GET.get('high_activity')

        if for_kids:
            queryset = queryset.filter(for_kids=True)

        if high_activity:
            queryset = queryset.filter(high_activity=True)

        return queryset.order_by("-pub_date")
