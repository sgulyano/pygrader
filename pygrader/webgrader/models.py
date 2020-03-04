from django.db import models
from django.conf import settings

from ckeditor.fields import RichTextField
from .validators import validate_zip_ext

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import zipfile
import os
import shutil

class Problem(models.Model):
    VISIBLE = 1
    INVISIBLE = 0
    VISIBILITY_CHOICES = [
        (VISIBLE, 'Visible'),
        (INVISIBLE, 'Invisible')
    ]

    problem_title = models.CharField('Problem Title', max_length=200)
    problem_desc = RichTextField(config_name='Problem Description')
    pub_date = models.DateTimeField('Date Published')
    testcases = models.FileField(upload_to ='problems/', null=True, validators=[validate_zip_ext])

    cpu_limit = models.IntegerField(default=2)
    mem_limit = models.IntegerField(default=1024)
    max_score = models.IntegerField(default=100)
    visibility = models.IntegerField(default=1, choices=VISIBILITY_CHOICES)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.testcases:
            self.prev_testcases_path = self.testcases.path
        else:
            self.prev_testcases_path = None

    def __str__(self):
        return self.problem_title


# method for updating
@receiver(post_save, sender=Problem)
def update_stock(sender, instance, **kwargs):
    print('AA')
    print(instance.prev_testcases_path)

    # remove old file
    if instance.prev_testcases_path:
        os.remove(instance.prev_testcases_path)
        prev_folder, _ = os.path.splitext(instance.prev_testcases_path)
        shutil.rmtree(prev_folder)

    # extract
    print(instance.testcases.path)
    folder, ext = os.path.splitext(instance.testcases.path)
    assert(ext == '.zip')
    with zipfile.ZipFile(instance.testcases.path,"r") as zip_ref:
        zip_ref.extractall(folder)
    

@receiver(post_delete, sender=Problem)
def delete_file(sender, instance, *args, **kwargs):
    if instance.prev_testcases_path:
        os.remove(instance.prev_testcases_path)
        prev_folder, _ = os.path.splitext(instance.prev_testcases_path)
        shutil.rmtree(prev_folder)



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.id, filename)

class Submission(models.Model):
    problem = models.ForeignKey(Problem, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    src_code = models.FileField('Source Code', upload_to=user_directory_path)
    uploaded_at = models.DateTimeField('Date Submitted', auto_now_add=True)
    result = models.CharField('Result', max_length=200, default='')
    score = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id) + "-user_" + str(self.author.id) + "-pb" + str(self.problem.id)