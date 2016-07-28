from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from distributors.models import Distributor, Section, UserProfile


class DistributorGroup(Distributor):
    GROUP_TYPES = (
        ('group', 'group'),
        ('page', 'public page'),
        ('event', 'event'),
    )
    IS_CLOSED_TYPES = (
        (0, 'open'),
        (1, 'closed'),
        (2, 'private'),
        )
    is_closed = models.PositiveIntegerField(_('Whether the community is closed'), choices=IS_CLOSED_TYPES, blank=True, null=True)
    type = models.CharField(max_length=5, choices=GROUP_TYPES, blank=True)
    members_count = models.PositiveIntegerField(blank=True, null=True)
    contacts = models.TextField(blank=True)
    user = models.ForeignKey(UserProfile, related_name='distributors_groups_of_user')

    class Meta:
        verbose_name = "Distributor group"
        verbose_name_plural = "Distributor groups"

    def get_absolute_url(self):
        return reverse('distributors:groups:distributor', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name