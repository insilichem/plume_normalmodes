# --- UCSF Chimera Copyright ---
# Copyright (c) 2006 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  This notice must be embedded in or
# attached to all copies, including partial copies, of the
# software or any revisions or derivations thereof.
# --- UCSF Chimera Copyright ---

import chimera
from chimera.baseDialog import ModelessDialog
import Pmw
import Tkinter
from Tkinter import *
from chimera.widgets import MoleculeScrolledListBox
import chimera.dialogs
from MMMD.gui import mmmdDialog


class NMProdyDialog(ModelessDialog):
    name = "Normal Modes Calculation (ProDy)"
    buttons = ("Run", "Close")
    lennard_jones = False
    mass_weighted = False

    def fillInUI(self, parent):
        self.proc = "std"
        parent.columnconfigure(1, weight=1)
        row = 0

        self.BackGround = None
        self.fixAtoms = None
        self.subspace = None

        self.AlgorithmMenu = Pmw.OptionMenu(parent,
                                            labelpos='w',
                                            label_text='Algorithm:',
                                            items=['Full atom', 'Residues', 'Mas'])

        self.AlgorithmDialog = Pmw.EntryField(parent,
                                              validate={'validator': 'numeric'},
                                              labelpos='w',
                                              label_text='n:',
                                              entry_width=5)

        self.AlgorithmMenu.grid(row=row, column=0, sticky='w')
        self.AlgorithmDialog.grid(row=row, column=1, sticky='ew', padx=5)

        row += 1

        #
        # Molecule Minimization
        #
        self.MPLabel = Tkinter.Label(parent,
                                     text="Minimize structure:")
        self.MPLabel.grid(column=0, row=row, sticky='w')
        self.MinimizerButton = Tkinter.Button(parent,
                                              text="Proceed",
                                              command=lambda: chimera.dialogs.display(
                                                  mmmdDialog.name))
        self.MinimizerButton.grid(column=1, row=row, sticky='w')
        row += 1

        #
        # Optional Selections: Lennard-Jones and mass-weighted hessian
        #

        self.options = Pmw.Group(parent, tag_text='Options')
        self.options.grid(column=0, row=row, columnspan=2, sticky='nsew')

        self.LennardJonesCheck = Pmw.RadioSelect(self.options.interior(),
                                                 buttontype='checkbutton',
                                                 command=self._lennard_jones)
        self.LennardJonesCheck.add('Lennard-Jones')
        self.LennardJonesCheck.grid(column=1, row=0, sticky='w')

        self.MassWeigthedCheck = Pmw.RadioSelect(self.options.interior(),
                                                 buttontype='checkbutton',
                                                 command=self._mass_weighted)
        self.MassWeigthedCheck.add('Mass weighted hessian')
        self.MassWeigthedCheck.grid(column=0, row=0, sticky='w')

        row += 1

        #
        # Model selection
        #
        self.molList = MoleculeScrolledListBox(parent,
                                               labelpos='w',
                                               label_text="Select model:   ",
                                               listbox_selectmode="extended")
        self.molList.grid(column=0, row=row, columnspan=2,
                          sticky='nsew')
        parent.rowconfigure(row, weight=1)
        row += 1

        #
        # Open gaussian modes
        #
        # self.gaussian = Pmw.Group(parent,tag_text='Open gaussian output file')
        # self.gaussian.grid(column=0, row=row, columnspan=2, sticky='nsew')

        # self.gaussianEntryFile = Pmw.EntryField(self.gaussian.interior(),
        #                                         labelpos='w',
        #                                         entry_width=25)
        # self.gaussianEntryFile.grid(column=0, row=0, sticky='w')

        # self.loadGaussian = Tkinter.Button(self.gaussian.interior(),
        #                                    text='Load',
        #                                    command=self._load_gaussian)
        # self.loadGaussian.grid(column=1, row=0, sticky='e')

        # row += 1
        #
        # Team information
        #
        self.teamName = Pmw.Group(parent)
        self.teamName.grid(column=0, row=row, columnspan=2,
                           sticky="nsew")
        self.teamNameInfo = Tkinter.Label(self.teamName.interior(),
                                          text="Interface designed by:\n"
                                          "V. Munoz-Robles, J.-D.Marechal and Jordi Guasp\n"
                                          "InsiliChem")
        self.teamNameInfo.grid(column=0, row=0, sticky="ew")
        row += 1

    def Run(self):
        self.molecules = self.molList.getvalue()

        if not self.molecules:
            from chimera import UserError
            raise UserError("No molecules selected")

        from base import nmod

        prodyalgorithm = None
        n_algorithm = None

        prodyalgorithm = self.AlgorithmMenu.getcurselection()
        if prodyalgorithm == ('Residues' or 'Mass'):
            n_algorithm = int(self.AlgorithmDialog.get())

        self.mi = nmod(self.molecules, self.proc,
                       prodyalgorithm=prodyalgorithm, n_algorithm=n_algorithm,
                       LJ=self.lennard_jones, mass_weighted=self.mass_weighted)

    def _lennard_jones(self, tag, state):
        if state:
            self.lennard_jones = True
        else:
            self.lennard_jones = False

    def _mass_weighted(self, tag, state):
        if state:
            self.mass_weighted = True
        else:
            self.mass_weighted = False

    def _load_gaussian(self):
        file = str(self.gaussianEntryFile.get())
        if not self.molecules:
            from chimera import UserError
            raise UserError("No molecules selected")

        from base import gaussian_nmod

        self.mi = gaussian_nmod(self.molecules, self.proc, file)


from chimera import dialogs
dialogs.register(NMProdyDialog.name, NMProdyDialog)