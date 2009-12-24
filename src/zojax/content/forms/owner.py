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
from zope import interface, schema
from zope.security import checkPermission

from zojax.principal.field import UserField
from zojax.layoutform.interfaces import ICancelButton
from zojax.layoutform import \
    button, Fields, PageletForm, PageletEditForm, PageletEditSubForm
from zojax.ownership.interfaces import IOwnership
from zojax.ownership.interfaces import IInheritOwnership, IUnchangeableOwnership
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _


class OwnerInformation(PageletEditSubForm):

    def getOwner(self):
        owner = IOwnership(self.context).owner
        if owner is None:
            return {'title': _('Unknown principal'), 'desc': ''}
        else:
            return {'title': owner.title, 'desc': owner.description}

    def isAvailable(self):
        if checkPermission('zojax.changeOwnership', self.context):
            return not (IInheritOwnership.providedBy(self.context) or
                        IUnchangeableOwnership.providedBy(self.context))
        return False

    def postUpdate(self):
        pass


class IChangeOwnerForm(interface.Interface):

    owner = UserField(
        title = _(u"Owner"),
        description = _(u"Select new owner for content."),
        required = True)


class ChangeOwner(PageletEditForm):

    label = _(u'Change content owner')
    fields = Fields(IChangeOwnerForm)

    buttons = PageletEditForm.buttons.copy()
    handlers = PageletEditForm.handlers.copy()

    def update(self):
        super(ChangeOwner, self).update()

    def applyChanges(self, data):
        owner = IOwnership(self.context.getContent())
        if owner.ownerId != data['owner']:
            owner.ownerId = data['owner']
            return True
        else:
            return False

    def getContent(self):
        return {'owner': IOwnership(self.context.getContent()).ownerId}

    @button.buttonAndHandler(_('Back'), provides=ICancelButton)
    def handleBack(self, action):
        self.redirect('./')
