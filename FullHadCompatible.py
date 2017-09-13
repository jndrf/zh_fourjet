from heppy.framework.analyzer import Analyzer
from heppy.framework.event import Event
from heppy.particles.tlv.jet import Jet
from itertools import permutations
from heppy.particles.tlv.particle import Particle
import math
import copy

class FullHadCompatible(Analyzer):
    '''
Rejects events that are compatible with a fully hadronic WW or ZZ decay
    '''

    def process(self, event):
        mass = {23:91, 24:80, 25:125}
        jets = getattr(event, self.cfg_ana.input_jets)
        if len(jets) < 4:
            setattr(event, self.cfg_ana.dWW, -1)
            setattr(event, self.cfg_ana.dZZ, -1)
            setattr(event, self.cfg_ana.output_jets, [])
            setattr(event, self.cfg_ana.pair1_m, 0)
            setattr(event, self.cfg_ana.pair2_m, 0)
            return True

        deltaW = []
        deltaZ = []

        mlist = []

        # epsilonW = []
        # epsilonZ = []

        # mij = Particle(0, 0, jets[0].p4() + jets[1].p4()).m()
        # mkl = Particle(0, 0, jets[2].p4() + jets[3].p4()).m()

        # epsilonZ.append(math.sqrt((mij-91)**2 + (mkl - 91)**2))
        # epsilonW.append(math.sqrt((mij-80)**2 + (mkl - 80)**2))

        # mij = Particle(0, 0, jets[0].p4() + jets[2].p4()).m()
        # mkl = Particle(0, 0, jets[1].p4() + jets[3].p4()).m()

        # epsilonZ.append(math.sqrt((mij-91)**2 + (mkl - 91)**2))
        # epsilonW.append(math.sqrt((mij-80)**2 + (mkl - 80)**2))

        # mij = Particle(0, 0, jets[0].p4() + jets[3].p4()).m()
        # mkl = Particle(0, 0, jets[2].p4() + jets[1].p4()).m()

        # epsilonZ.append(math.sqrt((mij-91)**2 + (mkl - 91)**2))
        # epsilonW.append(math.sqrt((mij-80)**2 + (mkl - 80)**2))

        for j1, j2, j3, j4 in permutations(jets, 4):
            try:
                m12 = math.sqrt((j1.p4() + j2.p4())*(j1.p4() + j2.p4()))
                m34 = math.sqrt((j3.p4() + j4.p4())*(j3.p4() + j4.p4()))

            except ValueError: #aus $Gruenden gibts manchmal negative Massen
                continue

            dW = math.sqrt((m12 - mass[24])**2 + (m34 - mass[24])**2)
            dZ = math.sqrt((m12 - mass[23])**2 + (m34 - mass[23])**2)
            deltaW.append(dW)
            deltaZ.append(dZ)
            mlist.append((m12, m34))


        setattr(event, self.cfg_ana.output_jets, jets)
        mlist.sort(key = lambda x: abs(x[0] - mass[25]) + abs(x[1] - mass[23]))
        if not deltaW or not deltaZ:
            setattr(event, self.cfg_ana.dWW, -1)
            setattr(event, self.cfg_ana.dZZ, -1)
            setattr(event, self.cfg_ana.pair1_m, 0)
            setattr(event, self.cfg_ana.pair2_m, 0)
            return True


        # if min(deltaW)<10 or min(deltaZ)<10:
        #     setattr(event, self.cfg_ana.dWW, min(deltaW))
        #     setattr(event, self.cfg_ana.dZZ, min(deltaZ))
        #     return True

        else: 
            setattr(event, self.cfg_ana.dWW, min(deltaW))
            setattr(event, self.cfg_ana.dZZ, min(deltaZ))
            setattr(event, self.cfg_ana.pair1_m, mlist[0][0])
            setattr(event, self.cfg_ana.pair2_m, mlist[0][1])
