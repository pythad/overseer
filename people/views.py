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

from .models import DistributorPerson


class DistributorPersonDetailView(DetailView):
    model = DistributorPerson
    template_name = "people/distributor.html"
    context_object_name = 'distributor'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.distributors_persons_of_user.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(DistributorPersonDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DistributorPersonDetailView, self).get_context_data(**kwargs)
        context['in_queries'] = self.object.distributors_persons_of_queries.all()
        return context


class DistributorPersonUpdateView(UpdateView):
    model = DistributorPerson
    fields = ['name', 'surname', 'bdate', 'address', 'm_number', 'description']
    template_name = "distributors/distributors_edit.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.distributors_persons_of_user.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(DistributorPersonUpdateView, self).dispatch(request, *args, **kwargs)


@require_POST
@login_required
def update_distributor(request):
    pk = request.POST.get('pk')
    if not request.user.distributors_persons_of_user.filter(pk=pk).exists():
        return HttpResponseForbidden()
    distributor = get_object_or_404(DistributorPerson, pk=pk)
    person = vk_api.users.get(
        user_id=distributor.vk_id, fields='sex, bdate, home_town, photo_max_orig, contacts')[0]
    context = {}
    if not distributor.bdate:
        try:
            bdate = datetime.datetime.strptime(
                person['bdate'], '%d.%m.%Y').strftime('%Y-%m-%d')
            distributor.bdate = bdate
            context['bdate'] = bdate
        except Exception:
            pass
    if not distributor.address:
        try:
            distributor.address = person['home_town']
            context['address'] = person['home_town']
        except Exception:
            pass
    try:
        distributor.photo_url = person['photo_max_orig']
        context['photo_url'] = person['photo_max_orig']
    except Exception:
        pass
    if not distributor.m_number:
        try:
            distributor.m_number = person['contacts']['mobile_phone']
            context['m_number'] = person['contacts']['mobile_phone']
        except Exception:
            pass
    distributor.save()
    return JsonResponse(context)


@require_POST
@login_required
def favorite_distributor(request):
    pk = request.POST.get('pk')
    if not request.user.distributors_persons_of_user.filter(pk=pk).exists():
        return HttpResponseForbidden()
    distributor = get_object_or_404(DistributorPerson, pk=pk)
    distributor.favorite = not distributor.favorite
    distributor.save()
    return HttpResponse()