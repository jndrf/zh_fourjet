
from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance2 as Resonance

import pprint
import itertools
import copy
from math import sqrt

mass = {23: 91, 25: 125}

class ZHReconstruction(Analyzer):

    def setOutput(self, event, higgsmass, higgs, zed):
        setattr(event, self.cfg_ana.higgsmass, higgsmass)
        setattr(event, self.cfg_ana.output_higgs, higgs)
        setattr(event, self.cfg_ana.output_zed, zed)


    def findHiggsCandidate(self, event, jets):
        candlist = []

        for jet in jets:
            jet.tags['higgsmaker'] = False
        for j1, j2, j3, j4 in itertools.permutations(jets):
            if not (j1.tags['b'] and j2.tags['b']): continue
            try:
                m12 = sqrt((j1.p4() + j2.p4())* (j1.p4() + j2.p4()))
                m34 = sqrt((j3.p4() + j4.p4())*(j3.p4() + j4.p4()))
            except ValueError:
                continue
            higgsmass = m12 + m34 - mass[23]
            try:
                candlist.append([j1, j2, j3, j4, higgsmass, m12, m34, j1.tags['ancestor'], j2.tags['ancestor']])
            except AttributeError:
                candlist.append([j1, j2, j3, j4, higgsmass, m12, m34, 0, 0])


        setattr(event, self.cfg_ana.numberOfCandidates, len(candlist))
        if not len(candlist): 
            return []
        candlist.sort(key = lambda x: abs(x[4] - mass[25]))
        setattr(event, self.cfg_ana.mHJet, candlist[0][5])
        setattr(event, self.cfg_ana.mZedJet, candlist[0][6])
        setattr(event, self.cfg_ana.anc1, candlist[0][7])
        setattr(event, self.cfg_ana.anc2, candlist[0][7])
        candlist[0][0].tags['higgsmaker'] = True
        candlist[0][1].tags['higgsmaker'] = True
        return candlist[0] #hier Liste mit den vier Jets des besten Higgs-Kandidaten. 

    def findHiggsPair(self, jets):
        hlist = []
        for jet in jets:
            jet.tags['higgs_from_pair'] = False
        for j1, j2, j3, j4 in itertools.permutations(jets):
        # try:
            if j1.tags['ancestor'] ==25 and j2.tags['ancestor'] ==25:
                hlist.append([Resonance(j1, j2, 25), j1, j2, Resonance(j3, j4, 23)])
        # except:
        #     print 'nixhix'
        # try:
            elif j3.tags['ancestor']==23 and j4.tags['ancestor']==23:
                hlist.append([Resonance(j1, j2, 25), j1, j2, Resonance(j3, j4, 23)])
        # except:
        #     print 'njetzed'
        #     import pdb
        #     pdb.set_trace()


        hlist.sort(key = lambda x: abs(x[0].m() - mass[25]))
        hlist[0][1].tags['higgs_from_pair'] = True
        hlist[0][2].tags['higgs_from_pair'] = True
        return hlist[0][0], hlist[0][3]


    def process(self, event):
        jets = getattr(event, self.cfg_ana.input_jets)
        self.setOutput(event, 0, None, None)
        setattr(event, self.cfg_ana.numberOfCandidates, -1)
        setattr(event, self.cfg_ana.mHJet, -1)
        setattr(event, self.cfg_ana.mZedJet, -1)
        setattr(event, self.cfg_ana.anc1, 0)
        setattr(event, self.cfg_ana.anc2, 0)

        if len(jets)==0: 
            return True
        candjets = self.findHiggsCandidate(event, jets)
        if not candjets:
            return True
        try:
            higgs, zed = self.findHiggsPair(jets)
        except IndexError:
            print 'teilchen kapott :('
            print jets
            higgs = None
            zed = None
        higgsmass = candjets[4]
        #print candjets
        self.setOutput(event, higgsmass, higgs, zed)
       
