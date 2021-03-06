from CMGTools.TTHAnalysis.treeReAnalyzer import *
from ROOT import TLorentzVector, TVector2, std
import ROOT
import time
import itertools
import PhysicsTools.Heppy.loadlibs
import array
import operator
import math

# mc to data pu weight
def getPUdict(fname, puHistName = "h_ratio"):
    puDict = {}

    puFile = ROOT.TFile(fname,"READ")
    hPUw = puFile.Get(puHistName)

    if not hPUw:
        print "PU hist not found!"
        exit(0)

    for ibin in range(1,hPUw.GetNbinsX()):

        #npv = hPUw.GetXaxis().GetBinLowEdge(ibin)
        npv = int(hPUw.GetXaxis().GetBinCenter(ibin))
        rat = hPUw.GetBinContent(ibin)

        puDict[npv] = rat

    puFile.Close()

    return puDict

# pu histo file name
#puFileName_norm = "../python/tools/pileup/pu_ratio_80mb.root"
#puFileName_up = "../python/tools/pileup/pu_ratio_84mb.root"
#puFileName_down = "../python/tools/pileup/pu_ratio_76mb.root"

'''
puFileName_up = "../python/tools/pileup/pu_ratio_74mb.root"
puFileName_norm = "../python/tools/pileup/pu_ratio_70mb.root"
puFileName_down = "../python/tools/pileup/pu_ratio_66mb.root"
'''

'''
#2015 final
puFileName_up = "../python/tools/pileup/pu_ratio_72p45mb.root"
puFileName_norm = "../python/tools/pileup/pu_ratio_69mb.root"
puFileName_down = "../python/tools/pileup/pu_ratio_65p55mb.root"
'''

#2016 4/fb
#puFileName_up   = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/pileup/pufiles/pu_ratio_4fb_Run2016B_74.9mb.root"
#puFileName_norm = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/pileup/pufiles/pu_ratio_4fb_Run2016B_71.3mb.root"
#puFileName_down = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/pileup/pufiles/pu_ratio_4fb_Run2016B_67.7mb.root"


#2016 ICHEP
#puFileName_up = "../python/tools/pileup/h_ratio_66p15.root"
#puFileName_norm = "../python/tools/pileup/h_ratio_63.root"
#puFileName_down = "../python/tools/pileup/h_ratio_59p85.root"

# 2017 Moriond
puFileName_up = "../python/tools/pileup/h_ratio_Moriond2017_72380.root"
puFileName_norm = "../python/tools/pileup/h_ratio_Moriond2017_69200.root"
puFileName_down = "../python/tools/pileup/h_ratio_Moriond2017_66010.root"

puNorm =  getPUdict(puFileName_norm)
puUp =  getPUdict(puFileName_up)
puDown =  getPUdict(puFileName_down)

print 80*"#"
print "Loaded PU weights!"
print puNorm

class EventVars1L_pileup:
    def __init__(self):
        self.branches = [
            'nVtx', 'nTrueInt',
            'puRatio','puRatio_up','puRatio_down'
            ]

    def listBranches(self):
        return self.branches[:]

    def __call__(self,event,base):

        # output dict:
        ret = {}

        if not event.isData:

            ret['nVtx'] = event.nVert

            nTrueInt = event.nTrueInt
            ret['nTrueInt'] = nTrueInt

            floornTrueInt = math.floor(nTrueInt)

            if floornTrueInt in puNorm:
                ret['puRatio'] = puNorm[floornTrueInt]
                ret['puRatio_up'] = puUp[floornTrueInt]
                ret['puRatio_down'] = puDown[floornTrueInt]
            else:
                ret['puRatio'] = 0
                ret['puRatio_up'] = 0
                ret['puRatio_down'] = 0
        else:
            ret['puRatio'] = 1
            ret['puRatio_up'] = 1
            ret['puRatio_down'] = 1


        return ret

if __name__ == '__main__':
    from sys import argv
    file = ROOT.TFile(argv[1])
    tree = file.Get("tree")
    class Tester(Module):
        def __init__(self, name):
            Module.__init__(self,name,None)
            self.sf = EventVars1L()
        def analyze(self,ev):
            print "\nrun %6d lumi %4d event %d: leps %d" % (ev.run, ev.lumi, ev.evt, ev.nLepGood)
            print self.sf(ev)
    el = EventLoop([ Tester("tester") ])
    el.loop([tree], maxEvents = 50)
