from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, User


class Section(models.Model):
    name = models.CharField(_('name'), max_length=200)
    user = models.ForeignKey(
        'distributors.UserProfile', related_name='user_sections')

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('distributors:section', kwargs={'pk': self.pk})


class Distributor(models.Model):

    name = models.CharField(_('name'), max_length=50)

    description = models.TextField(blank=True)
    mentions = models.PositiveIntegerField(
        _('number of mentions'), default=0, blank=True)
    photo_url = models.URLField(_('photo'), null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    vk_id = models.CharField(
        _('vk id'), blank=True, max_length=15)
    favorite = models.BooleanField(_('favorite'), default=False)

    class Meta:
        abstract = True

    def save(self, pm=False, *args, **kwargs):
        if pm == True:
            self.mentions += 1
        return super(Distributor, self).save(*args, **kwargs)


class Query(models.Model):
    title = models.CharField(_('title'), max_length=200)
    query = models.CharField(_('query'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    added = models.DateTimeField(
        _('date when the person was added'), auto_now_add=True)
    distributors_persons = models.ManyToManyField(
        'people.DistributorPerson', blank=True, related_name='distributors_persons_of_queries')
    distributors_groups = models.ManyToManyField(
        'groups.DistributorGroup', blank=True, related_name='distributors_groups_of_queries')
    user = models.ForeignKey(
        'distributors.UserProfile', related_name='user_queries')
    section = models.ForeignKey(Section, related_name='section_queries', blank=True, null=True)

    class Meta:
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('distributors:query', kwargs={'pk': self.pk})


class UserProfile(AbstractUser):
    pass
