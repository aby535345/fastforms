from rest_framework import serializers

from .models import created_forms

class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = created_forms
        fields = [
            'owner',
            'title',
            'content',
        ]