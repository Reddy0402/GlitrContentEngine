from rest_framework import serializers
from myapp.models import Jobs


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"
         read_only_fields = [
            "id",
            "generated_prompt",
            "generated_image",
            "status",
            "created_at",
            "updated_at",
        ]