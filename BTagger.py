from heppy.framework.analyzer import Analyzer
from random import random
from math import tanh
class BTagger(Analyzer):
    '''
    pt-dependend b-tagger. Formulas taken from https://github.com/delphes/delphes/blob/master/cards/delphes_card_CMS.tcl (search for b-tagging), which itself is based on arXiv:1211.4462
    Distinguishes between b, c, and other types of jets.
    '''
    def forB(self, pt):
        return .85*tanh(.0025*pt)*(25.0/(1+0.063*pt))

    def forC(self, pt):
        return 0.25 * tanh(0.018*pt)*(1/(1+0.0013*pt))

    def forTheRest(self, pt):
        return 0.01 + 0.000038 * pt

    def process(self, event):
        jets = getattr(event, self.cfg_ana.input_jets)

        for jet in jets:
            is_bjet = False
            
            if jet.match and jet.match.match and abs(jet.match.match.pdgid())==5:
                jet.tags['tageff'] = self.forB(jet.pt())
                is_bjet = self.forB(jet.pt()) > random()
            elif jet.match and jet.match.match and abs(jet.match.match.pdgid())==4:
                jet.tags['tageff'] = self.forC(jet.pt())
                is_bjet = self.forC(jet.pt()) > random()
            elif jet.match and jet.match.match and abs(jet.match.match.pdgid())<4:
                jet.tags['tageff'] = self.forTheRest(jet.pt())
                is_bjet = self.forTheRest(jet.pt()) > random()
            else:
                jet.tags['tageff'] = 0
                is_bjet = False

            '''lower part for tagging of genejts
            if jet.match and abs(jet.match.pdgid())==5:
                logstr += ' b ' +str(.85*tanh(.0025*jet.pt())*(25.0/(1+0.063*jet.pt())))
                is_bjet = self.forB(jet.pt())
            elif jet.match and abs(jet.match.pdgid())==4:
                logstr += ' c ' + str(0.25 * tanh(0.018*jet.pt())*(1/(1+0.0013*jet.pt())))
                is_bjet = self.forC(jet.pt())
            else:
                logstr += 'uds' + str(0.01 + 0.000038 * jet.pt())
                is_bjet = self.forTheRest(jet.pt())
            '''
            jet.tags['b'] = is_bjet
#            print logstr + str(is_bjet)
