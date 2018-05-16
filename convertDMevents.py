#!/usr/bin/env python
import os
import sys
import getopt
import time
import lhe_parser
import ROOT as r
import logging
from array import array

# DMpdgcode = 9000007
DMpdgcode = 5000521
# DMpdgcode = 22008    Depending on the provided DM decay model
ESevent = False
DISevent = False
initial_state = -1
final_state = 1

def convertES(inputFile):    # Convert LHE file's infos into a ROOT TTree

    ESevent = True
    lhe = lhe_parser.EventFile(inputFile)    # Load LHE file		
    
    rootfile_dm = r.TFile("rootfile_dm.root", "recreate")
    tree_dm = r.TTree("dmtree", "dmtree")
    
    Edm = array('d', [0])
    pxdm = array('d', [0])
    pydm = array('d', [0])
    pzdm = array('d', [0])
    dmpdg = array('i', [0])
    dis = array('i', [0])
    el = array('i', [0])
    E_2ry = array('d', [0]*500)
    px_2ry = array('d', [0]*500)
    py_2ry = array('d', [0]*500)
    pz_2ry = array('d', [0]*500)
    pdg_2ry = array('i', [0]*500)
    n_2ry = array('i', [0])

    tree_dm.Branch('Edm', Edm, 'Edm,/D')
    tree_dm.Branch('pxdm', pxdm, 'pxdm,/D')
    tree_dm.Branch('pydm', pydm, 'pydm,/D')
    tree_dm.Branch('pzdm', pzdm, 'pzdm,/D')
    tree_dm.Branch('dmpdg', dmpdg, 'dmpdg,/I')
    tree_dm.Branch('dis', dis, 'dis,/I')
    tree_dm.Branch('el', el, 'el,/I')
    tree_dm.Branch('E_2ry', E_2ry, 'E_2ry,/D')
    tree_dm.Branch('px_2ry', px_2ry, 'px_2ry,/D')
    tree_dm.Branch('py_2ry', py_2ry, 'py_2ry,/D')
    tree_dm.Branch('pz_2ry', pz_2ry, 'pz_2ry,/D')
    tree_dm.Branch('pdg_2ry', pdg_2ry, 'pdg_2ry,/I')
    tree_dm.Branch('n_2ry', n_2ry, 'n_2ry,/I')

    for event in lhe:
        index = 0
        for particle in event:
            if particle.status == initial_state and particle.pdg == DMpdgcode:
                Edm[0] = particle.E
                pxdm[0] = particle.px
                pydm[0] = particle.py
                pzdm[0] = particle.pz
                dmpdg[0] = particle.pdg
                el[0] = ESevent
                dis[0] = DISevent
            elif particle.status == final_state and particle.pdg != DMpdgcode:
                E_2ry[index] = particle.E
                px_2ry[index] = particle.px
                py_2ry[index] = particle.py
                pz_2ry[index] = particle.pz
                pdg_2ry[index] = particle.pdg
		index += 1
        n_2ry[0] = index
        tree_dm.Fill()

    # Write the tree into the output file and close the file
    rootfile_dm.Write()
    rootfile_dm.Close()

    print "----------------------------------------------------------------"
    print "--------STATUS INFO - LDM ESevents: ROOTfile successfully saved!"
    print "----------------------------------------------------------------"
    return(rootfile_dm)


#---------------------------------------------------------------------------

def convertDIS(inputFile_dm, inputFile_hadrons):

    DISevent = True
    lhe = lhe_parser.EventFile(inputFile_dm)    # Load LHE file		
    
    rootfile_dm = r.TFile("rootfile_dm.root", "recreate")
    tree_dm = r.TTree("dmtree", "dmtree")
    
    Edm = array('d', [0])
    pxdm = array('d', [0])
    pydm = array('d', [0])
    pzdm = array('d', [0])
    dmpdg = array('i', [0])
    dis = array('i', [0])
    el = array('i', [0])
    E_2ry = array('d', [0]*500)
    px_2ry = array('d', [0]*500)
    py_2ry = array('d', [0]*500)
    pz_2ry = array('d', [0]*500)
    pdg_2ry = array('i', [0]*500)
    n_2ry = array('i', [0])

    tree_dm.Branch('Edm', Edm, 'Edm,/D')
    tree_dm.Branch('pxdm', pxdm, 'pxdm,/D')
    tree_dm.Branch('pydm', pydm, 'pydm,/D')
    tree_dm.Branch('pzdm', pzdm, 'pzdm,/D')
    tree_dm.Branch('dmpdg', dmpdg, 'dmpdg,/I')
    tree_dm.Branch('dis', dis, 'dis,/I')
    tree_dm.Branch('el', el, 'el,/I')
    tree_dm.Branch('E_2ry', E_2ry, 'E_2ry,/D')
    tree_dm.Branch('px_2ry', px_2ry, 'px_2ry,/D')
    tree_dm.Branch('py_2ry', py_2ry, 'py_2ry,/D')
    tree_dm.Branch('pz_2ry', pz_2ry, 'pz_2ry,/D')
    tree_dm.Branch('pdg_2ry', pdg_2ry, 'pdg_2ry,/I')
    tree_dm.Branch('n_2ry', n_2ry, 'n_2ry,/I')

    print 'input file pythia: ', inputFile_hadrons
    P8gen = r.TPythia8()
    pythiagen = P8gen.Pythia8()
    pythiagen.readString("Beams:frameType = 4")
    pythiagen.readString("Beams:LHEF = "+str(inputFile_hadrons))
    pythiagen.init()

    for event in lhe:
        index = 0
        for particle in event:
            if particle.status == initial_state and particle.pdg == DMpdgcode:
                Edm[0] = particle.E
                pxdm[0] = particle.px
                pydm[0] = particle.py
                pzdm[0] = particle.pz
                dmpdg[0] = particle.pdg
                el[0] = ESevent
                dis[0] = DISevent
        if not pythiagen.info.atEndOfFile():
            pythiagen.next()    # Generate events, and check whether generation failed
            for i in range(pythiagen.event.size()):
                if pythiagen.event[i].isFinal() and pythiagen.event[i].id() != DMpdgcode:
                    E_2ry[index] = pythiagen.event[i].e()
                    px_2ry[index] = pythiagen.event[i].px()
                    py_2ry[index] = pythiagen.event[i].py()
                    pz_2ry[index] = pythiagen.event[i].pz()
                    pdg_2ry[index] = pythiagen.event[i].id()
                    index += 1 
        n_2ry[0] = index
        tree_dm.Fill()

    pythiagen.stat()

    # Write the tree into the output file and close the file
    rootfile_dm.Write()
    rootfile_dm.Close()

    print "----------------------------------------------------------------"
    print "-------STATUS INFO - LDM DISevents: ROOTfile successfully saved!"
    print "----------------------------------------------------------------"
    return(rootfile_dm)


#---------------------------------------------------------------------------
