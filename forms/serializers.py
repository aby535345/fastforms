from rest_framework import serializers

from .models import created_forms, complited_forms

class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = created_forms
        fields = [
            'owner',
            'title',
            'content',
        ]
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = complited_forms
        fields = [
            'form_id',
            'respondent_id',
            'answer',
        ]
