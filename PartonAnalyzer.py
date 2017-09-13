from heppy.framework.analyzer import Analyzer
from heppy.particles.genbrowser import GenBrowser

class PartonsFromZH(Analyzer):
    
    def process(self, event):
        genptcs = event.gen_particles
        
        event.genbrowser = GenBrowser(event.gen_particles,
                                      event.gen_vertices)
        partons_from_Z = []
        partons_from_H = []
        partons = []
        for ptc in genptcs:

            if not ptc.status() == 23: #Only outgoing partons from hard process
                continue
            
            ancestors = event.genbrowser.ancestors(ptc)
#            print ancestors
#            print ptc
#            print '----'
            is_from_Z = False 
            is_from_H = False             
	    for ancestor in ancestors:
                if ancestor.pdgid()==23:
                    is_from_Z = True
                if ancestor.pdgid()==25:
                    is_from_H = True

            if is_from_Z:
                partons_from_Z.append(ptc)
            elif is_from_H:
                partons_from_H.append(ptc)

            event.partons_from_Z = partons_from_Z
            event.partons_from_H = partons_from_H
#        print partons
#        setattr(event, self.cfg_ana.partons, partons)
#        print '++++'
