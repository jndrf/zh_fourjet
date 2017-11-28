from heppy.framework.analyzer import Analyzer
from heppy.particles.genbrowser import GenBrowser

class AncestorSeeker(Analyzer):
    
    def process(self, event):
        genjets = getattr(event, self.cfg_ana.input_jets)
        for jet in genjets:
            jet.tags['ancestor'] = 0
            if jet.match:
                genbrowser = GenBrowser([jet.match], event.gen_vertices)
                ancestors = genbrowser.ancestors(jet.match)
                for ancestor in ancestors:
                    if ancestor.pdgid()>=21 and ancestor.pdgid()<=37: #all gauge bosons, incl. bsm
                        jet.tags['ancestor'] = ancestor.pdgid()
            print jet

