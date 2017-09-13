from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class Selection(Analyzer):

    def beginLoop(self, setup):
        super(Selection, self).beginLoop(setup)
        self.counters.addCounter('cut_flow') 
        self.counters['cut_flow'].register('All events')
        self.counters['cut_flow'].register('No lepton')
        self.counters['cut_flow'].register('4 and more jets')
        self.counters['cut_flow'].register('Z not leptonic')
        self.counters['cut_flow'].register('Visible Mass > 180')
        self.counters['cut_flow'].register('Successful rescaling')
        self.counters['cut_flow'].register('Not Fully Hadronic ZZ/WW')
        self.counters['cut_flow'].register('2 or more b jets')
        self.counters['cut_flow'].register('higgs made')
    
    def process(self, event):
        self.counters['cut_flow'].inc('All events')
        if len(event.sel_iso_leptons) > 2:
            return True # could return False to stop processing
        self.counters['cut_flow'].inc('No lepton')
        # rawjets = getattr(event, self.cfg_ana.rawjets)        
        # cjets = getattr(event, self.cfg_ana.cutjets)
        # ljets = getattr(event, self.cfg_ana.leptonjets)
        # ejets = getattr(event, self.cfg_ana.massjets)
        # hjets = getattr(event, self.cfg_ana.hadjets)
        jets = getattr(event, self.cfg_ana.input_jets)
        higgs = getattr(event, self.cfg_ana.higgsmass)
        
        if getattr(event, self.cfg_ana.njets) < 4:
            return True
        self.counters['cut_flow'].inc('4 and more jets')
        
        for jet in jets:
            # jet.tags['pt'] = jet.pt()
            # jet.tags['px'] = jet.px()
            # jet.tags['py'] = jet.py()
            # jet.tags['pz'] = jet.pz()
            if jet.tags['n_constituents'] < 5: return True
            elif jet.tags['n_charged_hadrons'] < 1: return True
        self.counters['cut_flow'].inc('Z not leptonic')

        if getattr(event, self.cfg_ana.vismass) < 180:
            return True
        self.counters['cut_flow'].inc('Visible Mass > 180')

        if getattr(event, self.cfg_ana.chi2) < 0:
            return True
        self.counters['cut_flow'].inc('Successful rescaling')

        if getattr(event, self.cfg_ana.dWW) <= 10 or getattr(event, self.cfg_ana.dZZ) <= 10:
            return True
        self.counters['cut_flow'].inc('Not Fully Hadronic ZZ/WW')

        bjets = [jet for jet in jets if jet.tags['b']]
        if len(bjets) >= 2:
            self.counters['cut_flow'].inc('2 or more b jets')

        recos = 0
        for jet in jets:
            if jet.tags['b'] and jet.tags['higgsmaker']:
                recos += 1
        if recos != 2: return True
        mZedJet = getattr(event, self.cfg_ana.mZedJet)
        if getattr(event, self.cfg_ana.mHJet)<=100: return True
        if mZedJet <=80 or mZedJet>=110: return True
        if higgs<=0: return True
        self.counters['cut_flow'].inc('higgs made')
