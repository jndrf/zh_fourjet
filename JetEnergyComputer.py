from heppy.framework.analyzer import Analyzer
import copy
from numpy import array, linalg
import math
from random import gauss

class JetEnergyComputer(Analyzer):
    '''Use the initial p4 to constrain the energy of the 4 jets,
    in ee -> 4 jet final states.
    
    from heppy.analyzers.examples.zh_had.JetEnergyComputer import JetEnergyComputer
    compute_jet_energy = cfg.Analyzer(
      JetEnergyComputer,
      output_jets='rescaled_jets',
      input_jets='jets',
      sqrts=Collider.SQRTS
    )

    * output_jets: output jets with a rescaled energy.
    note that only the jet p4 is copied when creating a rescaled jet
    
    * input_jets: collection of jets to be rescaled
    
    * sqrts: center-of-mass energy of the collision
    
    '''
    
    def getRescaleFactor(self, jets, sqrts):
        '''
rescales the energy so that the sum of all jet energies is sqrt s. Returns a numpy array with the factors.
for method see Future_Colliders_2_2016.pdf, Slide 7.
'''
        rows = []
        
        for i in range(4):
            rows.append([])
        
        for jet in jets:
            e = jet.e()
            rows[0].append(1)
            rows[1].append((jet.p3().Px())/jet.e())
            rows[2].append(jet.p3().Py()/jet.e())
            rows[3].append(jet.p3().Pz()/jet.e())

        constraints = [sqrts, 0, 0, 0]
        
        newnrg = linalg.solve(array(rows), array(constraints))
        jetnrg = array([jet.e() for jet in jets])
        return newnrg/jetnrg

    def chisquare(self, jets, rejets, sigma, event):
        chi2 = 0
        for jet, rejet, in zip(jets, rejets):
            x = (jet.e() - rejet.e())/sigma
            chi2 += x**2
        setattr(event, self.cfg_ana.out_chi, chi2)
        return chi2

    def getChiFromResolution(self, rawjets, rejets, event):
        chi2 = 0
        for jet, rejet in zip(rawjets, rejets):
            uncert = 0.5 * math.sqrt(jet.e()) + 0.05*jet.e()
            x = ((jet.e() - rejet.e())/uncert)**2
            chi2 += x
        setattr(event, self.cfg_ana.out_chi, chi2)
        return chi2

    def process(self, event):
        sqrts = self.cfg_ana.sqrts
        jets = copy.deepcopy(getattr(event, self.cfg_ana.input_jets))
        if len(jets) != 4:
            setattr(event, self.cfg_ana.output_jets, [])
            setattr(event, self.cfg_ana.out_chi, -1)
            return True

        # here solve the equation to get the energy scale factor for each jet.
        scale_factors = self.getRescaleFactor(jets, self.cfg_ana.sqrts*gauss(1, 0.0012)) # spread from arXiv:1605.00100v2
        output = []
        for jet, factor in zip(jets, scale_factors):
            # the jets should not be deepcopied
            # as they are heavy objects containing
            # in particular a list of consistuent particles 
            scaled_jet = copy.copy(jet)
            scaled_jet.tags['raw_e'] = jet.e()
            # scaled_jet._tlv = copy.deepcopy(jet._tlv) # deepcobying is done anyways, no need to do it again.
            scaled_jet._tlv *= factor
#            if scaled_jet.e()<0: break
            output.append(scaled_jet)
            
        # px = 0
        # py = 0
        # pz = 0
        # for j in output:
        #     px += j._tlv.Px()
        #     py += j._tlv.Py()
        #     pz += j._tlv.Pz()

        
        setattr(event, self.cfg_ana.out_chi, 0)
        # if len(output) != 4:
        #     setattr(event, self.cfg_ana.output_jets, [])
        #     return True
        '''
        if self.getChiFromResolution(jets, output, event) >15:
            setattr(event, self.cfg_ana.output_jets, [])
            return True
        '''
        setattr(event, self.cfg_ana.output_jets, output)
        for jet in output:
            if jet.e() == 0:
                return False
            
        for jet in output:
            if jet.e()<0:
                setattr(event, self.cfg_ana.out_chi, -2)
                return True
