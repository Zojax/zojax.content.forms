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
from zope.security.checker import canAccess
from zope.traversing.browser import absoluteURL
from zope.cachedescriptors.property import Lazy
from zope.app.container.interfaces import \
     IAdding, IWriteContainer, IContainerNamesContainer, INameChooser
from zope.copypastemove.interfaces import IContainerItemRenamer

from zojax.layoutform.interfaces import \
    IAddButton, ISaveButton, ICancelButton
from zojax.layoutform import button, Fields, PageletAddForm, PageletEditForm

from zojax.statusmessage.interfaces import IStatusMessage

from zojax.content.type.interfaces import IContentType
from zojax.content.type.interfaces import IContentViewView
from zojax.content.type.interfaces import IRenameNotAllowed
from zojax.content.forms.interfaces import _, IContentAddView, IContentEditView

from formvalidator import ContentNameError


class AddForm(PageletAddForm):
    interface.implements(IContentAddView)

    _addedObject = None
    nameError = None
    prefix = 'content.add.'
    id = 'content-forms-add'
    formCancelMessage = _(u'Content creation has been canceled.')

    @Lazy
    def fields(self):
        return Fields(self.context.schema, omitReadOnly=True)

    @property
    def label(self):
        return self.context.title

    @property
    def description(self):
        return self.context.description

    def create(self, data):
        return self.context.create(**data)

    def getName(self, object=None):
        return self.request.get('add_input_name', '')

    def add(self, object):
        name = self.getName(object)

        if IContentType.providedBy(self.context):
            ob = self.context.add(object, name)

        elif IAdding.providedBy(self.context):
            self.context.contentName = name
            ob = self.context.add(object)

        else:
            raise ValueError("Can't add content.")

        self._addedObject = ob
        return ob

    @button.buttonAndHandler(_(u'Add'), name='add', provides=IAddButton)
    def handleAdd(self, action):
        data, errors = self.extractData()

        if errors:
            errors = [error for error in errors
                      if not error.error.__class__ == ContentNameError]

            IStatusMessage(self.request).add(
                [self.formErrorsMessage] + errors, 'formError')
        else:
            obj = self.createAndAdd(data)

            if obj is not None:
                self._addedObject = obj
                self._finishedAdd = True
                self.redirect(self.nextURL())

    @button.buttonAndHandler(_(u'Cancel'),
                             name='cancel', provides=ICancelButton)
    def handleCancel(self, action):
        self._finishedAdd = True
        self.redirect(self.cancelURL())
        IStatusMessage(self.request).add(self.formCancelMessage)

    def nextURL(self):
        viewName = queryMultiAdapter(
            (self._addedObject, self.request), IContentViewView)
        if viewName is not None:
            return '%s/%s'%(
                absoluteURL(self._addedObject, self.request), viewName.name)
        else:
            return '%s/'%absoluteURL(self._addedObject, self.request)

    def cancelURL(self):
        context = self.context.__parent__.__parent__
        return '%s/'%absoluteURL(context, self.request)

    def nameAllowed(self):
        """Return whether names can be input by the user."""
        context = self.context

        if IContentType.providedBy(context):
            context = context.context

        if IAdding.providedBy(context):
            context = context.context

        if IWriteContainer.providedBy(context):
            return not IContainerNamesContainer.providedBy(context)
        else:
            return False


class EditForm(PageletEditForm):
    interface.implements(IContentEditView)

    nameError = None
    successMessage = _('Content has been successfully updated.')
    formCancelMessage = _(u'Edit action has been canceled.')

    @Lazy
    def contentType(self):
        return IContentType(self.context)

    @property
    def label(self):
        return self.contentType.title

    @property
    def description(self):
        return self.contentType.description

    @Lazy
    def fields(self):
        return Fields(self.contentType.schema, omitReadOnly=True)

    @button.buttonAndHandler(
        _(u'Save'), name='save', provides=ISaveButton)
    def handleApply(self, action):
        context = self.context
        request = self.request

        data, errors = self.extractData()
        if errors:
            errors = [error for error in errors
                      if not error.error.__class__ == ContentNameError]

            IStatusMessage(self.request).add(
                [self.formErrorsMessage] + errors, 'formError')
        else:
            changes = self.applyChanges(data)

            if self.allowRename():
                newName = self.getName()
                if newName != context.__name__:
                    renamer = IContainerItemRenamer(context.__parent__)
                    renamer.renameItem(context.__name__, newName)
                    changes = True

            if changes:
                IStatusMessage(request).add(self.successMessage)
            else:
                IStatusMessage(request).add(self.noChangesMessage)

            nextURL = self.nextURL()
            if nextURL:
                self.redirect(nextURL)

    @button.buttonAndHandler(
        _(u'Cancel'), name='cancel', provides=ICancelButton)
    def handleCancel(self, action):
        self.redirect(self.cancelURL())
        IStatusMessage(self.request).add(self.formCancelMessage)

    def nextURL(self):
        viewName = queryMultiAdapter(
            (self.context, self.request), IContentViewView)
        if viewName is not None:
            return '%s/%s'%(
                absoluteURL(self.context, self.request), viewName.name)
        else:
            return '%s/'%absoluteURL(self.context, self.request)

    def cancelURL(self):
        viewName = queryMultiAdapter(
            (self.context, self.request), IContentViewView)
        if viewName is not None:
            return '%s/%s'%(
                absoluteURL(self.context, self.request), viewName.name)
        else:
            return '%s/'%absoluteURL(self.context, self.request)

    def getName(self):
        return self.request.get('edit_input_name', '')

    def allowRename(self):
        if IRenameNotAllowed.providedBy(self.context):
            return False

        container = self.context.__parent__
        return (IWriteContainer.providedBy(container) and
                not IContainerNamesContainer.providedBy(container) and
                canAccess(container, '__setitem__'))
