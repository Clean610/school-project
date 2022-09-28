from rest_framework import serializers
from schools.models import Schools, Student


class SchoolViewSerializer(serializers.ModelSerializer):
     class Meta:
        model = Schools
        fields = '__all__'

class StudentViewSerializer(serializers.ModelSerializer):
    schools = SchoolViewSerializer()

    class Meta:
        model = Student
        fields = '__all__'
    
    