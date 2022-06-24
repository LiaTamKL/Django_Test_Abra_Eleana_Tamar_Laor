from rest_framework.serializers import ModelSerializer , SlugRelatedField
from .models import *

def db_link(field):
        return SlugRelatedField(many=False,read_only=True,slug_field=field)


class AccountSerializer(ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    by_user = db_link("username")
    to_user = db_link("username")

    class Meta:
        model = Message
        fields = '__all__'