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
from zope.schema import getFieldNames
from zope.security.checker import canWrite
from zope.cachedescriptors.property import Lazy

from zojax.wizard import WizardStepForm
from zojax.wizard.interfaces import ISaveable
from zojax.content.type.interfaces import IItem, IContentType
from zojax.layoutform import Fields, PageletEditSubForm

from interfaces import _, IContentStep


class ContentStep(WizardStepForm):
    interface.implements(ISaveable, IContentStep)

    name = 'content'
    title = _('Content')
    label = _('Modify content')

    @Lazy
    def fields(self):
        content = self.getContent()
        item = IItem(content, None)
        if item is None:
            return Fields()

        fields = Fields(IItem)

        if not canWrite(content, 'title'):
            fields = fields.omit('title')

        if not canWrite(content, 'description'):
            fields = fields.omit('description')

        return fields

    def isAvailable(self):
        if not (self.groups or self.subforms or self.forms or self.views):
            return bool(self.fields)

        return super(ContentStep, self).isAvailable()


class ContentBasicFields(PageletEditSubForm):

    @Lazy
    def fields(self):
        ct = IContentType(self.context, None)
        if ct is not None:
            return Fields(ct.schema).omit('title', 'description')
        else:
            return Fields()

    def isAvailable(self):
        if not self.fields:
            return False
        return True

    def getContent(self):
        return self.context
