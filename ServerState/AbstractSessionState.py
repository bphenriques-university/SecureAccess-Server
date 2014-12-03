#!/usr/bin/python2
# -*- coding: UTF-8 -*-

import abc

class AbstractSessionState():
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def handle(self, session_manager):
		raise NotImplemented("Please implement handle")
