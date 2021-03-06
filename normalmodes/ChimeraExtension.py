#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chimera
from chimera.dialogs import display


class NormalModesProdyEMO(chimera.extension.EMO):

	def name(self):
		return 'Tangram Normal Modes'

	def description(self):
		return 'Calculate normal modes of one molecule with ProDy'

	def categories(self):
		return ['InsiliChem']

	#def icon(self):
	#	return self.path("Template.png")

	def activate(self):
		self.module('gui').showUI()


emo = NormalModesProdyEMO(__file__)
chimera.extension.manager.registerExtension(emo)
