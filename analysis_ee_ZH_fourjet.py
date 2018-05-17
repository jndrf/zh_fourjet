process = 'ee_ZH_any'
'''
Adapted example
Example configuration file for an ee->ZH analysis in the 4 jet channel,
with the FCC-ee

While studying this file, open it in ipython as well as in your editor to 
get more information: 

ipython
from analysis_ee_ZH_had_cfg import * 

'''
PTMIN = 8
import os
import copy
import heppy.framework.config as cfg

from heppy.framework.event import Event
Event.print_patterns=['*jet*', 'bquarks', '*higgs*',
                      '*zed*', '*lep*']

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# setting the random seed for reproducible results
import heppy.statistics.rrandom as random
random.seed(0xdeadbeef)

# definition of the collider
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240.

# input definition
comp = cfg.Component(
    'ee_ZH_Z_Hbb',
    files = [
        'data/plain/ee_ZH_any_0.root'
    ]
)
selectedComponents = [comp]

# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

# the papas simulation and reconstruction sequence
# from heppy.test.papas_cfg import papas_sequence, detector, papas, gen_particles_stable
from heppy.papas.detectors.FCCHiggsDetectors.config.cfg_CLIC import papas_sequence, detector, papas, gen_particles_stable
# on Detector change, change ROC curve!!!!

# write out partons from Z and H decays
#from heppy.analyzers.mytest_PartonAnalyzer import PartonsFromZH
from heppy.analyzers.examples.zh_fourjet.PartonAnalyzer import PartonsFromZH
partons = cfg.Analyzer(
    PartonsFromZH,
    partons = 'partons'
)

# Use a Selector to select leptons from the output of papas simulation.
# Currently, we're treating electrons and muons transparently.
# we could use two different instances for the Selector module
# to get separate collections of electrons and muons
# help(Selector) for more information
from heppy.analyzers.Selector import Selector
def is_lepton(ptc):
    return ptc.e()> 5. and abs(ptc.pdgid()) in [11, 13]

leptons = cfg.Analyzer(
    Selector,
    'sel_leptons',
    output = 'leptons',
    input_objects = 'rec_particles',
    #input_objects = 'gen_particles_stable',
    filter_func = is_lepton 
)

# Compute lepton isolation w/r other particles in the event.
# help(IsolationAnalyzer) 
# help(isolation) 
# for more information
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'leptons',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    iso_area = EtaPhiCircle(0.4)
)

# Select isolated leptons with a Selector
def is_isolated(lep):
    '''returns true if the particles around the lepton
    in the EtaPhiCircle defined above carry less than 30%
    of the lepton energy.'''
    return lep.iso.sume/lep.e()<0.3  # fairly loose

sel_iso_leptons = cfg.Analyzer(
    Selector,
    'sel_iso_leptons',
    output = 'sel_iso_leptons',
    input_objects = 'leptons',
    filter_func = is_isolated
)

# make exclusive  jets with pt>10GeV
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    output = 'exjets',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    fastjet_args = dict(ptmin=PTMIN),
)

# make exclusive gen jets with stable gen particles
genjets = cfg.Analyzer(
    JetClusterizer,
    output = 'exgenjets',
    particles = 'gen_particles_stable',
    fastjet_args = dict(ptmin=PTMIN),
)

# count exclusive jets
from heppy.analyzers.examples.zh_fourjet.JetCounter import JetCounter
jetcounter = cfg.Analyzer(
    JetCounter,
    input_jets = 'exjets',
    njets = 'n_jets'
)

genjetcounter = cfg.Analyzer(
    JetCounter,
    input_jets = 'exgenjets',
    njets = 'n_genjets'
)
# make four inclusive jets
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
incljets = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    fastjet_args = dict(njets=4)  
)

# make four inclusive gen jets with stable gen particles
inclgenjets = cfg.Analyzer(
    JetClusterizer,
    output = 'genjets',
    particles = 'gen_particles_stable',
    fastjet_args = dict(njets=4)  
)

#reject Z decays into Leptons
from heppy.analyzers.examples.zh_fourjet.RejectZLeptonic import RejectZLeptonic
reject_Z_leptonic = cfg.Analyzer(
    RejectZLeptonic,
    input_jets = 'jets',
    output_jets = 'ljets'
)

#reject visible mass <= 180 GeV
from heppy.analyzers.examples.zh_fourjet.RejectMisEnergy import RejectMisEnergy
reject_missing_nrg = cfg.Analyzer(
    RejectMisEnergy,
    input_jets = 'ljets',
    output_jets = 'ejets',
    out_mass = 'vismass'
)

# rescale the jet energy taking according to initial p4
from heppy.analyzers.examples.zh_fourjet.JetEnergyComputer import JetEnergyComputer
compute_jet_energy = cfg.Analyzer(
    JetEnergyComputer,
    output_jets='rescaled_jets',
    out_chi = 'chi2',
    input_jets='ejets',
    sqrts=Collider.SQRTS
)

# select b quarks for jet to parton matching.
def is_outgoing_quark(ptc):
    '''returns True if the particle is an outgoing b quark,
    see
    http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
    '''
    return abs(ptc.pdgid()) <= 6 and ptc.status() == 23
    
outgoing_quarks = cfg.Analyzer(
    Selector,
    'outgoing_quarks',
    output = 'outgoing_quarks',
    input_objects = 'gen_particles',
    filter_func =is_outgoing_quark
)

# match genjets to b quarks 
from heppy.analyzers.Matcher import Matcher
genjet_to_b_match = cfg.Analyzer(
    Matcher,
    match_particles = 'outgoing_quarks',
    particles = 'genjets',
    delta_r = 0.4 #default 0.4
    )

# match jets to genjets (so jets are matched to b quarks through gen jets)
jet_to_genjet_match = cfg.Analyzer(
    Matcher,
    match_particles='genjets',
    particles='rescaled_jets',
    delta_r=0.5
)

#Reject events that are compatible with a fully hadronic ZZ or WW decay
from heppy.analyzers.examples.zh_fourjet.FullHadCompatible import FullHadCompatible
fullhadcompatible = cfg.Analyzer(
    FullHadCompatible,
    input_jets='rescaled_jets',
    output_jets='hjets',
    dWW = 'deltaWW',
    dZZ = 'deltaZZ',
    pair1_m = 'm12',
    pair2_m = 'm34'
)

from heppy.analyzers.ParametrizedBTagger import ParametrizedBTagger
from heppy.analyzers.roc import clic_roc
clic_roc.set_working_point(0.8)
btag = cfg.Analyzer(
    ParametrizedBTagger,
    input_jets='hjets',
    roc=clic_roc
)

# pt-dependend b tagging, also based on CMS-performance
# different efficiencies for b, c and other quarks.
from heppy.analyzers.examples.zh_fourjet.BTagger import BTagger
btag_pt = cfg.Analyzer(
    BTagger,
    input_jets = 'hjets',
)

# compute the missing 4-momentum
from heppy.analyzers.RecoilBuilder import RecoilBuilder
missing_energy = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy',
    output = 'missing_energy',
    sqrts = Collider.SQRTS,
    to_remove = 'rec_particles'
    #to_remove = 'gen_particles_stable'
) 

#Find the Particle (H, Z, ...) from which the jets originate
from heppy.analyzers.examples.zh_fourjet.AncestorSeeker import AncestorSeeker
ancestors = cfg.Analyzer(
    AncestorSeeker,
    input_jets = 'genjets'
)

from heppy.analyzers.examples.zh_fourjet.MatchTransfer import MatchTransfer
matchtransfer = cfg.Analyzer(
    MatchTransfer,
    input_jets = 'hjets',
    input_genjets = 'genjets'
)

# reconstruction of the H and Z resonances.
# for now, use for the Higgs the two b jets with the mass closest to mH
# the other 2 jets are used for the Z.
# implement a chi2? 
from heppy.analyzers.examples.zh_fourjet.ZHReconstruction import ZHReconstruction
zhreco = cfg.Analyzer(
    ZHReconstruction,
    output_higgs='higgs',
    output_zed='zed', 
    input_jets='hjets',
    numberOfCandidates = 'n_candidates',
    higgsmass='higgsmass', #Ausgabe der Higgsmasse nach der Formel aus dem Paper
    mHJet = 'mHJet',
    mZedJet = 'mZedJet',
    anc1 = 'higgs_anc1',
    anc2 = 'higgs_anc2'
)

# simple cut flow printout
from heppy.analyzers.examples.zh_fourjet.Selection import Selection
selection = cfg.Analyzer(
    Selection,
    njets = 'n_jets',
    rawjets='jets',
    # cutjets='cjets',
    # leptonjets='ljets',
    # massjets='ejets',
    # hadjets='hjets',
    input_jets='hjets', 
    vismass = 'vismass',
    dWW = 'deltaWW',
    dZZ = 'deltaZZ',
    mHJet = 'mHJet',
    mZedJet = 'mZedJet',
    higgs='higgs',
    higgsmass='higgsmass', 
    anc1 = 'higgs_anc1',
    anc2 = 'higgs_anc2',
    zed='zed',
    leptons='sel_iso_leptons',
    numberOfCandidates = 'n_candidates',
    chi2 = 'chi2',
    log_level=logging.INFO
)

# Analysis-specific ntuple producer
# please have a look at the ZHTreeProducer class
from heppy.analyzers.examples.zh_fourjet.TreeProducer import TreeProducer
tree = cfg.Analyzer(
    TreeProducer,
    misenergy = 'missing_energy', 
    rawjets='jets',
#    cutjets = 'cjets',
    leptonjets = 'ljets',
    massjets = 'ejets',
    rejets = 'rescaled_jets',
    chi2 = 'chi2',
    hadjets = 'hjets',
    genjets='genjets',
    vismass = 'vismass',
    dWW = 'deltaWW',
    dZZ = 'deltaZZ',
    pair1_m = 'm12',
    pair2_m = 'm34',
    mHJet = 'mHJet',
    mZedJet = 'mZedJet',
    higgs='higgs',
    higgsmass='higgsmass', 
    anc1 = 'higgs_anc1',
    anc2 = 'higgs_anc2',
    zed='zed',
    leptons='sel_iso_leptons',
    numberOfCandidates = 'n_candidates',
    njets = 'n_jets',
    ngenjets = 'n_genjets'
)

# definition of the sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    papas_sequence,
    #gen_particles_stable, # need to include this only if papas_sequence is excluded
    partons,
    leptons,
    iso_leptons,
    sel_iso_leptons,
#    lepton_veto, 
    genjets, 
    jets,
    jetcounter,
    genjetcounter,
    incljets,
    inclgenjets,
    reject_Z_leptonic,
    reject_missing_nrg,
    compute_jet_energy, 
    outgoing_quarks,
    genjet_to_b_match,
    jet_to_genjet_match, 
    ancestors,
    fullhadcompatible,
    btag,
#    btag_pt,
    missing_energy, 
    matchtransfer,
    zhreco, 
    selection, 
    tree
)

# Specifics to read FCC events 
from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def process(iev=None):
        if iev is None:
            iev = loop.iEvent
        loop.process(iev)
        if display:
            display.draw()

    def next():
        loop.process(loop.iEvent+1)
        if display:
            display.draw()            

    iev = None
    usage = '''usage: python analysis_ee_ZH_had_cfg.py [ievent]
    
    Provide ievent as an integer, or loop on the first events.
    You can also use this configuration file in this way: 
    
    heppy_loop.py OutDir/ analysis_ee_ZH_had_cfg.py -f -N 100 
    '''
    if len(sys.argv)==2:
        papas.display = True
        try:
            iev = int(sys.argv[1])
        except ValueError:
            print usage
            sys.exit(1)
    elif len(sys.argv)>2: 
        print usage
        sys.exit(1)
            
        
    loop = Looper( 'looper', config,
                   nEvents=10,
                   nPrint=10,
                   timeReport=True)
    
    simulation = None
    for ana in loop.analyzers: 
        if hasattr(ana, 'display'):
            simulation = ana
    display = getattr(simulation, 'display', None)
    simulator = getattr(simulation, 'simulator', None)
    if simulator: 
        detector = simulator.detector
    if iev is not None:
        process(iev)
    else:
        loop.loop()
        loop.write()
