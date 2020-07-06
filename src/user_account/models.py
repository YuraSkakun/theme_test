from django.db import models

# Create your models here.

import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models import Max, Sum


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.PositiveIntegerField(null=True, blank=True)
    number_tests_passed = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)

    def update_score(self):
        points = self.test_results.aggregate(points=Sum('avr_score')).get('points', 0.0)
        self.avr_score = points / self.test_results.count()

    def count_passed_tests(self):
        return self.test_results.filter(is_completed=True).count()

    def total_score(self):
        return self.avr_score

    def percent_success_passed(self):
        percent_success_passed = sum([test.percent_correct_answers() for test in
                                      self.test_results.filter(is_completed=True)])
        return round(percent_success_passed, 2)

    def test_last_run(self):
        last_run = self.test_results.last()  # order_by('-id').first()
        # return last_run.datetime_run
        if last_run:
            return last_run.datetime_run
        return ''
