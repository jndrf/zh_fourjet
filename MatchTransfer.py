from heppy.framework.analyzer import Analyzer

class MatchTransfer(Analyzer):
    '''
    Transfers tags from the matched objects to the jets
    '''

    def process(self, event):
        jets = getattr(event, self.cfg_ana.input_jets)
        genjets = getattr(event, self.cfg_ana.input_genjets)
        gentags = ['ancestor']
        for jet in jets:
            for tag in gentags:
                jet.tags[tag] = False
                if jet.match:
                    jet.tags[tag] = jet.match.tags[tag]

            jet.tags['parton'] = 0
            if jet.match and jet.match.match:
                jet.tags['parton'] = jet.match.match.pdgid()

        for jet in genjets:
            jet.tags['parton'] = 0
            if jet.match:
                jet.tags['parton'] = jet.match.pdgid()
