from rest_framework.response import Response
from rest_framework import status 
from django.shortcuts import get_object_or_404
from schools.models import Schools, Student
from schools.serializers import SchoolViewSerializer ,StudentViewSerializer
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist


class SchoolsViewSet(ViewSet):
    queryset = Schools.objects.all()
    serializer_class = SchoolViewSerializer
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        school = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(school)
        return Response(serializer.data)
    
    def update(self, request, pk=None):

        school = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(school, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):

        school = get_object_or_404(self.queryset, pk=pk)
        school.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class studentViewSet(ViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentViewSerializer
    
    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        schools = request.data.get('schools')
        student_in_school = Student.objects.filter(schools=schools).count()
        schools = Schools.objects.get(pk=schools)
        
        if student_in_school >= schools.number_of_student:
            return Response({'message': "Cannot add more student in this school."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        school = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(school)
        return Response(serializer.data)
    

    def update(self, request, pk=None):

        student = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None):

        student = get_object_or_404(self.queryset, pk=pk)
        student.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    
class RetrieveStudentBySchoolViewSet(ViewSet):
    
    serializer_class = StudentViewSerializer
    def list(self, request, schools_pk=None):

        student = Student.objects.filter(schools=schools_pk)
        serializer = self.serializer_class(student, many=True)
        
        return Response(serializer.data)

    
    def create(self, request, schools_pk=None):
        
        student_in_school = Student.objects.filter(schools=schools_pk).count()
        try:
            schools = Schools.objects.get(pk=schools_pk)
        except ObjectDoesNotExist:
            return Response({'message': "School dose not existed"}, status=status.HTTP_400_BAD_REQUEST)
        
        if student_in_school >= schools.number_of_student:
            return Response({'message': "Cannot add more student in this school."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            request.data.pop('schools')
        
        except KeyError:
            pass
 
        data = {**request.data, "schools": schools_pk}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def retrieve(self, request, schools_pk=None, pk=None):
  
        student = Student.objects.filter(pk=pk, schools=schools_pk).first()
       
        if student:
            serializer = self.serializer_class(student)
            return Response(serializer.data)
        
        return Response({'message': "Student dose not existed."}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, schools_pk=None, pk=None):

        student = Student.objects.filter(pk=pk, schools=schools_pk).first()
       
        if student:

            serializer = self.serializer_class(student, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        
        return Response({'message': "Student dose not existed."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, schools_pk=None, pk=None):
        
        student = Student.objects.filter(pk=pk, schools=schools_pk).first()
        
        if student:
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
         
        return Response({'message': "Student dose not existed."}, status=status.HTTP_400_BAD_REQUEST)

        

   
   
   
   
   
   
   
   
   
