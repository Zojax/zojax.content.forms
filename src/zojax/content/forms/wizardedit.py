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
import string

from zope import interface, component, schema, event
from zope.proxy import sameProxiedObjects
from zope.security import checkPermission
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.traversing.interfaces import IContainmentRoot
from zope.exceptions.interfaces import UserError
from zope.app.component.interfaces import ISite
from zope.lifecycleevent import ObjectModifiedEvent
from zope.app.container.interfaces import \
    IWriteContainer, IContainerNamesContainer, INameChooser
from zope.copypastemove.interfaces import IContainerItemRenamer

from z3c.form import validator
from z3c.form.error import ErrorViewSnippet

from zojax.wizard import WizardWithTabs
from zojax.layoutform import button, Fields
from zojax.layoutform.interfaces import ISaveAction
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.content.type.interfaces import \
    IContentContainer, IContentViewView, IRenameNotAllowed, IContentNamesContainer

from content import ContentStep
from interfaces import _, IRedirectView
from interfaces import IEditContentWizard, IContentRenameForm


class EditContentWizard(WizardWithTabs):
    interface.implements(IEditContentWizard)

    label = _('Modify')
    prefix = 'content.edit.'
    id = 'content-forms-edit'
    handlers = WizardWithTabs.handlers.copy()

    formCancelMessage = _(u'Edit action has been canceled.')

    @property
    def title(self):
        return getattr(self.context, 'title', self.context.__name__)

    @property
    def description(self):
        return getattr(self.context, 'description', u'')

    @property
    def fields(self):
        if self.step.name != 'content' or \
                not isinstance(self.step, ContentStep):
            return Fields()

        context = self.context

        if not ISite.providedBy(context):
            if IRenameNotAllowed.providedBy(context):
                return Fields()

            if not IContentNamesContainer.providedBy(context):
                location = context.__parent__
                if IWriteContainer.providedBy(location) and \
                        not IContainerNamesContainer.providedBy(location):
                    return Fields(IContentRenameForm)

        return Fields()

    def updateDefaultStep(self, defaultStep=''):
        if not defaultStep:
            for step in self.steps:
                if not IRedirectView.providedBy(step):
                    self.step = step
                    return
                if self.steps:
                    self.step = self.steps[0]
        else:
            super(EditContentWizard, self).updateDefaultStep(defaultStep)

    @button.handler(ISaveAction)
    def handleApply(self, action):
        context = self.context
        request = self.request

        data, errors = self.extractData()
        if errors:
            errors = [error for error in errors
                      if not isinstance(error.error, NameError)]

            IStatusMessage(self.request).add(
                [self.formErrorsMessage] + errors, 'formError')
            return

        if not self.step.isComplete():
            return

        if 'shortname' in data:
            shortname = data['shortname']
            if shortname != context.__name__:
                valid_chars = "-.%s%s" % (string.lowercase, string.digits)
                shortname = shortname.lower()
                shortname = ''.join(c for c in shortname if c in valid_chars)
                data['shortname'] = shortname
                if shortname != context.__name__:
                    renamer = IContainerItemRenamer(context.__parent__)
                    renamer.renameItem(context.__name__, shortname)
                    event.notify(ObjectModifiedEvent(context))

                context = context.__parent__[shortname]
                self.redirect(
                    '%s/%s/'%(absoluteURL(context, request), self.__name__))

    def cancelURL(self):
        viewName = queryMultiAdapter(
            (self.context, self.request), IContentViewView)
        if viewName is not None:
            return '%s/%s'%(
                absoluteURL(self.context, self.request), viewName.name)
        else:
            return '%s/'%absoluteURL(self.context, self.request)

    def hasViewStep(self):
        return 'view' in self.stepsByName

    def upperContainer(self):
        request = self.request
        vhr = request.getVirtualHostRoot()
        parent = getattr(self.context, '__parent__', None)

        while True:
            if (parent is None or
                sameProxiedObjects(parent, vhr) or
                IContainmentRoot.providedBy(parent)):
                return None

            if IContentContainer.providedBy(parent):
                url = absoluteURL(parent, request)

                if checkPermission('zojax.ModifyContent', parent):
                    return '%s/@@context.html'%url

                viewName = queryMultiAdapter((parent,request), IContentViewView)
                if viewName:
                    return '%s/%s'%(url, viewName.name)

                return '%s/'%url
            else:
                parent = getattr(parent, '__parent__', None)


class EditContentRename(object):
    component.adapts(interface.Interface)
    interface.implements(IContentRenameForm)

    def __init__(self, context):
        self.context = context

    @property
    def shortname(self):
        return self.context.__name__


class NameError(schema.ValidationError):
    __doc__ = _(u'Content name already in use.')

    def __init__(self, msg):
        self.message = msg


class NameErrorViewSnippet(ErrorViewSnippet):

    def update(self):
        self.message = self.error.message


class ContentNameValidator(validator.InvariantsValidator):
    component.adapts(
        interface.Interface,
        interface.Interface,
        EditContentWizard,
        interface.Interface,
        interface.Interface)

    def validate(self, data):
        form = self.view
        if 'shortname' not in form.widgets:
            return super(ContentNameValidator, self).validate(data)

        widget = form.widgets['shortname']

        if widget.error:
            return super(ContentNameValidator, self).validate(data)

        context = self.view.context
        shortname = data.get('shortname')

        if shortname == context.__name__:
            return super(ContentNameValidator, self).validate(data)

        errors = []
        chooser =  INameChooser(context.__parent__)

        try:
            chooser.checkName(shortname, None)
        except (UserError, ValueError), err:
            exc = NameError(unicode(err))

            widget.error = NameErrorViewSnippet(
                exc, self.request, widget, widget.field, form, self.context)
            widget.error.update()
            errors.append(exc)

        return tuple(errors) + super(ContentNameValidator, self).validate(data)
