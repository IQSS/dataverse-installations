import json
from collections import OrderedDict

from django.db.models import F

from dv_apps.dataverses.models import Dataverse

"""
quit()
python manage.py shell
from dv_apps.metrics.dataverse_tree_util import *
get_selected_dataverse_ids(['Handwashing'])
"""

class DataverseTreeUtil(object):

    def __init__(self):
        pass

    def get_selected_dataverse_ids(self, dv_alias_list, include_child_dvs=True):
        """Based on the aliases passed into "selected_dvs",
        find the "id" values for these Dataverses
            - Additional, add sub Dataverses if "include_child_dvs" is True
        """
        if dv_alias_list is None or len(dv_alias_list)==0:
            return True, None # Look across all Dataverses

        # Retrieve ids of the selected Dataverses
        #
        first_cut_ids = Dataverse.objects.select_related('dvobject'\
                    ).annotate(id=F('dvobject'), owner_id=F('dvobject__owner__id')\
                    ).filter(alias__in=dv_alias_list\
                    ).values('id', 'owner_id')

        if len(first_cut_ids) == 0:
            if len(dv_alias_list) == 1:
                emsg = "This Dataverse alias was not found: \"%s\"" % dv_alias_list[0]
            else:
                fmt_alias_list = [ '"%s"' % x for x in dv_alias_list]
                emsg = "These Dataverse aliases were not found: %s" % ', '.join(fmt_alias_list)
            return False, emsg

        first_cut_id_list = [x['id'] for x in first_cut_ids]

        print 'first_cut_id_list', len(first_cut_id_list), first_cut_id_list
        # Include child dvs?
        #
        if not include_child_dvs:
            # No, just return what you have
            return True, first_cut_id_list

        # Yes, include child dvs

        # Is the root included?
        if len([x for x in first_cut_ids if x['owner_id'] is None]) > 0:
            # Yes! # Look across all Dataverses
            return True, None

        # Nope, need to look at the full Dataversetree
        full_tree = self.get_dataverse_tree_dict()

        # Check through tree, looking
        additional_ids = self.get_subtree_child_ids(full_tree, first_cut_id_list)
        print 'additional_ids', len(additional_ids), additional_ids

        all_ids = first_cut_id_list + additional_ids

        return True, all_ids


    def get_subtree_child_ids(self, tree_info, selected_ids, id_list=None, gather_all=False):
        """
        For any subtree, recursively return all of the "id"s and child "id"s
            {
                "name": "Malawi (2015) SIFPO formative study",
                "id": 2668913,
                "depth": 11,
                "children": [
                    {
                        "name": "Malawi (2015) Mosquito net durability study",
                        "id": 2668914,
                        "depth": 12,
                        "children": [
                            {
                                "depth": 13,
                                "id": 2668915,
                                "name": "Malawi (2015) Mystery client and client exit study"
                            }
                        ]
                    }
                ]
            }
        """
        #print 'get_subtree_child_ids. current:', tree_info['id'], 'selected:', selected_ids, id_list, gather_all
        if id_list is None:
            id_list = []

        # Is the tree's id in selected_ids?
        if tree_info['id'] in selected_ids or gather_all:
            # Yes, get that id
            id_list.append(tree_info['id'])

            # And get all child ids
            for child_tree in tree_info.get('children', []):
                self.get_subtree_child_ids(child_tree, selected_ids, id_list, gather_all=True)
        else:
            # Nope, just keep checking
            for child_tree in tree_info.get('children', []):
                self.get_subtree_child_ids(child_tree, selected_ids, id_list)

        return id_list



    def get_dataverse_tree_dict(self, skip_flat_dataverses=True):
        """Return JSON with the Datavese "tree" -- e.g. parent/child relations
        By default, don't show Dataverses that don't have any child Dataverses
        """

        # Note: "F(..) allows aliasing of a field.  e.g. SELECT dvobject as id,...
        dvs = Dataverse.objects.select_related('dvobject'\
                ).annotate(id=F('dvobject'), parent_id=F('dvobject__owner__id')\
                ).values('id', 'parent_id', 'name', 'alias'
                ).all(\
                ).order_by('name')

        parent_child_lists = {} #{ parent_id : [ info, info, info ]}
        root_node = None
        for dv_info in dvs:
            if dv_info['parent_id'] is None:
                root_node = dv_info
            else:
                parent_child_lists.setdefault(dv_info['parent_id'], []).append(dv_info)

        #print parent_child_lists
        #print 'root_node', root_node

        full_tree = self.get_child_nodes(root_node, parent_child_lists)

        fmt_list = []
        for info in full_tree.get('children'):
            if skip_flat_dataverses:
                if info.has_key('children'):
                    fmt_list.append(info)
            else:
                fmt_list.append(info)

        full_tree['children'] = fmt_list

        return full_tree


    def get_child_nodes(self, root_node, parent_child_lists, depth=0):
        """
        Used to recursively organizing the Dataverse parent/child tree
        into a python OrderedDict
        """
        child_nodes = parent_child_lists.get(root_node['id'], None)

        # Are there child nodes?
        if not child_nodes:
            return OrderedDict(name=root_node['name'],\
                                alias=root_node['alias'],
                                id=root_node['id'],\
                                depth=depth)
            #return OrderedDict(name=root_node['name'], value=randint(400, 500), depth=depth)
        else:
            child_list = [] # create child list
            for cn in child_nodes:
                child_tree = self.get_child_nodes(cn, parent_child_lists, depth=depth+1)

                # limit to dataverses with sub dataverses
                if child_tree and len(child_tree) > 0:
                    child_list.append(child_tree)

            fmt_d = OrderedDict()
            fmt_d['name'] = root_node['name']
            fmt_d['alias'] = root_node['alias']
            fmt_d['id'] = root_node['id']
            fmt_d['depth'] = depth
            fmt_d['children'] = child_list
            return fmt_d
