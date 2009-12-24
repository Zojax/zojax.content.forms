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
from zope.i18nmessageid import MessageFactory
from zojax.wizard.interfaces import IWizard, IWizardStep

_ = MessageFactory('zojax.content.forms')


# content wizard steps
class IContentWizard(IWizard):
    """Content wizard"""


class IContentViewStep(IWizardStep):
    """ Content view step """


class IContentStep(IWizardStep):
    """Content step """


class ISecurityStep(IWizardStep):
    """Content security"""


class IPresentationStep(IWizardStep):
    """Presentation step."""


class IPublishStep(IWizardStep):
    """Publish step."""


# Add content wizard
class IAddContentWizard(IContentWizard):
    """ add content wizard """


# Edit content wizard
class IEditContentWizard(IContentWizard):
    """ edit content wizard """


# Content rename form
class IContentRenameForm(interface.Interface):
    """ rename content form """

    shortname = schema.TextLine(
        title = _(u'Short Name'),
        description = _(u'Should not contain spaces, underscores or mixed case. '
                        "Short Name is part of the item's web address."),
        required = False,
        missing_value = u'')


# Simple edit/add forms

class IContentAddView(interface.Interface):
    """ add content view """

    nameError = interface.Attribute('Name error')

    def getName(object=None):
        """ return name for new object """


class IContentEditView(interface.Interface):
    """ edit content view """

    nameError = interface.Attribute('Name error')

    formCancelMessage = interface.Attribute('Form cancel message')

    def cancelURL():
        """ cancel url """

    def getName():
        """ return name for new object """

    def allowRename():
        """ allow content renaming """


# additional marker interfaces

class IRedirectView(interface.Interface):
    """ """
