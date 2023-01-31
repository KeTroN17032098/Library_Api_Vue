from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class library_spot(models.Model):
    sportname = models.CharField(max_length=255,unique=True,blank=False)

class member(models.Model):
    name = models.CharField(_('Name'), max_length=20,blank=True)
    libraryid=models.CharField(_('Library ID'), max_length=50,blank=True)
    count=models.IntegerField(_('Count'),default=1)
    where=models.ManyToManyField('library_spot',verbose_name=_('place where this person caught'),blank=True)
    description=models.TextField(_('Description'),blank=True)
    created_on=models.DateTimeField(_('Created Time'),auto_now_add=True)
    modified_on=models.DateTimeField(_('Modified Time'),auto_now=True)