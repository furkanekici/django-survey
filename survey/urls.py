from django.urls import path
from .views import (
    AnswerCreate,
    QuestionDetail,
    QuestionList,
    AnswerList,
    CreateQuestion,
    ChangeQuestion,
)

urlpatterns = [
    path("questions/list/", QuestionList.as_view()),
    path("questions/create/", CreateQuestion.as_view()),
    path("questions/read/<int:pk>/", QuestionDetail.as_view()),
    path("questions/write/<int:pk>/", ChangeQuestion.as_view()),
    path("answers/create/", AnswerCreate.as_view()),
    path("answers/list/<int:pk>/", AnswerList.as_view()),
]
