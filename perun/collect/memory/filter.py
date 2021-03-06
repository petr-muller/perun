"""This module provides methods for filtering the profile"""
import perun.collect.memory.parsing as parsing

__author__ = "Radim Podola"


def validate_profile(func):
    """ Validation decorator fro profile """
    def inner_decorator(profile, *args, **kwargs):
        """ Validate profile"""
        if 'snapshots' not in profile.keys():
            return {}
        if 'global' not in profile.keys():
            return {}
        # check if there is smt to remove
        try:
            glob_res = profile['global']['resources']
            if not glob_res:
                return profile
        except (IndexError, KeyError, TypeError):
            return {}

        return func(profile, *args, **kwargs)

    return inner_decorator


def remove_allocators(profile):
    """ Remove records in trace with direct allocation function

        Allocators are better to remove because they are
        in all traces. Removing them makes profile clearer.

    Arguments:
        profile(dict): dictionary including "snapshots" and
                       "global" sections in the profile

    Returns:
        dict: updated profile
    """
    allocators = ['malloc', 'calloc', 'realloc', 'free', 'memalign',
                  'posix_memalign', 'valloc', 'aligned_alloc']
    trace_filter(profile, function=allocators, source=[])

    return profile


@validate_profile
def trace_filter(profile, function, source):
    """ Remove records in trace section matching source or function
    Arguments:
        profile(dict): dictionary including "snapshots" and
                       "global" sections in the profile
        function(list): list of "function" records to omit
        source(list): list of "source" records to omit

    Returns:
        dict: updated profile
    """
    def determinate(call):
        """ Determinate expression """
        return (call['source'] not in source and
                call['function'] not in function)

    snapshots = profile['snapshots']
    for snapshot in snapshots:

        resources = snapshot['resources']
        for res in resources:
            # removing call records
            res['trace'] = [call for call in res['trace']
                            if determinate(call)]
            # updating "uid"
            res['uid'] = parsing.parse_allocation_location(res['trace'])

    return profile


def set_global_region(profile):
    """
    Arguments:
        profile(dict): partially computed profile
    """
    profile['global']['resources'] = {}


@validate_profile
def allocation_filter(profile, function, source):
    """ Remove record of specified function or source code out of the profile
    Arguments:
        profile(dict): dictionary including "snapshots" and
                       "global" sections in the profile
        function(list): function's name to remove record of
        source(list): source's name to remove record of

    Returns:
        dict: updated profile
    """
    def determinate(uid):
        """ Determinate expression """
        if not uid:
            return True
        if uid['function'] in function:
            return False
        if uid['source'] in source:
            return False
        return True

    snapshots = profile['snapshots']
    for snapshot in snapshots:
        snapshot['resources'] = [res for res in snapshot['resources'] if determinate(res['uid'])]
    set_global_region(profile)

    return profile


@validate_profile
def remove_uidless_records_from(profile):
    """ Remove record without UID out of the profile

    Arguments:
        profile(dict): dictionary including "snapshots" and
                       "global" sections in the profile

    Returns:
        dict: updated profile
    """
    snapshots = profile['snapshots']
    for snapshot in snapshots:
        snapshot['resources'] = [res for res in snapshot['resources'] if res['uid']]
    set_global_region(profile)

    return profile


if __name__ == "__main__":
    pass
