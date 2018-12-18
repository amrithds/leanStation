from rest_framework import serializers
from leanRestApis.models import ProjectActivity


class ProjectActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    project_id = serializers.IntegerField(required=True)
    activity_id = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    parent_project_activity_id = serializers.IntegerField(required=False)
    sequence=serializers.IntegerField(required=True)
    wbs_number=serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `ProjectActivity` instance, given the validated data.
        """
        return ProjectActivity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `ProjectActivity` instance, given the validated data.
        """
        instance.activity = validated_data.get('activity_id', instance.activity)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.parent_project_activity = validated_data.get('parent_id', instance.parent_project_activity)
        instance.sequence = validated_data.get('sequence', instance.sequence)
        instance.save()
        return instance