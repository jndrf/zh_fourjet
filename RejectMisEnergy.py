from heppy.framework.analyzer import Analyzer
from heppy.framework.event import Event
from heppy.particles.tlv.jet import Jet
from heppy.particles.jet import JetConstituents
from heppy.particles.tlv.particle import Particle
from math import sqrt
from ROOT import TLorentzVector
import copy
class RejectMisEnergy(Analyzer):

    def process(self, event):
        jets = getattr(event, self.cfg_ana.input_jets)
        # if len(jets)==0:
        #     setattr(event, self.cfg_ana.output_jets, [])
        #     setattr(event, self.cfg_ana.out_mass, -1)
        #     return True

        sum_p4 = TLorentzVector()
        for jet in jets:
            sum_p4 += jet.p4()
        virtualpart = Particle(0, 0, sum_p4, 1)

        setattr(event, self.cfg_ana.out_mass, virtualpart.m())
        # if virtualpart.m() <= 180:
        #     setattr(event, self.cfg_ana.output_jets, [])
        #     return True

        setattr(event, self.cfg_ana.output_jets, jets)

