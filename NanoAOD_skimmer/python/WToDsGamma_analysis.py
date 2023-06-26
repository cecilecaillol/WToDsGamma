#!/usr/bin/env python
import os, sys, math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

from WToDsGamma.NanoAOD_skimmer.objectSelector import ElectronSelector, MuonSelector, TauSelector, PhotonSelector

class Analysis(Module):
    def __init__(self, channel, isMC):
        self.channel = channel
        self.isMC    = isMC
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    
        self.out = wrappedOutputTree
        self.out.branch("nLepCand",          "I");
        self.out.branch("LepCand_id",        "I",  lenVar = "nLepCand");
        self.out.branch("LepCand_pt",        "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_eta",       "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_phi",       "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_mass",      "F",  lenVar = "nLepCand");
        self.out.branch("LepCand_charge",    "F",  lenVar = "nLepCand");

        self.out.branch("nPhoCand",          "I");
        self.out.branch("PhoCand_pt",        "F",  lenVar = "nPhoCand");
        self.out.branch("PhoCand_eta",       "F",  lenVar = "nPhoCand");
        self.out.branch("PhoCand_phi",       "F",  lenVar = "nPhoCand");

        self.out.branch("nTauCand",          "I");
        self.out.branch("TauCand_pt",        "F",  lenVar = "nTauCand");
        self.out.branch("TauCand_eta",       "F",  lenVar = "nTauCand");
        self.out.branch("TauCand_phi",       "F",  lenVar = "nTauCand");
        self.out.branch("TauCand_mass",      "F",  lenVar = "nTauCand");
        self.out.branch("TauCand_charge",    "F",  lenVar = "nTauCand");
        self.out.branch("TauCand_dm",        "I",  lenVar = "nTauCand");
        self.out.branch("TauCand_DNNvsjet",  "I",  lenVar = "nTauCand");
        self.out.branch("TauCand_DNNvse",  "I",  lenVar = "nTauCand");
        self.out.branch("TauCand_DNNvsmu",  "I",  lenVar = "nTauCand");

        self.out.branch("nJetCand",          "I");
        self.out.branch("JetCand_pt",        "F",  lenVar = "nJetCand");
        self.out.branch("JetCand_eta",       "F",  lenVar = "nJetCand");
        self.out.branch("JetCand_phi",       "F",  lenVar = "nJetCand");
        self.out.branch("JetCand_m",         "F",  lenVar = "nJetCand");
        self.out.branch("JetCand_puid",         "I",  lenVar = "nJetCand");
        self.out.branch("JetCand_jetid",         "I",  lenVar = "nJetCand");
        self.out.branch("JetCand_deepflavB", "F",  lenVar = "nJetCand");
        self.out.branch("JetCand_hadronFlavour", "I",  lenVar = "nJetCand");

        self.out.branch("gen_W_pt",          "F");
        self.out.branch("gen_W_eta",          "F");
        self.out.branch("gen_W_phi",          "F");
        self.out.branch("gen_W_mass",          "F");

        self.out.branch("gen_gamma_pt",          "F");
        self.out.branch("gen_gamma_eta",          "F");
        self.out.branch("gen_gamma_phi",          "F");
        self.out.branch("gen_gamma_mass",          "F");

        self.out.branch("gen_Ds_pt",          "F");
        self.out.branch("gen_Ds_eta",          "F");
        self.out.branch("gen_Ds_phi",          "F");
        self.out.branch("gen_Ds_mass",          "F");

        self.out.branch("gen_Kp_pt",          "F");
        self.out.branch("gen_Kp_eta",          "F");
        self.out.branch("gen_Kp_phi",          "F");
        self.out.branch("gen_Kp_mass",          "F");

        self.out.branch("gen_Km_pt",          "F");
        self.out.branch("gen_Km_eta",          "F");
        self.out.branch("gen_Km_phi",          "F");
        self.out.branch("gen_Km_mass",          "F");

        self.out.branch("gen_phi_pt",          "F");
        self.out.branch("gen_phi_eta",          "F");
        self.out.branch("gen_phi_phi",          "F");
        self.out.branch("gen_phi_mass",          "F");

        self.out.branch("gen_pi_pt",          "F");
        self.out.branch("gen_pi_eta",          "F");
        self.out.branch("gen_pi_phi",          "F");
        self.out.branch("gen_pi_mass",          "F");

        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def selectMuons(self, event, muSel):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if not muSel.evalMuon(mu): continue
            setattr(mu, 'id', 13)
            event.selectedMuons.append(mu)

        event.selectedMuons.sort(key=lambda x: x.pt, reverse=True)

    def selectElectrons(self, event, elSel):
        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            if not elSel.evalElectron(el): continue
            #remove overlap with selected muons 
            deltaR_to_leptons=[ el.p4().DeltaR(lep.p4()) for lep in event.selectedMuons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            setattr(el, 'id', 11)
            event.selectedElectrons.append(el)
        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)

    def selectPhotons(self, event, photonSel):
        event.selectedPhotons = []
        photons = Collection(event, "Photon")
        for pho in photons:
            if not photonSel.evalPhoton(pho): continue
            ##remove overlap with selected muons 
            #deltaR_to_leptons=[ pho.p4().DeltaR(lep.p4()) for lep in event.selectedMuons ]
            #hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            #if hasLepOverlap>0: continue
            event.selectedPhotons.append(pho)
        event.selectedPhotons.sort(key=lambda x: x.pt, reverse=True)


    def selectTaus(self, event, tauSel):
        event.selectedTaus = []
        taus = Collection(event, "Tau")
        for tau in taus:
            #remove overlap with selected electrons and muons 
            deltaR_to_leptons=[ tau.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            if not tauSel.evalTau(tau): continue
            setattr(tau, 'id', 15)
            event.selectedTaus.append(tau)
        event.selectedTaus.sort(key=lambda x: x.pt, reverse=True)



    def selectAK4Jets(self, event):
        ## Selected jets: pT>30, |eta|<4.7, pass tight ID
        
        event.selectedAK4Jets = []
        ak4jets = Collection(event, "Jet")
        for j in ak4jets:

            if j.pt<30 : 
                continue

            if abs(j.eta) > 4.7:
                continue
            
            if j.jetId<1: 
                continue
                
            #remove overlap with selected leptons 
            deltaR_to_leptons=[ j.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons+event.selectedTaus ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            event.selectedAK4Jets.append(j)
            
        event.selectedAK4Jets.sort(key=lambda x: x.pt, reverse=True)

    def selectGenParticles(self, event):

        event.selectedGenParticles = []
        genparticles = Collection(event, "GenPart")
        for genp in genparticles:
            event.selectedGenParticles.append(genp)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        

	event.gen_W=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        event.gen_Ds=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        event.gen_gamma=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        event.gen_Kp=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        event.gen_Km=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        event.gen_pi=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
        event.gen_phi=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
	# 22 = photon; 24 = W; 431 = D_s; 321 = K+; 333 = phi; 211 = pi
        if self.isMC:
           self.selectGenParticles(event)
           for genp in event.selectedGenParticles:
              #print genp.pdgId,genp.pt,genp.eta,genp.phi,event.selectedGenParticles[genp.genPartIdxMother].pdgId
	      if genp.pdgId==22 and abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==24 : 
		  event.gen_gamma.SetPtEtaPhiM(genp.pt,genp.eta,genp.phi,genp.mass)
                  event.gen_W.SetPtEtaPhiM(event.selectedGenParticles[genp.genPartIdxMother].pt,event.selectedGenParticles[genp.genPartIdxMother].eta,event.selectedGenParticles[genp.genPartIdxMother].phi,event.selectedGenParticles[genp.genPartIdxMother].mass)
              if abs(genp.pdgId)==431 and abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==24 :
                  event.gen_Ds.SetPtEtaPhiM(genp.pt,genp.eta,genp.phi,genp.mass)
              if genp.pdgId==321 and (abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==431 or abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==333) :
                  event.gen_Kp.SetPtEtaPhiM(genp.pt,genp.eta,genp.phi,genp.mass)
	          if (abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==333):
                     event.gen_phi.SetPtEtaPhiM(genp.pt,genp.eta,genp.phi,genp.mass)
              if genp.pdgId==-321 and (abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==431 or abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==333) :
                  event.gen_Km.SetPtEtaPhiM(genp.pt,genp.eta,genp.phi,genp.mass)
              if abs(genp.pdgId)==211 and abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==431 :
                  event.gen_pi.SetPtEtaPhiM(genp.pt,genp.eta,genp.phi,genp.mass)


        elSel = ElectronSelector()
        muSel = MuonSelector()
        tauSel = TauSelector()
        photonSel = PhotonSelector()
        
        # apply object selection
        self.selectMuons(event, muSel)
        self.selectElectrons(event, elSel)
        self.selectTaus(event, tauSel)
        self.selectPhotons(event, photonSel)
        self.selectAK4Jets(event)
        
        #apply event selection at reco-level depending on the channel:
        #if self.channel=="tt":
        #    if (len(event.selectedElectrons)+len(event.selectedMuons))!=1: return False
        #if self.channel=="w":
        #    if (len(event.selectedElectrons)+len(event.selectedMuons))!=0: return False
        #if self.channel=="w" or self.channel=="tt":
        #    if len(event.selectedPhotons)!=1: return False


        ######################################################
        ##### HIGH LEVEL VARIABLES FOR SELECTED EVENTS   #####
        ######################################################
        
        event.selectedLeptons=event.selectedElectrons+event.selectedMuons
        event.selectedLeptons.sort(key=lambda x: x.pt, reverse=True)
        
        lep_id       = [lep.id for lep in event.selectedLeptons]
        lep_pt       = [lep.pt for lep in event.selectedLeptons]
        lep_eta      = [lep.eta for lep in event.selectedLeptons]
        lep_phi      = [lep.phi for lep in event.selectedLeptons]
        lep_mass     = [lep.mass for lep in event.selectedLeptons]
        lep_charge   = [lep.charge for lep in event.selectedLeptons]

        pho_pt       = [pho.pt for pho in event.selectedPhotons]
        pho_eta      = [pho.eta for pho in event.selectedPhotons]
        pho_phi      = [pho.phi for pho in event.selectedPhotons]

        tau_pt       = [tau.pt for tau in event.selectedTaus]
        tau_eta      = [tau.eta for tau in event.selectedTaus]
        tau_phi      = [tau.phi for tau in event.selectedTaus]
        tau_mass     = [tau.mass for tau in event.selectedTaus]
        tau_charge   = [tau.charge for tau in event.selectedTaus]
        tau_dm       = [tau.decayMode for tau in event.selectedTaus]
        tau_DNNvsjet = [tau.idDeepTau2017v2p1VSjet for tau in event.selectedTaus]
        tau_DNNvse   = [tau.idDeepTau2017v2p1VSe for tau in event.selectedTaus]
        tau_DNNvsmu  = [tau.idDeepTau2017v2p1VSmu for tau in event.selectedTaus]

        jet_pt       = [jet.pt for jet in event.selectedAK4Jets]
        jet_eta      = [jet.eta for jet in event.selectedAK4Jets]
        jet_phi      = [jet.phi for jet in event.selectedAK4Jets]
        jet_m        = [jet.mass for jet in event.selectedAK4Jets]
        jet_deepflavB= [jet.btagDeepFlavB for jet in event.selectedAK4Jets]
        jet_puid     = [jet.puId for jet in event.selectedAK4Jets]
        jet_jetid    = [jet.jetId for jet in event.selectedAK4Jets]
        jet_hadronflavour = []
        for jet in event.selectedAK4Jets:
           if self.isMC:
                jet_hadronflavour.append(jet.hadronFlavour)
           else:
                jet_hadronflavour.append(-1)

        ## store branches
        self.out.fillBranch("nLepCand",               len(event.selectedLeptons))
        self.out.fillBranch("LepCand_id" ,            lep_id)
        self.out.fillBranch("LepCand_pt" ,            lep_pt)
        self.out.fillBranch("LepCand_eta" ,           lep_eta)
        self.out.fillBranch("LepCand_phi" ,           lep_phi)
        self.out.fillBranch("LepCand_mass" ,          lep_mass)
        self.out.fillBranch("LepCand_charge" ,        lep_charge)

        self.out.fillBranch("nPhoCand",               len(event.selectedPhotons))
        self.out.fillBranch("PhoCand_pt" ,            pho_pt)
        self.out.fillBranch("PhoCand_eta" ,           pho_eta)
        self.out.fillBranch("PhoCand_phi" ,           pho_phi)

        self.out.fillBranch("nTauCand",               len(event.selectedTaus))
        self.out.fillBranch("TauCand_pt" ,            tau_pt)
        self.out.fillBranch("TauCand_eta" ,           tau_eta)
        self.out.fillBranch("TauCand_phi" ,           tau_phi)
        self.out.fillBranch("TauCand_mass" ,          tau_mass)
        self.out.fillBranch("TauCand_charge" ,        tau_charge)
        self.out.fillBranch("TauCand_dm" ,            tau_dm)
        self.out.fillBranch("TauCand_DNNvsjet" ,      tau_DNNvsjet)
        self.out.fillBranch("TauCand_DNNvsmu" ,       tau_DNNvsmu)
        self.out.fillBranch("TauCand_DNNvse" ,        tau_DNNvse)

        self.out.fillBranch("nJetCand" ,              len(event.selectedAK4Jets))
        self.out.fillBranch("JetCand_pt",             jet_pt);
        self.out.fillBranch("JetCand_eta",            jet_eta);
        self.out.fillBranch("JetCand_phi",            jet_phi);
        self.out.fillBranch("JetCand_m",              jet_m);
        self.out.fillBranch("JetCand_puid",           jet_puid);
        self.out.fillBranch("JetCand_jetid",          jet_jetid);
        self.out.fillBranch("JetCand_deepflavB",      jet_deepflavB);
        self.out.fillBranch("JetCand_hadronFlavour",  jet_hadronflavour);

        if self.isMC:
           self.out.fillBranch("gen_W_pt",event.gen_W.Pt())
           self.out.fillBranch("gen_W_eta",event.gen_W.Eta())
           self.out.fillBranch("gen_W_phi",event.gen_W.Phi())
           self.out.fillBranch("gen_W_mass",event.gen_W.M())

           self.out.fillBranch("gen_gamma_pt",event.gen_gamma.Pt())
           self.out.fillBranch("gen_gamma_eta",event.gen_gamma.Eta())
           self.out.fillBranch("gen_gamma_phi",event.gen_gamma.Phi())
           self.out.fillBranch("gen_gamma_mass",event.gen_gamma.M())

           self.out.fillBranch("gen_Ds_pt",event.gen_Ds.Pt())
           self.out.fillBranch("gen_Ds_eta",event.gen_Ds.Eta())
           self.out.fillBranch("gen_Ds_phi",event.gen_Ds.Phi())
           self.out.fillBranch("gen_Ds_mass",event.gen_Ds.M())

           self.out.fillBranch("gen_Kp_pt",event.gen_Kp.Pt())
           self.out.fillBranch("gen_Kp_eta",event.gen_Kp.Eta())
           self.out.fillBranch("gen_Kp_phi",event.gen_Kp.Phi())
           self.out.fillBranch("gen_Kp_mass",event.gen_Kp.M())

           self.out.fillBranch("gen_Km_pt",event.gen_Km.Pt())
           self.out.fillBranch("gen_Km_eta",event.gen_Km.Eta())
           self.out.fillBranch("gen_Km_phi",event.gen_Km.Phi())
           self.out.fillBranch("gen_Km_mass",event.gen_Km.M())

           self.out.fillBranch("gen_phi_pt",event.gen_phi.Pt())
           self.out.fillBranch("gen_phi_eta",event.gen_phi.Eta())
           self.out.fillBranch("gen_phi_phi",event.gen_phi.Phi())
           self.out.fillBranch("gen_phi_mass",event.gen_phi.M())

           self.out.fillBranch("gen_pi_pt",event.gen_pi.Pt())
           self.out.fillBranch("gen_pi_eta",event.gen_pi.Eta())
           self.out.fillBranch("gen_pi_phi",event.gen_pi.Phi())
           self.out.fillBranch("gen_pi_mass",event.gen_pi.M())


        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
analysis_wmc    = lambda : Analysis(channel="w", isMC=True)
analysis_wdata  = lambda : Analysis(channel="w", isMC=False)

analysis_ttmc    = lambda : Analysis(channel="tt", isMC=True)
analysis_ttdata  = lambda : Analysis(channel="tt", isMC=False)

