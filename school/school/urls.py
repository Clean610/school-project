"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from cgitb import lookup
from django.contrib import admin
from django.urls import path, include
from schools import schools
from rest_framework_nested import routers



router = routers.DefaultRouter()
router.register(r'schools', schools.SchoolsViewSet, basename='schools')
router.register(r'students', schools.studentViewSet, basename='students')




school_router = routers.NestedSimpleRouter(router, r'schools', lookup='schools')
school_router.register(r'students', schools.RetrieveStudentBySchoolViewSet, basename='students_by_school')



urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(school_router.urls)),
]




