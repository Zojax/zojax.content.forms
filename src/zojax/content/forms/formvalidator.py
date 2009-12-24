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
from zope import schema, component, interface
from zope.exceptions.interfaces import UserError
from zope.app.container.interfaces import INameChooser

from z3c.form import validator

from interfaces import _
from interfaces import IContentAddView, IContentEditView
from zojax.content.type.interfaces import IEmptyNamesNotAllowed


class ContentNameError(schema.ValidationError):
    __doc__ = _(u'Content name already in use.')

    def __init__(self, msg):
        self.__doc__ = msg


class AddFormNameValidator(validator.InvariantsValidator):
    component.adapts(
        interface.Interface,
        interface.Interface,
        IContentAddView,
        interface.Interface,
        interface.Interface)

    def validate(self, data):
        if not self.view.nameAllowed():
            return super(AddFormNameValidator, self).validate(data)

        errors = []
        container = self.view.context.context

        # check content name
        chooser = INameChooser(container)

        name = self.view.getName(None)
        if name or IEmptyNamesNotAllowed.providedBy(container):
            try:
                chooser.checkName(name, None)
            except (UserError, ValueError), err:
                error = ContentNameError(unicode(err))
                errors.append(error)
                self.view.nameError = err

        return tuple(errors) + super(AddFormNameValidator, self).validate(data)


class EditFormNameValidator(validator.InvariantsValidator):
    component.adapts(
        interface.Interface,
        interface.Interface,
        IContentEditView,
        interface.Interface,
        interface.Interface)

    def validate(self, data):
        if not self.view.allowRename():
            return super(EditFormNameValidator, self).validate(data)

        name = self.view.getName()
        context = self.view.context

        if name == context.__name__:
            return super(EditFormNameValidator, self).validate(data)

        errors = []
        chooser =  INameChooser(self.context.__parent__)

        try:
            chooser.checkName(name, self.context)
        except Exception, err:
            error = ContentNameError(unicode(err))
            errors.append(error)
            self.view.nameError = err

        return tuple(errors) + super(EditFormNameValidator, self).validate(data)
