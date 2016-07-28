from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from distributors.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from linker.settings import vk_api


from .models import DistributorGroup


class DistributorGroupDetailView(DetailView):
    model = DistributorGroup
    template_name = "groups/distributor.html"
    context_object_name = 'distributor'

    @method_decorator(login_required(login_url="distributors:index"))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.distributors_groups_of_user.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(DistributorGroupDetailView, self).dispatch(request, *args, **kwargs)


class DistributorGroupUpdateView(UpdateView):
    model = DistributorGroup
    fields = ['name', 'description', 'contacts']
    template_name = "distributors/distributors_edit.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.distributors_groups_of_user.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(DistributorGroupUpdateView, self).dispatch(request, *args, **kwargs)


@require_POST
@login_required
def update_distributor(request):
    pk = request.POST.get('pk')
    if not request.user.distributors_groups_of_user.filter(pk=pk).exists():
        return HttpResponseForbidden()
    distributor = get_object_or_404(DistributorGroup, pk=pk)
    group = vk_api.groups.getById(
        group_id=distributor.vk_id, fields='members_count, description, contacts')[0]
    context = {}
    if not distributor.is_closed:
        try:
            is_closed = group['is_closed']
            distributor.is_closed = is_closed
            context['is_closed'] = is_closed
        except KeyError:
            pass
    if not distributor.type:
        try:
            distributor.type = group['type']
            context['type'] = group['type']
        except KeyError:
            pass
    if not distributor.members_count:
        try:
            distributor.members_count = group['members_count']
            context['members_count'] = group['members_count']
        except KeyError:
            pass
    if not distributor.description:
        try:
            distributor.description = group['description']
            context['description'] = group['description']
        except KeyError:
            pass
    if not distributor.contacts:
        try:
            distributor.contacts = group['contacts']
            context['contacts'] = group['contacts']
        except KeyError:
            pass
    distributor.save()
    return JsonResponse(context)


@require_POST
@login_required
def favorite_distributor(request):
    pk = request.POST.get('pk')
    if not request.user.distributors_groups_of_user.filter(pk=pk).exists():
        return HttpResponseForbidden()
    distributor = get_object_or_404(DistributorGroup, pk=pk)
    distributor.favorite = not distributor.favorite
    distributor.save()
    return HttpResponse()
