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
from zojax.wizard.button import WizardButton
from zojax.wizard.interfaces import ISaveable, IPreviousAction, IForwardAction
from zojax.layoutform.interfaces import ISaveAction, ICancelAction

from interfaces import _


previous = WizardButton(
    title = _(u'Previous'),
    condition = lambda form: not form.isFirstStep(),
    weight = 100,
    provides = IPreviousAction)

savenext = WizardButton(
    title = _(u'Save & Next'),
    condition = lambda form: not form.isLastStep() \
        and form.step.isSaveable(),
    weight = 200,
    provides = (IForwardAction, ISaveAction))

next = WizardButton(
    title = _(u'Next'),
    condition = lambda form: not form.isLastStep() \
        and not form.step.isSaveable(),
    weight = 300,
    provides = IForwardAction)

save = WizardButton(
    title = _(u'Save'),
    condition = lambda form: form.step.isSaveable(),
    weight = 400,
    provides = ISaveAction)

cancel = WizardButton(
    title=_(u'Cancel'),
    weight = 500,
    condition = lambda form: form.hasViewStep(),
    provides = ICancelAction)
