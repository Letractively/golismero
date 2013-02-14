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


from core.main.commonstructures import GlobalParams
from core.messaging.interfaces import IReceiver
from core.messaging.notifier import Notifier
from core.messaging.message import Message
from core.api.results.information.url import Url
from core.plugins.priscillapluginmanager import PriscillaPluginManager
from core.api.results.result import Result
from core.main.commonstructures import Singleton
from threading import Thread



#--------------------------------------------------------------------------
class Audit(IReceiver):
    """
    Instance of an audit, with their custom parameters, scope, target, plugins, etc.
    """

    #----------------------------------------------------------------------
    def __init__(self, auditParams, receiver):
        """
        :param receiver: Orchestrator instance that will recives messages sent by audit.
        :type reciber: Orchestrator

        :param auditParams: global params for an audit execution
        :type auditParams: GlobalParams
        """


        if not isinstance(auditParams, GlobalParams):
            raise TypeError("Expected GlobalParams, got %s instead" % type(auditParams))

        self.__audit_params = auditParams

        # set Receiver
        self.__receiver = receiver

        # set audit name
        self.name = self.__audit_params.audit_name

        # set audit as running
        self.__is_alive = True


    def get_name(self):
        return self.__auditname

    def set_name(self, name):
        if not name:
            self.__auditname = self.__generateAuditName()
        else:
            self.__auditname = name

    name = property(get_name, set_name)

    #----------------------------------------------------------------------
    def __generateAuditName(self):
        """
        Get a random name for an audit.

        :returns: str -- generated name for the audit.
        """
        import datetime

        return "golismero-".join(datetime.datetime.now().strftime("%Y-%m-%d-%H_%M"))


    #----------------------------------------------------------------------
    def get_audit_name(self):
        """
        Return the audit name.

        :returns: str -- the audit name
        """
        return self.__auditname


    #----------------------------------------------------------------------
    def run(self):
        """
        Start execution of an audit.
        """

        # 1 - Load neccesary plugins. Only testing plugins
        m_audit_plugins = PriscillaPluginManager().get_plugins(self.__audit_params.plugins, "testing")

        # 2 - Configure plugins to be it own the target of messages
        for p in m_audit_plugins:
            p.set_observer(self)

        # 3 - Creates and start the notifier
        self.__notifier = Notifier()
        self.__notifier.start()


        # 4 - Asociate plugins to nofitier
        for l_plugin in m_audit_plugins:
            self.__notifier.add_plugin(l_plugin)

        # 5 - Generate firsts messages with targets URLs
        for l_url in self.__audit_params.targets:
            self.__notifier.notify(Message(Url(l_url), Message.MSG_TYPE_INFO))



    #----------------------------------------------------------------------
    def get_is_alive(self):
        """
        Get info about the state of the audit. If the audit is not yet finished,
        returns True. False otherwise.

        :returns: bool -- True is audit is still running. False otherwise.
        """
        return self.__is_alive

    is_alive = property(get_is_alive)

    #----------------------------------------------------------------------
    def recv_msg(self, result_info):
        """
        Send a result to the core system.

        :param result_info: Result to receive
        :type result_info: Result
        """
        # Encapsulate Result information into a Message
        if isinstance(result_info, Result):
            # Build the message
            m_message = Message(result_info, Message.MSG_TYPE_INFO)
            # Send message to the core
            self.__receiver.recv_msg(m_message)

    #----------------------------------------------------------------------
    def send_msg(self, message):
        """
        Send message info to the plugins for this audit.

        :param message: The message to send.
        :type message: Message
        """
        if isinstance(message, Message):
            # Only resend to the plugins if information is info type
            if message.message_type is Message.MSG_TYPE_INFO:
                self.__notifier.notify(message)

    #----------------------------------------------------------------------
    def __get_is_finished(self):
        """
        Returns True if all plugins are finished. False otherwise.

        :returns: bool -- True if finished. False otherwise.
        """
        return self.__notifier.is_finished

    is_finished = property(__get_is_finished)



#--------------------------------------------------------------------------
class AuditManager(Singleton, IReceiver):
    """
    Manage and control audits.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """
        Constructor.
        """

        # Audits list
        self.__audits = dict()

    #----------------------------------------------------------------------
    def set_orchestrator(self, orchestrator):
        """
        Set the core object, manager of global messages.

        :param orchestrator: global manager. Instace of Orchestrator
        :type orchestrator: Orchestrator
        """
        if not isinstance(orchestrator, Orchestrator):
            raise TypeError("Expected Orchestrator, got %s instead" % type(orchestrator))
        self.__orchestrator = orchestrator


    #----------------------------------------------------------------------
    def new_audit(self, globalParams):
        """
        Creates a new audit with params passed as parameter

        :param globalParams: Params of audit
        :type globalParams: GlobalParams

        :returns: Audit -- return just created audit

        :raises: TypeError
        """
        if not isinstance(globalParams, GlobalParams):
            raise TypeError("Expected GlobalParams, got %s instead" % type(globalParams))

        # Create the audit
        m_audit = Audit(globalParams, self.__orchestrator)
        # Store it
        self.__audits[m_audit.get_audit_name()] = m_audit
        # Run!
        m_audit.run()

        # return it
        return m_audit


    #----------------------------------------------------------------------
    def get_all_audits(self):
        """
        Get the list of audits currently running.

        :returns: dicts(str, Audit) -- Return a dict with tuples (auditName, Audit instance)
        """
        return self.__audits

    #----------------------------------------------------------------------
    def get_audit(self, auditName):
        """
        Get an instance of Audit by its name.

        :param auditName: audit name
        :type auditName: str

        :returns: Audit -- instance of audit
        :raises: TypeError, KeyError
        """
        if not isinstance(auditName, basestring):
            raise TypeError("Audit name must be a string")

        return self.__audits[auditName]

    #----------------------------------------------------------------------
    def recv_msg(self, message):
        """
        Receive a message and resend it to all audits.

        :param message: inbound message
        :type message: Message
        """
        if isinstance(message, Message):
            for p in self.__audits.values():
                p.send_msg(message)

    #----------------------------------------------------------------------
    def __get_is_finished(self):
        """
        Returns True if all plugins are finished. False otherwise.

        :returns: bool -- True if finished. False otherwise.
        """
        for i in self.__audits.values():
            if i.is_finished is False:
                return False
        return True

    is_finished = property(__get_is_finished)
