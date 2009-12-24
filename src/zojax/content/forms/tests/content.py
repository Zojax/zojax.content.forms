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
from zope import schema, interface
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.content.type.container import ContentContainer


class IContent1(IItem):

    url = schema.TextLine(
        title = u'URL',
        required = False)


class IContent2(IItem):
    pass

class IContainer(interface.Interface):
    pass


class Content1(PersistentItem):
    interface.implements(IContent1)

class Content2(PersistentItem):
    interface.implements(IContent2)

class Container(ContentContainer):
    interface.implements(IContainer)
