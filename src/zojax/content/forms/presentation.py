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
from zojax.wizard import WizardStepForm
from zojax.content.forms.interfaces import _, IPresentationStep


class ContentPresentationStep(WizardStepForm):
    interface.implements(IPresentationStep)

    name = u'presentation'
    title = _(u'Presentation')

    def isAvailable(self):
        if self.groups or self.subforms or self.forms or self.views:
            return super(ContentPresentationStep, self).isAvailable()

        return False
