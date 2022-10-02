from django.db import models
from django.contrib.auth.models import AbstractUser


class Faculty(models.Model):
    """ Stores Faculty information """

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    """ Stores department details """
    name = models.CharField(max_length=255, null=False, blank=False)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.name


class Subject(models.Model):
    """ Stores subject details """

    YEAR_1 = SEMESTER_1 = 1
    YEAR_2 = SEMESTER_2 = 2
    YEAR_3 = 3
    YEAR_4 = 4

    YEAR = [
        (YEAR_1, 'First Year'),
        (YEAR_2, 'Second Year'),
        (YEAR_3, 'Third Year'),
        (YEAR_4, 'Fourth Year')
    ]

    SEMESTER = [
        (SEMESTER_1, 'Semester I'),
        (SEMESTER_2, 'Semester II')
    ]

    subject_code = models.CharField(max_length=10, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    credit = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    year = models.PositiveSmallIntegerField(choices=YEAR, default=YEAR_1)
    semester = models.PositiveSmallIntegerField(choices=SEMESTER, default=SEMESTER_1)

    def __str__(self):
        return '{} {}'.format(self.subject_code, self.name)


class User(AbstractUser):
    """ User model additional fields """

    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.png', null=True, blank=True)
    subject = models.ManyToManyField(Subject, related_name='users', through='SubjectMark')

    def __str__(self):
        return self.username


class Grade(models.Model):
    """ Stores the grade and GPA points for the grade """

    AP = 1
    A = 2
    AM = 3
    BP = 4
    B = 5
    BM = 6
    CP = 7
    C = 8
    CM = 9
    DP = 10
    D = 11
    E = 12
    ABSENT = 13

    GRADE = [
        (AP, 'A+'),
        (A, 'A'),
        (BP, 'B+'),
        (B, 'B'),
        (CP, 'C+'),
        (C, 'C'),
        (CM, 'C-'),
        (DP, 'D+'),
        (D, 'D'),
        (E, 'E'),
        (ABSENT, 'Absent')
    ]

    faculty = models.ForeignKey(Faculty, null=False, blank=False, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(choices=GRADE, default=ABSENT, null=False, blank=False)
    gpa_point = models.DecimalField(max_digits=3, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.grade, self.faculty)


class SubjectMark(models.Model):
    """ Stores details about student results """

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    mark = models.ForeignKey(Grade, null=False, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '{} {} {}'.format(self.user, self.subject, self.mark)
