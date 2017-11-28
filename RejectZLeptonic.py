from heppy.framework.analyzer import Analyzer
from heppy.framework.event import Event
from heppy.particles.tlv.jet import Jet
from heppy.particles.jet import JetConstituents
import copy
class RejectZLeptonic(Analyzer):
    

    def process(self, event):
        jets = copy.deepcopy(getattr(event, self.cfg_ana.input_jets))
        charged_hadrons = [211]
        # if len(jets)==0:
        #     setattr(event, self.cfg_ana.output_jets, [])
        #     return True

        #reject jets with less than five particles
        for jet in jets:
            sump = 0
            sumh = 0
            for val in jet.constituents.values():
                sump += len(val)
            
            for key in charged_hadrons:
                try:
                    sumh += len(jet.constituents[key])
                except KeyError:
                    pass

            # if sump < 5:
            #     setattr(event, self.cfg_ana.output_jets, [])
            #     return True
            # if not sumh:
            #     setattr(event, self.cfg_ana.output_jets, [])
            #    return True
            jet.tags['n_constituents'] = sump
            jet.tags['n_charged_hadrons'] = sumh

        setattr(event, self.cfg_ana.output_jets, jets)
