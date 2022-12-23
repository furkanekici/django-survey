from .models import Answer, Question

from .serializers import QuestionSerializer, AnswerSerializer
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class QuestionList(APIView):
    def get(self, request, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can view question" in users_group_permissions_list
            or request.user.is_superuser
        ):
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CreateQuestion(APIView):
    def post(self, request, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can add question" in users_group_permissions_list
            or request.user.is_superuser
        ):

            serializer = QuestionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class QuestionDetail(APIView):
    def get_object(self, pk):

        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can view question" in users_group_permissions_list
            or request.user.is_superuser
        ):
            question = self.get_object(pk)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ChangeQuestion(APIView):
    def get_object(self, pk):

        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can change question" in users_group_permissions_list
            or request.user.is_superuser
        ):
            question = self.get_object(pk)
            serializer = QuestionSerializer(question, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can delete question" in users_group_permissions_list
            or request.user.is_superuser
        ):
            question = self.get_object(pk)
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AnswerList(APIView):
    def get(self, request, pk, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can view answer" in users_group_permissions_list
            or request.user.is_superuser
        ):

            answers = Answer.objects.filter(toQuestion=pk)
            serializer = AnswerSerializer(answers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AnswerCreate(APIView):
    def update_participation_count(self, question):
        question.participationCount = question.answer_set.count()
        question.save()

    def update_yes_count(self, question):
        question.yesCount = question.answer_set.filter(responseText="yes").count()
        question.save()

    def update_no_count(self, question):
        question.noCount = question.answer_set.filter(responseText="no").count()
        question.save()

    def update_other_count(self, question):
        question.otherCount = (
            question.answer_set.exclude(responseText="yes")
            .exclude(responseText="no")
            .count()
        )
        question.save()

    def post(self, request, format=None):
        users_group_permissions_list = [
            permission.name
            for permission in request.user.groups.all()[0].permissions.all()
        ]
        if (
            "Can add answer" in users_group_permissions_list
            or request.user.is_superuser
        ):

            data = request.data
            serializer = AnswerSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                self.update_participation_count(
                    Question.objects.get(pk=data["toQuestion"])
                )
                if data["responseText"] == "yes":
                    self.update_yes_count(Question.objects.get(pk=data["toQuestion"]))
                elif data["responseText"] == "no":
                    self.update_no_count(Question.objects.get(pk=data["toQuestion"]))
                else:
                    self.update_other_count(Question.objects.get(pk=data["toQuestion"]))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
