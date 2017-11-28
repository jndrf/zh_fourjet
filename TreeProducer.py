from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from heppy.analyzers.ntuple import *

from ROOT import TFile

class TreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.taggers = ['b', 'tageff', 'higgsmaker', 'matched', 'dr', 'n_constituents', 'n_charged_hadrons', 'ancestor', 'parton', 'res', 'higgs_from_pair', 'raw_e', 'raw_res' ]
        bookJet(self.tree, 'rawjet1', self.taggers)
        bookJet(self.tree, 'rawjet2', self.taggers)
        bookJet(self.tree, 'rawjet3', self.taggers)
        bookJet(self.tree, 'rawjet4', self.taggers)

        bookJet(self.tree, 'cutjet1', self.taggers)
        bookJet(self.tree, 'cutjet2', self.taggers)
        bookJet(self.tree, 'cutjet3', self.taggers)
        bookJet(self.tree, 'cutjet4', self.taggers)

        bookJet(self.tree, 'cutjet1', self.taggers)
        bookJet(self.tree, 'cutjet2', self.taggers)
        bookJet(self.tree, 'cutjet3', self.taggers)
        bookJet(self.tree, 'cutjet4', self.taggers)

        bookJet(self.tree, 'leptonjet1', self.taggers)
        bookJet(self.tree, 'leptonjet2', self.taggers)
        bookJet(self.tree, 'leptonjet3', self.taggers)
        bookJet(self.tree, 'leptonjet4', self.taggers)

        bookJet(self.tree, 'massjet1', self.taggers)
        bookJet(self.tree, 'massjet2', self.taggers)
        bookJet(self.tree, 'massjet3', self.taggers)
        bookJet(self.tree, 'massjet4', self.taggers)

        bookJet(self.tree, 'hadjet1', self.taggers)
        bookJet(self.tree, 'hadjet2', self.taggers)
        bookJet(self.tree, 'hadjet3', self.taggers)
        bookJet(self.tree, 'hadjet4', self.taggers)

        bookJet(self.tree, 'genjet1', self.taggers)
        bookJet(self.tree, 'genjet2', self.taggers)
        bookJet(self.tree, 'genjet3', self.taggers)
        bookJet(self.tree, 'genjet4', self.taggers)

        bookJet(self.tree, 'rescaled_jet1', self.taggers)
        bookJet(self.tree, 'rescaled_jet2', self.taggers)
        bookJet(self.tree, 'rescaled_jet3', self.taggers)
        bookJet(self.tree, 'rescaled_jet4', self.taggers)

        Bookparticle(self.tree, 'misenergy')
        bookParticle(self.tree, 'higgs')
        bookParticle(self.tree, 'zed')
        bookLepton(self.tree, 'lepton1')
        bookLepton(self.tree, 'lepton2')
      
        bookParticle(self.tree, 'zed_parton1')
        bookParticle(self.tree, 'zed_parton2')
        bookParticle(self.tree, 'higgs_parton1')
        bookParticle(self.tree, 'higgs_parton2')
      
        var(self.tree, 'n_jets') 
        var(self.tree, 'n_genjets') 
        var(self.tree, 'n_leptons') 
        var(self.tree, 'n_candidates')
        var(self.tree, 'higgsmass') #Higgsmasse nach der Formel aus dem Paper

        var(self.tree, 'vismass')
        var(self.tree, 'chi2')
        var(self.tree, 'deltaWW')
        var(self.tree, 'deltaZZ')
        var(self.tree, 'm12')
        var(self.tree, 'm34')
        var(self.tree, 'mHJet')
        var(self.tree, 'mZedJet')
        var(self.tree, 'higgs_ancestor1_pdgid')
        var(self.tree, 'higgs_ancestor2_pdgid')
       
    def process(self, event):
        self.tree.reset()
        misenergy = getattr(event, self.cfg_ana.misenergy)
        fillParticle(self.tree, 'misenergy', misenergy )        

        rawjets = getattr(event, self.cfg_ana.rawjets)
        for ijet, jet in enumerate(rawjets):
            if ijet==4:
                break
            fillJet(self.tree, 'rawjet{ijet}'.format(ijet=ijet+1),
                    jet, self.taggers)


        cutjets = getattr(event, self.cfg_ana.cutjets)
        for ijet, jet in enumerate(cutjets):
            if ijet==4:
                break
            fillJet(self.tree, 'cutjet{ijet}'.format(ijet=ijet+1),
                    jet, self.taggers)


        leptonjets = getattr(event, self.cfg_ana.leptonjets)
        for ijet, jet in enumerate(leptonjets):
            if ijet==4:
                break
            fillJet(self.tree, 'leptonjet{ijet}'.format(ijet=ijet+1),
                    jet, self.taggers)


        massjets = getattr(event, self.cfg_ana.massjets)
        for ijet, jet in enumerate(massjets):
            if ijet==4:
                break
            fillJet(self.tree, 'massjet{ijet}'.format(ijet=ijet+1),
                    jet, self.taggers)


        hadjets = getattr(event, self.cfg_ana.hadjets)
        for ijet, jet in enumerate(hadjets):
            if ijet==4:
                break
            fillJet(self.tree, 'hadjet{ijet}'.format(ijet=ijet+1),
                    jet, self.taggers)

        genjets = getattr(event, self.cfg_ana.genjets)
        for ijet, genjet in enumerate(genjets):
            if ijet==4:
                break
            fillJet(self.tree, 'genjet{ijet}'.format(ijet=ijet+1),
                    genjet, self.taggers)

        rejets = getattr(event, self.cfg_ana.rejets)
        for ijet, rejet in enumerate(rejets):
            if ijet==4:
                break
            fillJet(self.tree, 'rescaled_jet{ijet}'.format(ijet=ijet+1),
                    rejet, self.taggers)

        higgs = getattr(event, self.cfg_ana.higgs)
        try:
            fill(self.tree, 'higgsmass', getattr(event, self.cfg_ana.higgsmass))
        except AttributeError:
            pass
        if higgs:
            fillParticle(self.tree, 'higgs', higgs)
            try:
                if len(event.partons_from_H)==2:
                    fillParticle(self.tree, 'higgs_parton1', event.partons_from_H[0])
                    fillParticle(self.tree, 'higgs_parton2', event.partons_from_H[1])
            except AttributeError:
                pass
                

        zed = getattr(event, self.cfg_ana.zed)
        if zed:
            fillParticle(self.tree, 'zed', zed)
            try:
                if len(event.partons_from_Z)==2:
                    fillParticle(self.tree, 'zed_parton1', event.partons_from_Z[0])
                    fillParticle(self.tree, 'zed_parton2', event.partons_from_Z[1])
            except AttributeError:
                pass
        leptons = getattr(event, self.cfg_ana.leptons)
        for ilep, lepton in enumerate(reversed(leptons)):
            if ilep == 2:
                break
            fillLepton(self.tree,
                       'lepton{ilep}'.format(ilep=ilep+1), 
                       lepton)
       
        fill( self.tree, 'n_jets', getattr(event, self.cfg_ana.njets))
        fill( self.tree, 'n_genjets', getattr(event, self.cfg_ana.ngenjets))
        fill( self.tree, 'n_leptons', len(leptons) )
        fill( self.tree, 'n_candidates', getattr(event, self.cfg_ana.numberOfCandidates))

        fill(self.tree, 'vismass', getattr(event, self.cfg_ana.vismass))
        fill(self.tree, 'chi2', getattr(event, self.cfg_ana.chi2))
        fill(self.tree, 'deltaWW', getattr(event, self.cfg_ana.dWW))
        fill(self.tree, 'deltaZZ', getattr(event, self.cfg_ana.dZZ))
        fill(self.tree, 'm12', getattr(event, self.cfg_ana.pair1_m))
        fill(self.tree, 'm34', getattr(event, self.cfg_ana.pair2_m))
        # fill(self.tree, 'tagger_b', getattr(event, self.cfg_ana.bRate))
        # fill(self.tree, 'tagger_c', getattr(event, self.cfg_ana.cRate))
        # fill(self.tree, 'tagger_mis', getattr(event, self.cfg_ana.misRate))
        fill(self.tree, 'mHJet', getattr(event, self.cfg_ana.mHJet))
        fill(self.tree, 'mZedJet', getattr(event, self.cfg_ana.mZedJet)) 
        fill(self.tree, 'higgs_ancestor1_pdgid', getattr(event, self.cfg_ana.anc1))
        fill(self.tree, 'higgs_ancestor2_pdgid', getattr(event, self.cfg_ana.anc2))
        
        self.tree.tree.Fill()
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        

