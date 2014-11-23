#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import abc

class ServerState():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def handle(self, server_instance):
		raise NotImplemented("Please implement handle")
