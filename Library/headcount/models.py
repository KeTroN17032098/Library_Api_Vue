from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.conf import settings
# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=255,blank=False,unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        
class SubPlace(models.Model):
    place = models.ForeignKey(Place,related_name="subplace",on_delete=models.CASCADE,verbose_name=_("Place originated"))
    name = models.CharField(max_length=255,blank=False)
    
    def __str__(self):
        return self.place.name+"_"+self.name
    
    class Meta:
        verbose_name = _("Subplace")
        verbose_name_plural = _("Subplaces")
    
class DailyCount(models.Model):
    subplace=models.ForeignKey(SubPlace,related_name="dailycount",on_delete=models.CASCADE,verbose_name=_("Subplace originated"))
    date=models.DateField(_("Count Date"),default=datetime.date.today())
    male=models.PositiveIntegerField(_("Male Count"),default=0)
    female=models.PositiveIntegerField(_("Male Count"),default=0)
    created_on=models.DateTimeField(_('Created Time'),auto_now_add=True)
    modified_on=models.DateTimeField(_('Modified Time'),auto_now=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,verbose_name=_("Who Created"),related_name="dailycount_createdby")
    modified_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,verbose_name=_("Who Modified"),related_name="dailycount_modifiedby")
    
    def __str__(self):
        return self.subplace.name+"_"+self.date.strftime("%Y-%m-%d")

    class Meta:
        verbose_name = _("Dailycount")
        verbose_name_plural = _("Dailycounts")