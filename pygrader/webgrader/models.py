from django.db import models
from django.conf import settings

class Problem(models.Model):
    problem_title = models.CharField('Problem Title', max_length=200)
    problem_desc = models.TextField('Problem Description')
    pub_date = models.DateTimeField('Date Published')
    visible = models.IntegerField(default=1)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.id, filename)

class Submission(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    src_code = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField('Date Submitted', auto_now_add=True)
    score = models.IntegerField(default=0)