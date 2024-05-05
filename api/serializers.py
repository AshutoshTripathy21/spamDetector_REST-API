from rest_framework import serializers
from .models import User, Contact, Spam

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'email', 'password']

class ContactSerializer(serializers.ModelSerializer):
    is_spam = serializers.SerializerMethodField()
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'is_spam']

    def get_is_spam(self, obj):
        return Spam.objects.filter(number=obj.phone_number).exists()

class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ['id', 'number', 'marked_by']

class UserLoginSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)