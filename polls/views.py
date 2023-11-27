# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Article
from .forms import ArticleFilterForm


class ArticleListView(ListView):
    model = Article
    template_name = 'polls/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10  # Set the number of articles per page

    def get_queryset(self):
        queryset = super().get_queryset()

        form = ArticleFilterForm(self.request.GET)
        if form.is_valid():
            location = form.cleaned_data.get('location')
            language = form.cleaned_data.get('language')
            for_kids = form.cleaned_data.get('for_kids')
            high_activity = form.cleaned_data.get('high_activity')
            free = form.cleaned_data.get('free')

            if location:
                queryset = queryset.filter(location=location)
            if language:
                queryset = queryset.filter(language=language)
            if for_kids is not None:
                queryset = queryset.filter(for_kids=for_kids)
            if high_activity is not None:
                queryset = queryset.filter(high_activity=high_activity)
            if free is not None:
                queryset = queryset.filter(free=free)

        return queryset.order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ArticleFilterForm(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


def handle_button_click(request, article_id, slot_id):
    article = get_object_or_404(Article, pk=article_id)
    remaining_count_field = f'slot{slot_id}_remaining_count'

    if getattr(article, remaining_count_field) > 0:
        # Update the remaining count
        setattr(article, remaining_count_field, getattr(article, remaining_count_field) - 1)
        article.save()
        return JsonResponse({'status': 'success', 'message': 'Påmeldt!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Maximum limit reached'}, status=400)


def process_payment(request):
    try:
        # Simulate successful payment
        response_data = {'status': 'success', 'message': 'Payment processed successfully'}
        return JsonResponse(response_data)
    except Exception as e:
        # Simulate an error during payment processing
        response_data = {'status': 'error', 'message': 'Payment processing error'}
        if getattr(process_payment, 'error_flag', False):
            raise Exception("Simulated error during payment processing")
        return JsonResponse(response_data, status=500)


def login_user(request):
    try:
        # Simulate successful login
        response_data = {'status': 'success', 'message': 'Login successful'}
        return JsonResponse(response_data)
    except Exception as e:
        # Simulate an error during login
        response_data = {'status': 'error', 'message': 'Login error'}
        return JsonResponse(response_data, status=500)
