from flask_table import Table, BoolCol, DatetimeCol, Col, ButtonCol
from flask import url_for


# Nodes
class NodesTable(Table):
    classes = ['pure-table']
    allow_sort = True
    unique_id = Col('Unique ID')
    api_key = Col('API Key')
    owner = Col('Owner')
    active = BoolCol('Active')
    created = DatetimeCol('Create Date')
    updated = DatetimeCol('Updated Date')
    delete = ButtonCol('Delete', 'delete_node', url_kwargs=dict(id='id'),
                       button_attrs={'class': 'pure-button button-error'})
    disable = ButtonCol('Disable', 'disable_node', url_kwargs=dict(id='id'),
                       button_attrs={'class': 'pure-button button-secondary'})
    regen = ButtonCol('Regen API Key', 'regen_node_api', url_kwargs=dict(id='id'),
                      button_attrs={'class': 'pure-button button-secondary'})

    def sort_url(self, col_key, reverse=False):
        if col_key == 'delete' or col_key == 'regen' or col_key == 'disable':
            col_key = 'id'
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('nodes', sort=col_key, direction=direction)


class Node(object):
    def __init__(self, unique_id, api_key, owner, active, created, updated):
        self.unique_id = unique_id
        self.api_key = api_key
        self.owner = owner
        self.active = active
        self.created = created
        self.updated = updated


# Invites
class InviteTable(Table):
    classes = ['pure-table']
    allow_sort = True
    invite_code = Col('Invite Code')
    created_by = Col('Created By')
    active = BoolCol('Active')
    created = DatetimeCol('Create Date')
    updated = DatetimeCol('Updated Date')
    delete = ButtonCol('Delete', 'delete_invite', url_kwargs=dict(id='id'),
                       button_attrs={'class': 'pure-button button-error'})
    disable = ButtonCol('Disable', 'disable_invite', url_kwargs=dict(id='id'),
                        button_attrs={'class': 'pure-button button-secondary'})

    def sort_url(self, col_key, reverse=False):
        if col_key == 'delete' or col_key == 'regen' or col_key == 'disable':
            col_key = 'id'
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('invites', sort=col_key, direction=direction)


class Invite(object):
    def __init__(self, invite_code, active):
        self.invite_code = invite_code
        self.active = active


# Users
class UsersTable(Table):
    classes = ['pure-table']
    allow_sort = True
    username = Col('Invite Code')
    role = Col('Created By')
    active = BoolCol('Active')
    created = DatetimeCol('Create Date')
    updated = DatetimeCol('Updated Date')
    delete = ButtonCol('Delete', 'delete_user', url_kwargs=dict(id='id'),
                       button_attrs={'class': 'pure-button button-error'})
    disable = ButtonCol('Disable', 'disable_user', url_kwargs=dict(id='id'),
                        button_attrs={'class': 'pure-button button-secondary'})
    gen_pass = ButtonCol('New Password', 'regen_password', url_kwargs=dict(id='id'),
                         button_attrs={'class': 'pure-button button-secondary'})

    def sort_url(self, col_key, reverse=False):
        if col_key == 'delete' or col_key == 'disable' or col_key == 'gen_pass':
            col_key = 'id'
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('invites', sort=col_key, direction=direction)


class Users(object):
    def __init__(self, username, active):
        self.username = username
        self.active = active
