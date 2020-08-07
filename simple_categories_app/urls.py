from django.urls import path

from simple_categories_app.views import CategoryDetailsView, CategoryView

urlpatterns = [
    path('<category_id>/', CategoryDetailsView.as_view(), name='categories_details'),
    path('', CategoryView.as_view(), name='categories'),
]
