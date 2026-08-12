from rest_framework import serializers

from .models import Dustbin



class DustbinSerializer(serializers.ModelSerializer):

    class Meta:

        model = Dustbin

        fields = "__all__"