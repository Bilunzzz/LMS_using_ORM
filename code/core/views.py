from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg, Count
from core.models import Course, CourseContent, CourseMember, Comment

# Create your views here.
def index(request):
    return HttpResponse("<h1>Selamat datang di LMS KITA</h1>")

def testing(request):
    guru = User.objects.create_user(username="guru_1", email="guru_1t@email.com", 
                         password="rahasia", first_name="Guru", last_name="Satu")
    
    Course.objects.create(
        name="Pemrograman Python",
        description="Belajar Pemrograman Python", 
        price=500000,
        teacher=guru
    )
    
    return HttpResponse("<h1>Kosongan</h1>")

def allCourses(request):
    allCourses = Course.objects.all().select_related('teacher')
    data_resp = []
    for course in allCourses:
        record = {'id': course.id, 'name': course.name, 
                  'price': course.price,
                  'teacher': {
                      'id': course.teacher.id,
                      'username': course.teacher.username,
                      'email': course.teacher.email,
                      'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
                  }}
        data_resp.append(record)
    return JsonResponse(data_resp, safe=False)

def userProfile(request, user_id):
    user = User.objects.get(pk=user_id)
    courses = Course.objects.filter(teacher=user)
    data_resp = {'username': user.username, 'email': user.email, 
              'fullname': f"{user.first_name} {user.last_name}"}
    data_resp['courses'] = []
    for course in courses:
        course_data = {'id': course.id, 'name': course.name, 
                  'description': course.description, 'price': course.price}
        data_resp['courses'].append(course_data)
    return JsonResponse(data_resp, safe=False)

def courseStats(request):
    courses = Course.objects.all()
    stats = courses.aggregate(  course_count=Count('*'),
                                max_price=Max('price'),
                                min_price=Min('price'),
                                avg_price=Avg('price'))
    cheapest_list = courses.filter(price=stats['min_price'])
    expensive_list = courses.filter(price=stats['max_price'])
    popullar_list = courses.annotate(member_count=Count('coursemember')).order_by('-member_count')[:3]
    unpopullah_list = courses.annotate(member_count=Count('coursemember')).order_by('member_count')[:3]
    result = {
        'course_count': stats['course_count'],
        'min_price': stats['min_price'],
        'max_price': stats['max_price'],
        'avg_price': stats['avg_price'],
        'cheapest': [course.name for course in cheapest_list],
        'expensive': [course.name for course in expensive_list],
        'popular': [course.name for course in popullar_list],
        'unpopular': [course.name for course in unpopullah_list],
    }
    return JsonResponse(result, safe=False)

def userStats(request):
    users_with_courses = User.objects.annotate(course_count=Count('course')).filter(course_count__gt=0).count()
    users_without_courses = User.objects.annotate(course_count=Count('course')).filter(course_count=0).count()
    avg_courses_per_user = CourseMember.objects.values('user_id').annotate(course_count=Count('course_id')).aggregate(avg_course_count=Avg('course_count'))['avg_course_count']
    user_with_most_courses = User.objects.annotate(course_count=Count('coursemember')).order_by('-course_count').first()
    user_with_most_courses_data = {
        'username': user_with_most_courses.username,
        'course_count': user_with_most_courses.course_count
    } if user_with_most_courses else None
    
    users_without_courses_list = User.objects.annotate(course_count=Count('coursemember')).filter(course_count=0)
    users_without_courses_list_data = [{'username': user.username} for user in users_without_courses_list]
    
    result = {
        'users_with_courses': users_with_courses,
        'users_without_courses': users_without_courses,
        'avg_courses_per_user': avg_courses_per_user,
        'user_with_most_courses': user_with_most_courses_data,
        'users_without_courses_list': users_without_courses_list_data
    }
    
    return JsonResponse(result, safe=False)