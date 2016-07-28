from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from distributors.models import Distributor, Section, UserProfile

class DistributorPerson(Distributor):
    surname = models.CharField(
        _('surname'), max_length=50, null=True, blank=True)

    bdate = models.DateField(_('birthday date'), null=True, blank=True)
    address = models.CharField(
        _('address'), max_length=200, null=True, blank=True)
    m_number = models.CharField(
        _('mobile number'), max_length=25, null=True, blank=True)
    user = models.ForeignKey(UserProfile, related_name='distributors_persons_of_user')

    class Meta:
        verbose_name = "Distributor"
        verbose_name_plural = "Distributors"
        ordering = ['added']

    def __str__(self):
        return self.name + ' ' + self.surname

    def get_absolute_url(self):
        return reverse('distributors:people:distributor', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return self.name + ' ' + self.surname
