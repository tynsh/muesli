# muesli/web/views.py
#
# This file is part of MUESLI.
#
# Copyright (C) 2011, Ansgar Burchardt <ansgar (at) 43-1.org>
# Copyright (C) 2011, Matthias Kuemmerer <matthias (at) matthias-k.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from muesli import models
from muesli.web.forms import *

from pyramid import security
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from pyramid.url import route_url
from sqlalchemy.orm import exc
from hashlib import sha1

import re
import os

@view_config(route_name='login', renderer='muesli.web:templates/login.pt')
def login(request):
  form = Form(UserLogin())
  if request.method == 'POST' and form.validate(request.POST):
    user = request.db.query(models.User).filter_by(email=form['email'], password=sha1(form['password']).hexdigest()).first()
    if user is not None:
      security.remember(request, user.id)
      request.user = user
  return { 'form': form, 'user': security.authenticated_userid(request) }

@view_config(route_name='logout', renderer='invest.measure.web:templates/logout.pt')
def logout(request):
  security.forget(request)
  request.session.invalidate()
  return {}

@view_config(route_name='overview', renderer='muesli.web:templates/overview.pt')
class Overview(object):
  def __init__(self, request):
    self.request = request
  def __call__(self):
    return {}