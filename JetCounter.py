from heppy.framework.analyzer import Analyzer

class JetCounter(Analyzer):
    '''
    counts all jets, used to be directlz in theclusterizer.
    but for portability and stuff it is now here
    '''

    def process(self, event):
        jets = getattr(event, self.cfg_ana.input_jets)
        setattr(event, self.cfg_ana.njets, len(jets))
