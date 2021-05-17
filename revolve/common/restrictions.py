from databases.models import Database
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
    "PREMIUM_ACCOUNT": 1
}


def get_value_by_key(value, dict):
    return dict[value]


def check_projects_restrictions(auth):
    projects = Project.objects.filter(owner=auth)
    account_type = get_value_by_key(auth.account_type, ACCOUNT_MAPPING)
    projects_restriction = get_value_by_key(account_type, PROJECT_RESTRICTIONS)

    if projects_restriction == 0:
        return True

    if projects_restriction < len(projects):
        return True

    return False


def check_database_restrictions(auth):
    databases = Database.objects.filter(owner=auth)
    account_type = get_value_by_key(auth.account_type, ACCOUNT_MAPPING)
    check_database_restriction = get_value_by_key(account_type, DATABASE_RESTRICTIONS)

    if check_database_restriction == 0:
        return False

    if check_database_restriction == 1:
        return True

    if check_database_restriction < len(databases):
        return True

    return False

# def check_predictions_restrictions(auth):
   