#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Author: Daniel Garcia Garcia a.k.a cr0hn | dani@iniqua.com

Golismero project site: http://code.google.com/p/golismero/
Golismero project mail: golismero.project@gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from core.api.results.result import Result

#------------------------------------------------------------------------------
class Information(Result):
    """
    Abstract class for informational messages
    """

    #--------------------------------------------------------------------------
    #
    # Types of Infomation results
    #
    #--------------------------------------------------------------------------
    INFORMATION_IMAGE = 0
    INFORMATION_URL = 1
    INFORMATION_DOCUMENT = 2
    INFORMATION_BINARY = 3
    INFORMATION_MAIL = 4
    INFORMATION_UNKNOWN = 10


    #----------------------------------------------------------------------
    def __init__(self, information_type = None):
        """Constructor"""
        super(Information, self).__init__(Result.TYPE_INFORMATION)

        self.__information_type = information_type



    #----------------------------------------------------------------------
    def get_information_type(self):
        """
        Get the message type

        :returns: int -- The message type.
        """
        if self.__information_type is None:
            return Information.INFORMATION_URL
        else:
            return self.__information_type

    #----------------------------------------------------------------------
    def set_information_type(self, information_type):
        """
        Set the message type.

        :param result_type: The type of result
        :type result_type: int
        """
        if information_type is not None and information_type >= 0 and information_type <= 10:
            self.__information_type = information_type

    result_subtype = property(get_information_type, set_information_type)

