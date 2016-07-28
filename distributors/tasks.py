from __future__ import absolute_import

from celery import shared_task

from linker.settings import vk_api
from .models import Query
from people.models import DistributorPerson
from groups.models import DistributorGroup


@shared_task
def update_queries():
    queries = Query.objects.all()
    for query in queries:
        vk_api_call = vk_api.newsfeed.search(
            q=query.query, extended=1, count=20)
        distributors_persons = vk_api_call['profiles']
        distributors_groups = vk_api_call['groups']
        q_distriburors_people_ids = [dist.vk_id for dist in query.distributors_persons.all()]
        q_distriburors_groups_ids = [dist.vk_id for dist in query.distributors_groups.all()]
        for person in distributors_persons:
            if not str(person['id']) in q_distriburors_people_ids:
                print(
                    '\nFound ' + ' ' + person['first_name'] + ' ' + person['last_name'])
                distributor_person = DistributorPerson(name=person['first_name'], surname=person[
                    'last_name'], photo_url=person['photo_100'], vk_id=person['id'], user=query.user)
                distributor_person.save(pm=True)
                if query.section:
                    distributor_person.section = query.section
                distributor_person.save()
                query.distributors_persons.add(distributor_person)
        for group in distributors_groups:
            if not str(group['id']) in q_distriburors_groups_ids:
                print(
                    '\nFound ' + ' ' + group['screen_name'])
                distributors_group = DistributorGroup(
                    name=group['name'], photo_url=group['photo_200'], vk_id=group['id'], user=query.user)
                distributors_group.save(pm=True)
                if query.section:
                    distributors_group.section = query.section
                distributors_group.save()
                query.distributors_groups.add(distributors_group)
        query.save()
