from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
# Create your models here.


class Thread(models.Model):
    title = models.CharField(_('Title'), max_length=100,blank=False)
    body=models.TextField(_('Body'))
    created_on=models.DateTimeField(_('Created Time'),auto_now_add=True)
    modified_on=models.DateTimeField(_('Modified Time'),auto_now=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,verbose_name=_("Who Created"),related_name="thread_createdby")
    modified_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,verbose_name=_("Who Modified"),related_name="thread_modifiedby")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")
        
class ThreadImage(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,verbose_name=_("Thread that owned this images"))
    image=ResizedImageField(force_format="WEBP",quality=75,upload_to='post_imgs/%Y/%m/%d/',null=True)
    def __str__(self):
        return self.thread.title+"_image_"+str(self.id)
    class Meta:
        verbose_name = _("ThreadImage")
        verbose_name_plural = _("ThreadImages")

class ThreadFile(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,verbose_name=_("Thread that owned this files"))
    file=models.FileField(verbose_name=_('File'), upload_to='files/%Y/%m/%d/', null=True)
    def __str__(self):
        return self.thread.title+"_file_"+str(self.id)
    class Meta:
        verbose_name = _("ThreadFile")
        verbose_name_plural = _("ThreadFiles")

class Comment(models.Model):
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,verbose_name=_("Thread that owned this comment"))
    body=models.TextField(_('Body'))
    created_on=models.DateTimeField(_('Created Time'),auto_now_add=True)
    modified_on=models.DateTimeField(_('Modified Time'),auto_now=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,verbose_name=_("Who Created"),related_name="comment_createdby")
    modified_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,verbose_name=_("Who Modified"),related_name="comment_modifiedby")
    
    def __str__(self):
        return self.thread.title+"_"+str(self.id)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")