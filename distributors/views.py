from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages

from linker.settings import vk_api

from .models import Query, Section, UserProfile
from .mixins import LoginRequiredMixin
from people.models import DistributorPerson
from groups.models import DistributorGroup

import datetime


class Index(TemplateView):
    template_name = "distributors/index.html"


class DistributorListView(LoginRequiredMixin, ListView):
    model = DistributorPerson
    template_name = "distributors/distributors.html"
    context_object_name = 'distributors_persons'

    def get_queryset(self):
        return self.request.user.distributors_persons_of_user.all()

    def get_context_data(self, **kwargs):
        context = super(DistributorListView, self).get_context_data(**kwargs)
        context[
            'distributors_groups'] = self.request.user.distributors_groups_of_user.all()
        return context


class QueryListView(LoginRequiredMixin, ListView):
    model = Query
    template_name = "distributors/queries.html"
    context_object_name = 'queries'

    def get_queryset(self):
        return self.request.user.user_queries.all()


class QueryDetailView(DetailView):
    model = Query
    template_name = "distributors/query.html"
    context_object_name = 'query'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user_queries.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(QueryDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QueryDetailView, self).get_context_data(**kwargs)
        context['distributors_persons'] = self.request.user.distributors_persons_of_user.filter(
            distributors_persons_of_queries=self.object)
        context['distributors_groups'] = self.request.user.distributors_groups_of_user.filter(
            distributors_groups_of_queries=self.object)
        return context


class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    fields = ['title', 'query', 'description']
    template_name = "distributors/create_query.html"

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        section_pk = self.request.GET.get('section', None)
        if section_pk:
            try:
                section = Section.objects.get(pk=section_pk)
                self.object.section = section
            except ObjectDoesNotExist:
                pass
        self.object.save()
        vk_api_call = vk_api.newsfeed.search(
            q=form.cleaned_data['query'], extended=1, count=20)
        profiles = vk_api_call['profiles']
        groups = vk_api_call['groups']
        for person in profiles:
            try:
                p = self.request.user.distributors_persons_of_user.get(
                    vk_id=str(person['id']))
                p.save(pm=True)
                self.object.distributors_persons.add(p)
            except ObjectDoesNotExist:
                p = DistributorPerson(
                    name=person['first_name'], surname=person['last_name'], photo_url=person['photo_100'], vk_id=person['id'], user=self.request.user)
                p.save(pm=True)
                self.object.distributors_persons.add(p)
        for group in groups:
            try:
                g = self.request.user.distributors_groups_of_user.get(
                    vk_id=str(group['id']))
                g.save(pm=True)
                self.object.distributors_groups.add(g)
            except ObjectDoesNotExist:
                g = DistributorGroup(
                    name=group['name'], photo_url=group['photo_200'], vk_id=group['id'], user=self.request.user)
                g.save(pm=True)
                self.object.distributors_groups.add(g)
        self.request.user.save()
        self.object.save()
        messages.success(
            self.request, 'Запит \'{}\' було створено'.format(self.object))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, 'Щось трапилось не так. Зверніть увагу на вказівки.')
        return super(QueryCreateView, self).form_invalid(form)


class QueryDeleteView(DeleteView):
    model = Query
    success_url = reverse_lazy('distributors:queries')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user_queries.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(QueryDeleteView, self).dispatch(request, *args, **kwargs)


class SectionListView(LoginRequiredMixin, ListView):
    model = Section
    template_name = "distributors/sections.html"
    context_object_name = 'sections'

    def get_queryset(self):
        return self.request.user.user_sections.all()


class SectionDetailView(DetailView):
    model = Section
    template_name = "distributors/section.html"
    context_object_name = 'section'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user_sections.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(SectionDetailView, self).dispatch(request, *args, **kwargs)


class SectionCreateView(LoginRequiredMixin, CreateView):
    model = Section
    template_name = "distributors/create_section.html"
    fields = ['name']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(
            self.request, 'Секція \'{}\' була створена'.format(self.object))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(
            self.request, 'Щось трапилось не так. Зверніть увагу на вказівки.')
        return super(SectionCreateView, self).form_invalid(form)


class SectionDeleteView(DeleteView):
    model = Section
    success_url = reverse_lazy('distributors:sections')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user_sections.filter(pk=kwargs.get('pk', None)).exists():
            return HttpResponseForbidden()
        return super(SectionDeleteView, self).dispatch(request, *args, **kwargs)


@login_required
def my_favorite_distributors(request):
    pk = request.GET.get('pk', None)
    if pk is None:
        return render(request, 'distributors/distributors_list.html',
                      {'distributors_persons': request.user.distributors_persons_of_user.filter(favorite=True),
                       'distributors_groups': request.user.distributors_groups_of_user.filter(favorite=True)})
    return render(request, 'distributors/distributors_list.html', {'distributors_persons': request.user.distributors_persons_of_user.filter(distributors_persons_of_queries=get_object_or_404(Query, pk=pk)).filter(favorite=True),
                                                                   'distributors_groups': request.user.distributors_groups_of_user.filter(distributors_groups_of_queries=get_object_or_404(Query, pk=pk)).filter(favorite=True)})


@login_required
def all_distributors(request):
    pk = request.GET.get('pk', None)
    if pk is None:
        return render(request, 'distributors/distributors_list.html', {'distributors_persons': request.user.distributors_persons_of_user.all(),
                                                                       'distributors_groups': request.user.distributors_groups_of_user.all()})
    return render(request, 'distributors/distributors_list.html', {'distributors_persons': request.user.distributors_persons_of_user.filter(distributors_persons_of_queries=get_object_or_404(Query, pk=pk)),
                                                                   'distributors_groups': request.user.distributors_groups_of_user.filter(distributors_groups_of_queries=get_object_or_404(Query, pk=pk))})


@login_required
def by_mentions_distributors(request):
    pk = request.GET.get('pk', None)
    if pk is None:
        return render(request, 'distributors/distributors_list.html', {'distributors_persons': request.user.distributors_persons_of_user.order_by('-mentions'),
                                                                       'distributors_groups': request.user.distributors_groups_of_user.order_by('-mentions')})
    return render(request, 'distributors/distributors_list.html', {'distributors_persons': request.user.distributors_persons_of_user.filter(distributors_persons_of_queries=get_object_or_404(Query, pk=pk)).order_by('-mentions'),
                                                                   'distributors_groups': request.user.distributors_groups_of_user.filter(distributors_groups_of_queries=get_object_or_404(Query, pk=pk)).order_by('-mentions')})


@login_required
def search_dist(request):
    if request.method == 'GET':
        pk = request.GET.get('pk', None)
        if pk is None:
            query = request.GET.get('query').lower()
            if query:
                dist_persons_list = (dist for dist in request.user.distributors_persons_of_user.all(
                ) if query in dist.full_name.lower())
                dist_groups_list = request.user.distributors_groups_of_user.filter(
                    name__icontains=query)
            else:
                dist_persons_list = request.user.distributors_persons_of_user.all()
                dist_groups_list = request.user.distributors_groups_of_user.all()
            return render(request, 'distributors/distributors_list.html', {'distributors_persons': dist_persons_list,
                                                                           'distributors_groups': dist_groups_list})
        else:
            query = request.GET.get('query').lower()
            if query:
                dist_persons_list = (dist for dist in request.user.distributors_persons_of_user.filter(distributors_persons_of_queries=get_object_or_404(
                    Query, pk=pk)) if query in dist.full_name.lower())
                dist_groups_list = request.user.distributors_groups_of_user.filter(distributors_groups_of_queries=get_object_or_404(
                    Query, pk=pk)).filter(name__icontains=query)
            else:
                dist_persons_list = request.user.distributors_persons_of_user.filter(distributors_persons_of_queries=get_object_or_404(
                    Query, pk=pk))
                dist_groups_list = request.user.distributors_groups_of_user.filter(distributors_groups_of_queries=get_object_or_404(
                    Query, pk=pk))
            return render(request, 'distributors/distributors_list.html', {'distributors_persons': dist_persons_list,
                                                                           'distributors_groups': dist_groups_list})
