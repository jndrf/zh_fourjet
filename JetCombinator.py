from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.jet import Jet
from heppy.particles.jet import JetConstituents

class JetCombinator(Analyzer):
    """
    combines jets
    """

    def process(self, event):
        
