from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer


class RegisterSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        instance = User(**validated_data)
        instance.set_password(raw_password)
        instance.save()
        return instance
