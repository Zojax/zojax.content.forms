##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.component import queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.publisher.browser import queryDefaultViewName

from zojax.wizard.step import WizardStep
from zojax.content.type.interfaces import IContentViewView
from zojax.content.forms.interfaces import IContentViewStep, IRedirectView


class ContentViewStep(WizardStep):
    interface.implements(IContentViewStep, IRedirectView)

    def render(self):
        context = self.context
        request = self.request
        url = absoluteURL(context, request)

        viewView = queryMultiAdapter(
            (self.context, request), IContentViewView)
        if viewView is not None:
            request.response.redirect('%s/%s'%(url, viewView.name))
        else:
            request.response.redirect('%s/'%url)

        return u''

    def isAvailable(self):
        name = queryDefaultViewName(self.context, self.request, None)
        if name == self.wizard.__name__:
            return False
        else:
            return super(ContentViewStep, self).isAvailable()
