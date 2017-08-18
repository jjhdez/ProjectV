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

from flask_restful import Resource
from flask import request, g
from v.tools.exception import ExceptionRest
from v.tools.v import processing_rest_exception, processing_rest_success, \
    type_of_insert_rest, type_of_update_rest
from v.tools.validate import validate_rest
from v.dream.model.dreamMdl import DreamMdl
from flask_babel import gettext, ngettext, _


class DreamListRst(Resource, DreamMdl):
    def get(self):
        try:
            _qrg = """
                SELECT array_to_json(array_agg(row_to_json(t) )) as collection
                FROM ( SELECT id, created_at, name, due_date_at, completed_at
                 FROM %s WHERE deleted_at is null and completed_at is null and create_id=%s )t;
                """ % (self._table, g.user.id,)
            g.db_conn.execute(_qrg)
            if g.db_conn.count() > 0:
                _collection = g.db_conn.one()[0]
                if _collection:
                    _data = {self._table: _collection}
                    _get = processing_rest_success(data=_data)
                else:
                    raise ExceptionRest(status_code=404, message=_("Not found record"))
            else:
                raise ExceptionRest(status_code=404, message=_("Not found record"))
        except (Exception, ExceptionRest), e:
            _get = processing_rest_exception(e)
        return _get

    def post(self):
        _request = request.json
        try:
            _errors = validate_rest(fields=self._fields, request=_request)
            if not _errors:
                _col, _val = type_of_insert_rest(self._fields, _request)
                _qrp = """
                    INSERT INTO %s (create_id , %s ) VALUES (%s, %s)
                    RETURNING (select row_to_json(collection) FROM (VALUES(id)) collection(id));
                """ % (self._table, _col, g.user.id, _val)
                g.db_conn.execute(_qrp)
                if g.db_conn.count() > 0:
                    _data = {self._table: g.db_conn.one()}
                    _post = processing_rest_success(data=_data, message=_('It was created correctly'), status_code=201)
                else:
                    raise ExceptionRest(status_code=500, message=_('Unable to register'))
            else:
                raise ExceptionRest(status_code=400, errors=_errors)
        except (Exception, ExceptionRest), e:
            _post = processing_rest_exception(e)
        return _post


class DreamRst(Resource, DreamMdl):
    def get(self, id):
        try:
            _qrg = """
                    SELECT array_to_json(array_agg(row_to_json(t) )) as collection
                    FROM ( SELECT id, created_at, name, due_date_at, completed_at FROM %s
                    WHERE deleted_at is null and completed_at is null and  create_id=%s and id = %s)t;
                """ % (self._table, g.user.id, id,)
            g.db_conn.execute(_qrg)
            if g.db_conn.count() > 0:
                _collection = g.db_conn.one()[0]
                if _collection:
                    _data = {self._table: _collection}
                    _get = processing_rest_success(data=_data)
                else:
                    raise ExceptionRest(status_code=404, message=_("Not found record"))
            else:
                raise ExceptionRest(status_code=404, message=_("Not found record"))
        except (Exception, ExceptionRest), e:
            _get = processing_rest_exception(e)
        return _get

    def put(self, id):
        _request = request.json
        try:
            _errors = validate_rest(fields=self._fields, request=_request, method='put')
            if not _errors:
                _val = type_of_update_rest(self._fields, _request)
                _qrp = "UPDATE %s SET %s WHERE id=%s;" % (self._table, _val, id,)
                g.db_conn.execute(_qrp)
                if g.db_conn.count() > 0:
                    _put = processing_rest_success(status_code=201, message=_("The record was successfully updated"))
                else:
                    raise ExceptionRest(status_code=404, message=_("Not found record"))
            else:
                raise ExceptionRest(status_code=400, errors=_errors)
        except (Exception, ExceptionRest), e:
            _put = processing_rest_exception(e)
        return _put

    def delete(self, id):
        try:
            _qrd = "UPDATE %s SET deleted_at=current_timestamp WHERE id=%s;" % (self._table, id,)
            g.db_conn.execute(_qrd)
            if g.db_conn.count() > 0:
                _delete = processing_rest_success(status_code=201, message=_("The record was successfully removed"))
            else:
                raise ExceptionRest(status_code=404,message=_("Not found record"))
        except (Exception, ExceptionRest), e:
            _delete = processing_rest_exception(e)
        return _delete
