# -*- coding: utf-8 -*-
# Copyright 2017 ProjectV Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class ProjectIssueMdl:
    _fields = {
        u'project_task_participed_id': {
            'required': True,
            'typeof': 'str',
        },
        u'assigned_user_id': {
            'required': True,
            'typeof': 'str',
        },
        u'name': {
            'required': True,
            'typeof': 'str',
        },
        u'description': {
            'typeof': 'str',
        },
        u'kind': {
            'typeof': 'str',
        },
        u'priority': {
            'typeof': 'str',
        },
        u'completed_at': {
            'typeof': 'datetime',
        }

    }
    _table = 'project_task_issues'

    def __init__(self):
        pass

    _query_get = """
        SELECT array_to_json(array_agg(row_to_json(t) )) as collection
                FROM ( SELECT id, project_task_participed_id, assigned_user_id, name, description,kind, priority, completed_at
                 FROM project_task_issues %s  )t;
    """