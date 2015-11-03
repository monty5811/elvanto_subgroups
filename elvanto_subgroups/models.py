# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils import timezone

from elvanto_subgroups.elvanto import e_api


class ElvantoGroup(models.Model):
    name = models.CharField("Group Name", max_length=250)
    e_id = models.CharField("Elvanto ID", max_length=36)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @staticmethod
    def populate():
        data = e_api("groups/getAll", fields=['people'])
        if data['status'] == 'ok':
            for grp in data['groups']['group']:
                grp_obj = ElvantoGroup.objects.get(e_id=grp["id"])
                grp_obj.group_members.clear()
                if len(grp['people']) > 0:
                    for x in grp['people']['person']:
                        prsn = ElvantoPerson.objects.get(e_id=x['id'])
                        prsn.elvanto_groups.add(grp_obj)
                        prsn.save()

    @staticmethod
    def pull():
        """
        Pull all elvanto groups and create entries in local db.
        """
        data = e_api("groups/getAll")
        for e_grp in data['groups']['group']:
            grp, created = ElvantoGroup.objects.get_or_create(e_id=e_grp['id'])
            grp.name = e_grp['name'].encode('utf-8', 'replace').strip()
            grp.save()


class ElvantoPerson(models.Model):
    e_id = models.CharField("Elvanto ID", max_length=36)
    first_name = models.CharField("First Name", max_length=250)
    preferred_name = models.CharField("Preferred Name", max_length=250, blank=True)
    last_name = models.CharField("Last Name", max_length=250)
    elvanto_groups = models.ManyToManyField(ElvantoGroup, blank=True, related_name='group_members')

    def full_name(self):
        if self.preferred_name == '':
            return "{0} {1}".format(self.first_name, self.last_name)
        else:
            return "{0} {1}".format(self.preferred_name, self.last_name)

    def __str__(self):
        return self.full_name()

    @staticmethod
    def pull():
        """
        Pull all elvanto people into db, then pull down groups to add people.
        Then iterate through them to add them to the correct groups
        """
        data = e_api("people/getAll",
                     page_size=settings.ELVANTO_PEOPLE_PAGE_SIZE)

        people = data['people']
        num_synced = people["on_this_page"]
        page = 2
        while num_synced < people["total"]:
            more_data = e_api("people/getAll",
                              page_size=settings.ELVANTO_PEOPLE_PAGE_SIZE,
                              page=page)
            for person in more_data["people"]["person"]:
                people["person"].append(person)
            num_synced += more_data["people"]["on_this_page"]
            page += 1

        for e_prsn in people['person']:
            prsn, created = ElvantoPerson.objects.get_or_create(e_id=e_prsn['id'])
            prsn.first_name = e_prsn['firstname'].strip()
            prsn.preferred_name = e_prsn['preferred_name'].strip()
            prsn.last_name = e_prsn['lastname'].strip()
            prsn.save()

    class Meta:
        ordering = ['last_name', 'first_name']


class Link(models.Model):
    main_group = models.OneToOneField(
        ElvantoGroup,
        related_name='main_group'
    )
    sub_groups = models.ManyToManyField(
        ElvantoGroup,
        related_name='sub_groups',
        limit_choices_to={'main_group__isnull': True},
    )
    last_sync = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.main_group)

    @property
    def get_absolute_url(self):
        return reverse_lazy('link_update', args=[self.pk])

    @property
    def get_delete_url(self):
        return reverse_lazy('link_delete', args=[self.pk])

    @property
    def is_circular(self):
        return self.main_group in self.sub_groups.all()

    def add_people(self, ids_to_add=None):
        if ids_to_add is None:
            return

        print(
            'Adding {0} to {1}'.format(
                str(ids_to_add),
                str(self.main_group)
            )
        )
        for p_id in ids_to_add:
            e_api(
                "groups/addPerson",
                id=self.main_group.e_id,
                person_id=p_id
            )

    def remove_people(self, ids_to_remove=None):
        if ids_to_remove is None:
            return

        print(
            'Removing {0} from {1}'.format(
                str(ids_to_remove),
                str(self.main_group)
            )
        )
        for p_id in ids_to_remove:
            e_api(
                "groups/removePerson",
                id=self.main_group.e_id,
                person_id=p_id
            )

    def sync(self):
        if self.is_circular:
            print('This group is linked with itself, do not sync it!')
            return
        # fetch people in big group
        main_group_ppl_ids = self.main_group.group_members.all(
        ).values_list(
            'e_id',
            flat=True
        )
        # aggregate people in sub groups
        all_sub_group_ids = list()
        for subgroup in self.sub_groups.all():
            sub_group_ppl_ids = subgroup.group_members.all(
            ).values_list(
                'e_id',
                flat=True
            )
            all_sub_group_ids += sub_group_ppl_ids

        # compare groups
        main_group_ppl_ids = set(main_group_ppl_ids)
        all_sub_group_ids = set(all_sub_group_ids)

        if main_group_ppl_ids == all_sub_group_ids:
            # groups are already synced
            return
        else:
            people_to_remove = main_group_ppl_ids - all_sub_group_ids
            self.remove_people(
                ids_to_remove=people_to_remove
            )
            people_to_add = all_sub_group_ids - main_group_ppl_ids
            self.add_people(
                ids_to_add=people_to_add
            )

        self.last_sync = timezone.now()
        # TODO sync other meta data, e.g. picture, location, etc

    @staticmethod
    def sync_all():
        for link in Link.objects.all():
            link.sync()
