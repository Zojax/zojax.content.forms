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
from zope.app.component.interfaces import ISite

from zojax.layoutform import Fields
from zojax.wizard import WizardStepForm
from zojax.wizard.interfaces import ISaveable
from zojax.content.type.interfaces import IItemPublishing
from zojax.content.forms.interfaces import _, IPublishStep


class ContentPublishStep(WizardStepForm):
    interface.implements(ISaveable, IPublishStep)

    name = u'publish'
    title = _(u'Publish')
    label = _(u'Publish content')

    fields = Fields(IItemPublishing)
