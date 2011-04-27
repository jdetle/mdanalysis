# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# MDAnalysis --- http://mdanalysis.googlecode.com
# Copyright (c) 2006-2011 Naveen Michaud-Agrawal,
#               Elizabeth J. Denning, Oliver Beckstein,
#               and contributors (see website for details)
# Released under the GNU Public Licence, v2 or any higher version
#
# Please cite your use of MDAnalysis in published work:
#
#     N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and
#     O. Beckstein. MDAnalysis: A Toolkit for the Analysis of
#     Molecular Dynamics Simulations. J. Comput. Chem. (2011),
#     doi:10.1002/jcc.21787
#

import MDAnalysis
from MDAnalysis.tests.datafiles import PDBQT_input, PDBQT_querypdb
import MDAnalysis.KDTree.NeighborSearch as kdNS


from numpy.testing import *
from numpy import array, float32
from nose.plugins.attrib import attr


class TestPDBQT(TestCase):
    def setUp(self):
        """Set up the standard AdK system in implicit solvent."""
        self.universe = MDAnalysis.Universe(PDBQT_input) # PDBQT
        self.query_universe = MDAnalysis.Universe(PDBQT_querypdb) # PDB file

    def tearDown(self):
        del self.universe
        del self.query_universe

    def test_segid(self):
        sel = self.universe.selectAtoms('segid A')
        assert_equal(sel.numberOfAtoms(), 909, "failed to select segment A")
        sel = self.universe.selectAtoms('segid B')
        assert_equal(sel.numberOfAtoms(), 896, "failed to select segment B")
        
    def test_protein(self):
        sel = self.universe.selectAtoms('protein')
        assert_equal(sel.numberOfAtoms(), 1805, "failed to select protein")
        assert_equal(sel._atoms, self.universe.atoms,
                     "selected protein is not the same as auto-generated protein segment A+B")

    def test_backbone(self):
        sel = self.universe.selectAtoms('backbone')
        assert_equal(sel.numberOfAtoms(), 796)

    def test_neighborhood(self):
        '''Creates a KDTree of the protein and 
        uses the coordinates of the atoms in the query pdb
        to create a list of protein residues within 4.0A of the query atoms.
        '''
        protein = self.universe.selectAtoms("protein")
        ns_protein = kdNS.AtomNeighborSearch(protein)
        query_atoms = self.query_universe.atoms
        residue_neighbors = ns_protein.search_list(query_atoms, 4.0)
        assert_equal(residue_neighbors, 80)