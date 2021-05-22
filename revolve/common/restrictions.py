from django.db.models import Q

from databases.models import Database
from groups.models import Group
from projects.models import Project

ACCOUNT_MAPPING = {
    0: "TRIAL_ACCOUNT",
    1: "BASIC_ACCOUNT",
    2: "PREMIUM_ACCOUNT"
}

PROJECT_RESTRICTIONS = {
    "TRIAL_ACCOUNT": 1,
    "BASIC_ACCOUNT": 5,
    "PREMIUM_ACCOUNT": 0
}

DATABASE_RESTRICTIONS = {
    "TRIAL_ACCOUNT": 0,
    "BASIC_ACCOUNT": 3,
    "PREMIUM_ACCOUNT": 'unlimited'
}

GROUPS_RESTRICTIONS = {
    "TRIAL_ACCOUNT": 0,
    "BASIC_ACCOUNT": 3,
    "PREMIUM_ACCOUNT": 'unlimited'
}


def get_value_by_key(value, dict):
    return dict[value]


def check_projects_restrictions(auth):
    projects = Project.objects.filter(owner=auth)
    account_type = get_value_by_key(auth.account_type, ACCOUNT_MAPPING)
    projects_restriction = get_value_by_key(account_type, PROJECT_RESTRICTIONS)

    if projects_restriction == 0:
        return True, 'unlimited', account_type

    if projects_restriction > len(projects):
        return True, projects_restriction - len(projects), account_type

    return False, 0, account_type


def check_database_restrictions(auth):
    databases = Database.objects.filter(owner=auth)
    account_type = get_value_by_key(auth.account_type, ACCOUNT_MAPPING)
    database_restriction = get_value_by_key(account_type, DATABASE_RESTRICTIONS)

    if database_restriction == 0:
        return False, 0, account_type

    if database_restriction == 'unlimited':
        return True, 'unlimited', account_type

    if database_restriction > len(databases):
        return True, database_restriction - len(databases), account_type

    return False, 0, account_type


def check_groups_restrictions(auth):
    groups = Group.objects.filter(Q(owner=auth) | Q(users=auth))
    account_type = get_value_by_key(auth.account_type, ACCOUNT_MAPPING)
    groups_restriction = get_value_by_key(account_type, GROUPS_RESTRICTIONS)

    if groups_restriction == 0:
        return False, 0, account_type

    if groups_restriction == 'unlimited':
        return True, 'unlimited', account_type

    if groups_restriction > len(groups):
        return True, groups_restriction - len(groups), account_type

    return False, 0, account_type
