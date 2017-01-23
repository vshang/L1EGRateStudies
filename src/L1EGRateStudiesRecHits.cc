// -*- C++ -*-
//
// Package:    L1EGRateStudiesRecHits
// Class:      L1EGRateStudiesRecHits
// 
/**\class L1EGRateStudiesRecHits L1EGRateStudiesRecHits.cc SLHCUpgradeSimulations/L1EGRateStudies/src/L1EGRateStudiesRecHits.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Nick Smith
//         Created:  Mon Mar 10 13:27:23 CDT 2014
// $Id$
//
//


// system include files
#include <memory>
#include <array>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"
#include "TTree.h"
#include "TMath.h"

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/SLHC/interface/L1EGCrystalCluster.h"
#include "SimDataFormats/SLHC/src/classes.h"

#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include "FastSimulation/BaseParticlePropagator/interface/BaseParticlePropagator.h"
//#include "FastSimulation/Particle/interface/ParticleTable.h"

//#include "SimDataFormats/SLHC/interface/StackedTrackerTypes.h"
//#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
//#include "DataFormats/L1TrackTrigger/interface/TTPixelTrack.h"
//#include "DataFormats/L1TrackTrigger/interface/L1TkPrimaryVertex.h"
//#include "SLHCUpgradeSimulations/L1TrackTrigger/interface/L1TkElectronTrackMatchAlgo.h"

#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"

#include "FastSimulation/Particle/interface/RawParticle.h"
//
// class declaration
//
class L1EGRateStudiesRecHits : public edm::EDAnalyzer {

   public:
      explicit L1EGRateStudiesRecHits(const edm::ParameterSet&);
      ~L1EGRateStudiesRecHits();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      //virtual void endRun(edm::Run const&, edm::EventSetup const&);
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // -- user functions
      void integrateDown(TH1F *);
      void fill_tree(const l1slhc::L1EGCrystalCluster& cluster);
      bool cluster_passes_cuts(const l1slhc::L1EGCrystalCluster& cluster) const;
      bool checkTowerExists(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps) const;
      //void checkRecHitsFlags(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps, const EcalRecHitCollection &ecalRecHits) const;
      
      // ----------member data ---------------------------
      bool doEfficiencyCalc;
      bool useOfflineClusters;
      bool debug;
      bool useEndcap;
      
      double genMatchDeltaRcut;
      double genMatchRelPtcut;
      
      int eventCount;
      //std::vector<edm::InputTag> L1EGammaInputTags;
      edm::InputTag L1CrystalClustersInputTag;
      edm::InputTag offlineRecoClusterInputTag;

      edm::EDGetTokenT<l1slhc::L1EGCrystalClusterCollection> crystalClustersToken_;
      l1slhc::L1EGCrystalClusterCollection crystalClusters;
      edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;      

      edm::EDGetTokenT<reco::GenParticleCollection> genCollectionToken_;
      reco::GenParticleCollection genParticles;
      //iEvent.getByLabel("genParticles", genParticleHandle);
      edm::Handle<reco::GenParticleCollection> genParticleHandle;

      edm::EDGetTokenT<EcalRecHitCollection> ecalRecHitEBToken_;
      //edm::EDGetTokenT<EcalRecHitCollection> ecalRecHitEEToken_;

      edm::EDGetTokenT<reco::SuperClusterCollection> offlineRecoClusterToken_;
      edm::Handle<reco::SuperClusterCollection> offlineRecoClustersHandle;
            
      int nHistBins, nHistEtaBins;
      double histLow;
      double histHigh;
      double histetaLow;
      double histetaHigh;
      TH1F * efficiency_denominator_hist;
      TH1F * efficiency_denominator_eta_hist;
      TH1F * efficiency_denominator_reco_hist;

      TH1F * dyncrystal_efficiency_hist;
      std::map<double, TH1F *> dyncrystal_efficiency_reco_hists; // Turn-on thresholds
      std::map<double, TH1F *> dyncrystal_efficiency_gen_hists; // Turn-on thresholds
      TH1F * dyncrystal_efficiency_bremcut_hist;
      TH1F * dyncrystal_efficiency_eta_hist;
      TH1F * dyncrystal_deltaR_hist;
      TH1F * dyncrystal_deltaR_bremcut_hist;
      TH1F * dyncrystal_deta_hist;
      TH1F * dyncrystal_dphi_hist;
      TH1F * dyncrystal_dphi_bremcut_hist;
      TH1F * dyncrystal_rate_hist;
      TH2F * dyncrystal_2DdeltaR_hist;

      std::map<std::string, TH1F *> EGalg_efficiency_hists;
      std::map<std::string, std::map<double, TH1F *>> EGalg_efficiency_reco_hists;
      std::map<std::string, std::map<double, TH1F *>> EGalg_efficiency_gen_hists;
      std::map<std::string, TH1F *> EGalg_efficiency_eta_hists;
      std::map<std::string, TH1F *> EGalg_deltaR_hists;
      std::map<std::string, TH1F *> EGalg_deta_hists;
      std::map<std::string, TH1F *> EGalg_dphi_hists;
      std::map<std::string, TH1F *> EGalg_rate_hists;
      std::map<std::string, TH2F *> EGalg_2DdeltaR_hists;
      std::map<std::string, TH2F *> EGalg_reco_gen_pt_hists;
      std::map<std::string, TH1F *> EGalg_reco_gen_pt_1dHists;

      // EcalRecHits flags
      TH1I * RecHitFlagsTowerHist;
      TH1I * RecHitFlagsNoTowerHist;

      // Crystal pt stuff
      TTree * crystal_tree;
      struct {
         double run;
         double lumi;
         double event;
         std::array<float, 6> crystal_pt;
         int   crystalCount;
         float cluster_pt;
         float cluster_energy;
         float eta;
         float phi;
         float hovere;
         float iso;
         float bremStrength;
         float e2x5;
         float e3x5;
         float e5x5;
         float deltaR = 0.;
         float deltaPhi = 0.;
         float deltaEta = 0.;
         float gen_pt = 0.;
         float gen_z = 999.;
         float gen_eta = 0.;
         float gen_phi = 0.;
         float gen_energy = 0.;
         float gen_charge = 0.;
         float E_gen = 0.;
         float denom_pt = 0.;
         float reco_pt = 0.;
         float reco_eta = -99.;
         float reco_phi = -99.;
         bool  passed = false;
         int   nthCandidate = -1;
         bool  endcap = false;
         float uslPt = 0.;
         float lslPt = 0.;
         float corePt = 0.;
         float E_core = 0.;
         float phiStripContiguous0;
         float phiStripOneHole0;
         float phiStripContiguous3p;
         float phiStripOneHole3p;
         float trackDeltaR;
         float trackZ;
         float trackEta;
         float trackPhi;
         float trackDeltaPhi;
         float trackDeltaEta;
         float trackP;
         float trackPt;
         float trackHighestPt;
         float trackHighestPtEta;
         float trackHighestPtPhi;
         float trackHighestPtChi2;
         float trackHighestPtCutChi2;
         float trackHighestPtCutChi2Eta;
         float trackHighestPtCutChi2Phi;
         float trackHighestPtCutChi2Chi2;
         float trackRInv;
         float trackChi2;
         float trackIsoConeTrackCount;
         float trackIsoConePtSum;
         float zVertex;
         float zVertexEnergy;
      } treeinfo;

      // (pt_reco-pt_gen)/pt_gen plot
      TH2F * reco_gen_pt_hist;
      TH1F * reco_gen_pt_1dHist;

      // dphi vs. brem
      TH2F * brem_dphi_hist;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
L1EGRateStudiesRecHits::L1EGRateStudiesRecHits(const edm::ParameterSet& iConfig) :
   doEfficiencyCalc(iConfig.getUntrackedParameter<bool>("doEfficiencyCalc", false)),
   useOfflineClusters(iConfig.getUntrackedParameter<bool>("useOfflineClusters", false)),
   debug(iConfig.getUntrackedParameter<bool>("debug", false)),
   useEndcap(iConfig.getUntrackedParameter<bool>("useEndcap", false)),
   genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.1)),
   genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
   crystalClustersToken_(consumes<l1slhc::L1EGCrystalClusterCollection>(iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag"))),
   genCollectionToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"))),
   ecalRecHitEBToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ecalRecHitEB"))),
   //ecalRecHitEEToken_(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("ecalRecHitEE"))),
   offlineRecoClusterToken_(consumes<reco::SuperClusterCollection>(iConfig.getParameter<edm::InputTag>("OfflineRecoClustersInputTag"))),
   nHistBins(iConfig.getUntrackedParameter<int>("histogramBinCount", 10)),
   nHistEtaBins(iConfig.getUntrackedParameter<int>("histogramEtaBinCount", 20)),
   histLow(iConfig.getUntrackedParameter<double>("histogramRangeLow", 0.)),
   histHigh(iConfig.getUntrackedParameter<double>("histogramRangeHigh", 50.)),
   histetaLow(iConfig.getUntrackedParameter<double>("histogramRangeetaLow", -2.5)),
   histetaHigh(iConfig.getUntrackedParameter<double>("histogramRangeetaHigh", 2.5))
{
   eventCount = 0;
   //L1EGammaInputTags = iConfig.getParameter<std::vector<edm::InputTag>>("L1EGammaInputTags");
   //L1EGammaInputTags.push_back(edm::InputTag("l1extraParticles:All"));
   //L1EGammaInputTags.push_back(edm::InputTag("l1extraParticlesUCT:All"));
   //L1CrystalClustersInputTag = iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag");

   edm::Service<TFileService> fs;
   
   // If using offline-reco clusters, label dR & related hists appropriately
   std::string drLabel("(Gen-Reco);Counts");
   if ( useOfflineClusters ) drLabel = "(vs. Offline Reco.);Counts";

   // Make a set of histograms to fill, depending on if we are doing rate or efficiency
   if ( doEfficiencyCalc )
   {
      auto thresholds = iConfig.getUntrackedParameter<std::vector<int>>("turnOnThresholds");
      //offlineRecoClusterInputTag = iConfig.getParameter<edm::InputTag>("OfflineRecoClustersInputTag");

      dyncrystal_efficiency_hist = fs->make<TH1F>("dyncrystalEG_efficiency_pt", "Dynamic Crystal Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      dyncrystal_efficiency_bremcut_hist = fs->make<TH1F>("dyncrystalEG_efficiency_bremcut_pt", "Dynamic Crystal Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      dyncrystal_efficiency_eta_hist = fs->make<TH1F>("dyncrystalEG_efficiency_eta", "Dynamic Crystal Trigger;Gen. #eta;Efficiency", nHistEtaBins, histetaLow, histetaHigh);
      // Implicit conversion from int to double
      for(int threshold : thresholds)
      {
         dyncrystal_efficiency_reco_hists[threshold] = fs->make<TH1F>(("dyncrystalEG_threshold"+std::to_string(threshold)+"_efficiency_reco_pt").c_str(), "Dynamic Crystal Trigger;Offline reco. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
         dyncrystal_efficiency_gen_hists[threshold] = fs->make<TH1F>(("dyncrystalEG_threshold"+std::to_string(threshold)+"_efficiency_gen_pt").c_str(), "Dynamic Crystal Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      }
      dyncrystal_deltaR_hist = fs->make<TH1F>("dyncrystalEG_deltaR", ("Dynamic Crystal Trigger;#Delta R "+drLabel).c_str(), 50, 0., genMatchDeltaRcut);
      dyncrystal_deltaR_bremcut_hist = fs->make<TH1F>("dyncrystalEG_deltaR_bremcut", ("Dynamic Crystal Trigger;#Delta R "+drLabel).c_str(), 50, 0., genMatchDeltaRcut);
      dyncrystal_deta_hist = fs->make<TH1F>("dyncrystalEG_deta", ("Dynamic Crystal Trigger;d#eta "+drLabel).c_str(), 100, -0.25, 0.25);
      dyncrystal_dphi_hist = fs->make<TH1F>("dyncrystalEG_dphi", ("Dynamic Crystal Trigger;d#phi "+drLabel).c_str(), 100, -0.25, 0.25);
      dyncrystal_dphi_bremcut_hist = fs->make<TH1F>("dyncrystalEG_dphi_bremcut", ("Dynamic Crystal Trigger;d#phi "+drLabel).c_str(), 50, -0.1, 0.1);
      dyncrystal_2DdeltaR_hist = fs->make<TH2F>("dyncrystalEG_2DdeltaR_hist", "Dynamic Crystal Trigger;d#eta;d#phi;Counts", 50, -0.05, 0.05, 50, -0.05, 0.05);

      //for(auto& inputTag : L1EGammaInputTags)
      //{
      //   const std::string &name = inputTag.encode();
      //   EGalg_efficiency_hists[name] = fs->make<TH1F>((name+"_efficiency_pt").c_str(), (name+";Gen. pT (GeV);Efficiency").c_str(), nHistBins, histLow, histHigh);
      //   EGalg_efficiency_eta_hists[name] = fs->make<TH1F>((name+"_efficiency_eta").c_str(), (name+";Gen. #eta;Efficiency").c_str(), nHistEtaBins, histetaLow, histetaHigh);
      //   // Implicit conversion from int to double
      //   for(int threshold : thresholds)
      //   {
      //      EGalg_efficiency_reco_hists[name][threshold] = fs->make<TH1F>((name+"_threshold"+std::to_string(threshold)+"_efficiency_reco_pt").c_str(), (name+";Offline reco. pT (GeV);Efficiency").c_str(), nHistBins, histLow, histHigh);
      //      EGalg_efficiency_gen_hists[name][threshold] = fs->make<TH1F>((name+"_threshold"+std::to_string(threshold)+"_efficiency_gen_pt").c_str(), (name+";Gen. pT (GeV);Efficiency").c_str(), nHistBins, histLow, histHigh);
      //   }
      //   EGalg_deltaR_hists[name] = fs->make<TH1F>((name+"_deltaR").c_str(), (name+";#Delta R "+drLabel).c_str(), 50, 0., genMatchDeltaRcut);
      //   EGalg_deta_hists[name] = fs->make<TH1F>((name+"_deta").c_str(), (name+";d#eta "+drLabel).c_str(), 100, -0.25, 0.25);
      //   EGalg_dphi_hists[name] = fs->make<TH1F>((name+"_dphi").c_str(), (name+";d#phi "+drLabel).c_str(), 100, -0.25, 0.25);
      //   EGalg_2DdeltaR_hists[name] = fs->make<TH2F>((name+"_2DdeltaR").c_str(), ";d#eta;d#phi;Counts", 50, -0.05, 0.05, 50, -0.05, 0.05);
      //   EGalg_reco_gen_pt_hists[name] = fs->make<TH2F>((name+"_reco_gen_pt").c_str(), (name+";Gen. pT (GeV);(reco-gen)/gen;Counts").c_str(), 40, 0., 50., 40, -0.3, 0.3); 
      //   EGalg_reco_gen_pt_1dHists[name] = fs->make<TH1F>((name+"_1d_reco_gen_pt").c_str(), (name+";(reco-gen)/gen;Counts").c_str(), 100, -1., 1.); 
      //}

      reco_gen_pt_hist = fs->make<TH2F>("reco_gen_pt" , "EG relative momentum error;Gen. pT (GeV);(reco-gen)/gen;Counts", 40, 0., 50., 40, -0.3, 0.3); 
      reco_gen_pt_1dHist = fs->make<TH1F>("1d_reco_gen_pt" , "EG relative momentum error;(reco-gen)/gen;Counts", 100, -1., 1.); 
      brem_dphi_hist = fs->make<TH2F>("brem_dphi_hist" , "Brem. strength vs. d#phi;Brem. Strength;d#phi;Counts", 40, 0., 2., 40, -0.05, 0.05); 

      efficiency_denominator_hist = fs->make<TH1F>("gen_pt", "Gen. pt;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_reco_hist = fs->make<TH1F>("reco_pt", "Offline reco. pt;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_eta_hist = fs->make<TH1F>("gen_eta", "Gen. #eta;Gen. #eta; Counts", nHistEtaBins, histetaLow, histetaHigh);
   }
   else
   {
      dyncrystal_rate_hist = fs->make<TH1F>("dyncrystalEG_rate" , "Dynamic Crystal Trigger;ET Threshold (GeV);Rate (kHz)", nHistBins, histLow, histHigh);
      //for(auto& inputTag : L1EGammaInputTags)
      //{
      //   const std::string &name = inputTag.encode();
      //   EGalg_rate_hists[name] = fs->make<TH1F>((name+"_rate").c_str() , (name+";ET Threshold (GeV);Rate (kHz)").c_str(), nHistBins, histLow, histHigh);
      //}
   }
   RecHitFlagsTowerHist = fs->make<TH1I>("recHitFlags_tower", "EcalRecHit status flags when tower exists;Flag;Counts", 20, 0, 19);
   RecHitFlagsNoTowerHist = fs->make<TH1I>("recHitFlags_notower", "EcalRecHit status flags when tower exists;Flag;Counts", 20, 0, 19);

   crystal_tree = fs->make<TTree>("crystal_tree", "Crystal cluster individual crystal pt values");
   crystal_tree->Branch("run", &treeinfo.run);
   crystal_tree->Branch("lumi", &treeinfo.lumi);
   crystal_tree->Branch("event", &treeinfo.event);
   crystal_tree->Branch("passed", &treeinfo.passed);
   crystal_tree->Branch("pt", &treeinfo.crystal_pt, "1:2:3:4:5:6");
   crystal_tree->Branch("crystalCount", &treeinfo.crystalCount);
   crystal_tree->Branch("cluster_pt", &treeinfo.cluster_pt);
   crystal_tree->Branch("cluster_energy", &treeinfo.cluster_energy);
   crystal_tree->Branch("eta", &treeinfo.eta);
   crystal_tree->Branch("phi", &treeinfo.phi);
   crystal_tree->Branch("cluster_hovere", &treeinfo.hovere);
   crystal_tree->Branch("cluster_iso", &treeinfo.iso);
   crystal_tree->Branch("bremStrength", &treeinfo.bremStrength);
   crystal_tree->Branch("e2x5", &treeinfo.e2x5);
   crystal_tree->Branch("e3x5", &treeinfo.e3x5);
   crystal_tree->Branch("e5x5", &treeinfo.e5x5);
   crystal_tree->Branch("deltaR", &treeinfo.deltaR);
   crystal_tree->Branch("deltaPhi", &treeinfo.deltaPhi);
   crystal_tree->Branch("deltaEta", &treeinfo.deltaEta);
   crystal_tree->Branch("gen_pt", &treeinfo.gen_pt);
   crystal_tree->Branch("gen_z", &treeinfo.gen_z);
   crystal_tree->Branch("gen_eta", &treeinfo.gen_eta);
   crystal_tree->Branch("gen_phi", &treeinfo.gen_phi);
   crystal_tree->Branch("gen_energy", &treeinfo.gen_energy);
   crystal_tree->Branch("gen_charge", &treeinfo.gen_charge);
   crystal_tree->Branch("E_gen", &treeinfo.E_gen);
   crystal_tree->Branch("denom_pt", &treeinfo.denom_pt);
   crystal_tree->Branch("reco_pt", &treeinfo.reco_pt);
   crystal_tree->Branch("reco_eta", &treeinfo.reco_eta);
   crystal_tree->Branch("reco_phi", &treeinfo.reco_phi);
   crystal_tree->Branch("nthCandidate", &treeinfo.nthCandidate);
   crystal_tree->Branch("endcap", &treeinfo.endcap);
   crystal_tree->Branch("uslPt", &treeinfo.uslPt);
   crystal_tree->Branch("lslPt", &treeinfo.lslPt);
   crystal_tree->Branch("corePt", &treeinfo.corePt);
   crystal_tree->Branch("E_core", &treeinfo.E_core);
   crystal_tree->Branch("phiStripContiguous0", &treeinfo.phiStripContiguous0);
   crystal_tree->Branch("phiStripOneHole0", &treeinfo.phiStripOneHole0);
   crystal_tree->Branch("phiStripContiguous3p", &treeinfo.phiStripContiguous3p);
   crystal_tree->Branch("phiStripOneHole3p", &treeinfo.phiStripOneHole3p);
   crystal_tree->Branch("trackDeltaR", &treeinfo.trackDeltaR);
   crystal_tree->Branch("trackZ", &treeinfo.trackZ);
   crystal_tree->Branch("trackEta", &treeinfo.trackEta);
   crystal_tree->Branch("trackPhi", &treeinfo.trackPhi);
   crystal_tree->Branch("trackDeltaPhi", &treeinfo.trackDeltaPhi);
   crystal_tree->Branch("trackDeltaEta", &treeinfo.trackDeltaEta);
   crystal_tree->Branch("trackP", &treeinfo.trackP);
   crystal_tree->Branch("trackPt", &treeinfo.trackPt);
   crystal_tree->Branch("trackHighestPt", &treeinfo.trackHighestPt);
   crystal_tree->Branch("trackHighestPtEta", &treeinfo.trackHighestPtEta);
   crystal_tree->Branch("trackHighestPtPhi", &treeinfo.trackHighestPtPhi);
   crystal_tree->Branch("trackHighestPtChi2", &treeinfo.trackHighestPtChi2);
   crystal_tree->Branch("trackHighestPtCutChi2", &treeinfo.trackHighestPtCutChi2);
   crystal_tree->Branch("trackHighestPtCutChi2Eta", &treeinfo.trackHighestPtCutChi2Eta);
   crystal_tree->Branch("trackHighestPtCutChi2Phi", &treeinfo.trackHighestPtCutChi2Phi);
   crystal_tree->Branch("trackHighestPtCutChi2Chi2", &treeinfo.trackHighestPtCutChi2Chi2);
   crystal_tree->Branch("trackRInv", &treeinfo.trackRInv);
   crystal_tree->Branch("trackChi2", &treeinfo.trackChi2);
   crystal_tree->Branch("trackIsoConeTrackCount", &treeinfo.trackIsoConeTrackCount);
   crystal_tree->Branch("trackIsoConePtSum", &treeinfo.trackIsoConePtSum);
   crystal_tree->Branch("zVertex", &treeinfo.zVertex);
   crystal_tree->Branch("zVertexEnergy", &treeinfo.zVertexEnergy);
}


L1EGRateStudiesRecHits::~L1EGRateStudiesRecHits()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1EGRateStudiesRecHits::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   eventCount++;

   // electron candidates
   std::map<std::string, l1extra::L1EmParticleCollection> eGammaCollections;
   //for(const auto& inputTag : L1EGammaInputTags)
   //{
   //   if (inputTag.encode().compare("l1extraParticles:All") == 0) continue;
   //   if (inputTag.encode().compare("l1extraParticlesUCT:All") == 0) continue;
   //   edm::Handle<l1extra::L1EmParticleCollection> handle;
   //   iEvent.getByLabel(inputTag, handle);
   //   if ( handle.product() == nullptr )
   //      std::cout << "There is no product of type " << inputTag.encode() << std::endl;
   //   else
   //      eGammaCollections[inputTag.encode()] = *handle.product();

   //   // Special case: Run 1, UCT alg. iso/niso are exclusive, we want to make inclusive EGamma available too
   //   if (inputTag.encode().find("l1extraParticlesUCT") != std::string::npos)
   //   {
   //      auto& collection = eGammaCollections["l1extraParticlesUCT:All"];
   //      collection.insert(begin(collection), begin(*handle.product()), end(*handle.product()));
   //   }
   //   else if (inputTag.encode().find("l1extraParticles") != std::string::npos)
   //   {
   //      auto& collection = eGammaCollections["l1extraParticles:All"];
   //      collection.insert(begin(collection), begin(*handle.product()), end(*handle.product()));
   //   }
   //}

   // electron candidate extra info from Sacha's algorithm
   //l1slhc::L1EGCrystalClusterCollection crystalClusters;
   //edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;      
   //iEvent.getByLabel(L1CrystalClustersInputTag,crystalClustersHandle);
   iEvent.getByToken(crystalClustersToken_,crystalClustersHandle);
   crystalClusters = (*crystalClustersHandle.product());

   // Generator info (truth)
   //edm::Handle<reco::GenParticleCollection> genParticleHandle;
   //reco::GenParticleCollection genParticles;
   iEvent.getByToken(genCollectionToken_,genParticleHandle);
   genParticles = *genParticleHandle.product();

   // Trigger tower info (trigger primitives)
   //edm::Handle<EcalTrigPrimDigiCollection> tpH;
   //iEvent.getByLabel(edm::InputTag("ecalDigis:EcalTriggerPrimitives"), tpH);
   //EcalTrigPrimDigiCollection triggerPrimitives = *tpH.product();

   // EcalRecHits for looking at flags in the cluster seed crystal
   edm::Handle<EcalRecHitCollection> pcalohits;
   //iEvent.getByLabel("ecalRecHit","EcalRecHitsEB",pcalohits);
   iEvent.getByToken(ecalRecHitEBToken_,pcalohits);
   EcalRecHitCollection ecalRecHits = *pcalohits.product();

   // Record the standards
   treeinfo.run = iEvent.eventAuxiliary().run();
   treeinfo.lumi = iEvent.eventAuxiliary().luminosityBlock();
   treeinfo.event = iEvent.eventAuxiliary().event();

   // Sort clusters so we can always pick highest pt cluster matching cuts
   std::sort(begin(crystalClusters), end(crystalClusters), [](const l1slhc::L1EGCrystalCluster& a, const l1slhc::L1EGCrystalCluster& b){return a.pt() > b.pt();});
   // also sort old algorithm products
   for(auto& collection : eGammaCollections)
      std::sort(begin(collection.second), end(collection.second), [](const l1extra::L1EmParticle& a, const l1extra::L1EmParticle& b){return a.pt() > b.pt();});
   
   int clusterCount = 0;
   if ( doEfficiencyCalc )
   {
      reco::Candidate::PolarLorentzVector trueElectron;
      float reco_electron_pt = 0.;
      float reco_electron_eta = -99.;
      float reco_electron_phi = -99.;
      
      // Get offline cluster info
      iEvent.getByToken(offlineRecoClusterToken_, offlineRecoClustersHandle);
      reco::SuperClusterCollection offlineRecoClusters = *offlineRecoClustersHandle.product();

      // Find the cluster corresponding to generated electron
      bool offlineRecoFound = false;
      for(auto& cluster : offlineRecoClusters)
      {
         reco::Candidate::PolarLorentzVector p4;
         p4.SetPt(cluster.energy()*sin(cluster.position().theta()));
         p4.SetEta(cluster.position().eta());
         p4.SetPhi(cluster.position().phi());
         p4.SetM(0.);
         if ( reco::deltaR(p4, genParticles[0].polarP4()) < 0.1
             && fabs(p4.pt() - genParticles[0].pt()) < genMatchRelPtcut*genParticles[0].pt() )
         {
            if ( useOfflineClusters )
               trueElectron = p4;
            reco_electron_pt = p4.pt();
            reco_electron_eta = p4.eta();
            reco_electron_phi = p4.phi();
            offlineRecoFound = true;
            if (debug) std::cout << "Gen.-matched pBarrelCorSuperCluster: pt " 
                     << cluster.energy()/std::cosh(cluster.position().eta()) 
                     << " eta " << cluster.position().eta() 
                     << " phi " << cluster.position().phi() << std::endl;
            if (debug) std::cout << "Cluster pt - Gen pt / Gen pt = " << (reco_electron_pt-genParticles[0].pt())/genParticles[0].pt() << std::endl;
            break;
         }
      }
      if ( useOfflineClusters && !offlineRecoFound )
      {
         // if we can't offline reconstruct the generated electron, 
         // it might as well have not existed.
         eventCount--;
         return;
      }

      if ( !useOfflineClusters )
      {
         // Get the particle position upon entering ECal
         RawParticle particle(genParticles[0].p4());
         particle.setVertex(genParticles[0].vertex().x(), genParticles[0].vertex().y(), genParticles[0].vertex().z(), 0.);
         //particle.setID(genParticles[0].pdgId());
         // Skip setID requires some external libraries working well that
         // define HepPDT::ParticleID
         // in the end, setID sets the mass and charge of our particle.
         // Try doing this by hand for the moment
         particle.setMass(.511);
         int pdgId = genParticles[0].pdgId();
         if (pdgId > 0) {
            particle.setCharge( -1.0 ); }
         if (pdgId < 0) {
            particle.setCharge( 1.0 ); }
         BaseParticlePropagator prop(particle, 0., 0., 4.);
         BaseParticlePropagator start(prop);
         prop.propagateToEcalEntrance();
         if(prop.getSuccess()!=0)
         {
            trueElectron = reco::Candidate::PolarLorentzVector(prop.E()*sin(prop.vertex().theta()), prop.vertex().eta(), prop.vertex().phi(), 0.);
            if ( debug ) std::cout << "Propogated genParticle to ECal, position: " << prop.vertex() << " momentum = " << prop.momentum() << std::endl;
            if ( debug ) std::cout << "                       starting position: " << start.vertex() << " momentum = " << start.momentum() << std::endl;
            if ( debug ) std::cout << "                    genParticle position: " << genParticles[0].vertex() << " momentum = " << genParticles[0].p4() << std::endl;
            if ( debug ) std::cout << "       old pt = " << genParticles[0].pt() << ", new pt = " << trueElectron.pt() << std::endl;
         }
         else
         {
            // something failed?
            trueElectron = genParticles[0].polarP4();
         }
      }

      // Only one electron is produced in singleElectron files
      // we look for that electron in the reconstructed data within some deltaR cut,
      // and some relative pt error cut
      // and if we find it, it goes in the numerator
      // but only if in the barrel!
      if ( !useEndcap && fabs(trueElectron.eta()) > 1.479 )
      {
         eventCount--;
         return;
      }
      efficiency_denominator_hist->Fill(trueElectron.pt());
      treeinfo.gen_pt = genParticles[0].pt();
      treeinfo.gen_z = genParticles[0].vz();
      treeinfo.gen_eta = genParticles[0].eta();
      treeinfo.gen_phi = genParticles[0].phi();
      treeinfo.gen_energy = genParticles[0].energy();
      treeinfo.gen_charge = genParticles[0].charge();
      treeinfo.E_gen = genParticles[0].pt()*cosh(genParticles[0].eta());
      treeinfo.denom_pt = trueElectron.pt();
      if ( fabs(trueElectron.eta()) > 1.479 )
         treeinfo.endcap = true;
      else
         treeinfo.endcap = false;
      efficiency_denominator_eta_hist->Fill(trueElectron.eta());
      if ( offlineRecoFound ) {
         treeinfo.reco_pt = reco_electron_pt;
         treeinfo.reco_eta = reco_electron_eta;
         treeinfo.reco_phi = reco_electron_phi;
         efficiency_denominator_reco_hist->Fill(reco_electron_pt);
      }
      else
      {
         treeinfo.reco_pt = 0.;
      }
      if ( crystalClusters.size() > 0 )
      {
         auto bestCluster = *std::min_element(begin(crystalClusters), end(crystalClusters), [trueElectron](const l1slhc::L1EGCrystalCluster& a, const l1slhc::L1EGCrystalCluster& b){return reco::deltaR(a, trueElectron) < reco::deltaR(b, trueElectron);});
         bool clusterFound = false;
         bool bestClusterUsed = false;
         for(const auto& cluster : crystalClusters)
         {
            clusterCount++;
            if ( reco::deltaR(cluster, trueElectron) < genMatchDeltaRcut
                 && fabs(cluster.pt()-trueElectron.pt())/trueElectron.pt() < genMatchRelPtcut )
            {
               clusterFound = true;
               if ( cluster.eta() != bestCluster.eta() || cluster.phi() != bestCluster.phi() ) // why don't I have a comparison op
                  continue;
               bestClusterUsed = true;
               if ( debug ) std::cout << "using cluster dr = " << reco::deltaR(cluster, trueElectron) << std::endl;
               treeinfo.nthCandidate = clusterCount;
               treeinfo.deltaR = reco::deltaR(cluster, trueElectron);
               treeinfo.deltaPhi = reco::deltaPhi(cluster, trueElectron);
               treeinfo.deltaEta = trueElectron.eta()-cluster.eta();
               
               fill_tree(cluster);
               //checkRecHitsFlags(cluster, triggerPrimitives, ecalRecHits);

               if ( cluster_passes_cuts(cluster) )
               {
                  dyncrystal_efficiency_hist->Fill(trueElectron.pt());
                  dyncrystal_efficiency_eta_hist->Fill(trueElectron.eta());
                  if ( offlineRecoFound )
                  {
                     for(auto& pair : dyncrystal_efficiency_reco_hists)
                     {
                        // (threshold, histogram)
                        if (cluster.pt() > pair.first)
                           pair.second->Fill(reco_electron_pt);
                     }
                  }
                  for(auto& pair : dyncrystal_efficiency_gen_hists)
                  {
                     // (threshold, histogram)
                     if (cluster.pt() > pair.first)
                        pair.second->Fill(trueElectron.pt());
                  }
                  dyncrystal_deltaR_hist->Fill(reco::deltaR(cluster, trueElectron));
                  dyncrystal_deta_hist->Fill(trueElectron.eta()-cluster.eta());
                  dyncrystal_dphi_hist->Fill(reco::deltaPhi(cluster.phi(), trueElectron.phi()));
                  if ( cluster.bremStrength() < 0.2 )
                  {
                     dyncrystal_efficiency_bremcut_hist->Fill(trueElectron.pt());
                     dyncrystal_deltaR_bremcut_hist->Fill(reco::deltaR(cluster, trueElectron));
                     dyncrystal_dphi_bremcut_hist->Fill(reco::deltaPhi(cluster.phi(), trueElectron.phi()));
                  }
                  dyncrystal_2DdeltaR_hist->Fill(trueElectron.eta()-cluster.eta(), reco::deltaPhi(cluster, trueElectron));

                  reco_gen_pt_hist->Fill( trueElectron.pt(), (cluster.pt() - trueElectron.pt())/trueElectron.pt() );
                  reco_gen_pt_1dHist->Fill( (cluster.pt() - trueElectron.pt())/trueElectron.pt() );
                  brem_dphi_hist->Fill( cluster.bremStrength(), reco::deltaPhi(cluster, trueElectron) );
                  break;
               }
            }
         }
         if ( clusterFound && !bestClusterUsed )
         {
            std::cerr << "Found a cluster but it wasn't the best so I lost efficiency!" << std::endl;
         }
      }
      
      for(const auto& eGammaCollection : eGammaCollections)
      {
         const std::string &name = eGammaCollection.first;
         for(const auto& EGCandidate : eGammaCollection.second)
         {
            if ( reco::deltaR(EGCandidate.polarP4(), trueElectron) < genMatchDeltaRcut &&
                 fabs(EGCandidate.pt()-trueElectron.pt())/trueElectron.pt() < genMatchRelPtcut )
            {
               if ( debug ) std::cout << "Filling hists for EG Collection: " << name << std::endl;
               EGalg_efficiency_hists[name]->Fill(trueElectron.pt());
               EGalg_efficiency_eta_hists[name]->Fill(trueElectron.eta());
               if ( offlineRecoFound )
               {
                  for(auto& pair : EGalg_efficiency_reco_hists[name])
                  {
                     // (threshold, histogram)
                     if (EGCandidate.pt() > pair.first)
                        pair.second->Fill(reco_electron_pt);
                  }
               }
               for(auto& pair : EGalg_efficiency_gen_hists[name])
               {
                  // (threshold, histogram)
                  if (EGCandidate.pt() > pair.first)
                     pair.second->Fill(trueElectron.pt());
               }
               EGalg_deltaR_hists[name]->Fill(reco::deltaR(EGCandidate.polarP4(), trueElectron));
               EGalg_deta_hists[name]->Fill(trueElectron.eta()-EGCandidate.eta());
               EGalg_dphi_hists[name]->Fill(reco::deltaPhi(EGCandidate.phi(), trueElectron.phi()));
               EGalg_reco_gen_pt_hists[name]->Fill( trueElectron.pt(), (EGCandidate.pt() - trueElectron.pt())/trueElectron.pt() );
               EGalg_reco_gen_pt_1dHists[name]->Fill( (EGCandidate.pt() - trueElectron.pt())/trueElectron.pt() );
               EGalg_2DdeltaR_hists[name]->Fill(trueElectron.eta()-EGCandidate.eta(), reco::deltaPhi(EGCandidate, trueElectron));
               break;
            }
         }
      }
   }
   else // !doEfficiencyCalc
   {
      for(const auto& cluster : crystalClusters)
      {
         if ( !useEndcap && fabs(cluster.eta()) >= 1.479 ) continue;
         clusterCount++;
         treeinfo.nthCandidate = clusterCount;
         if ( fabs(cluster.eta()) > 1.479 )
            treeinfo.endcap = true;
         else
            treeinfo.endcap = false;
         fill_tree(cluster);
         //checkRecHitsFlags(cluster, triggerPrimitives, ecalRecHits);

         if ( cluster_passes_cuts(cluster) )
         {
            dyncrystal_rate_hist->Fill(cluster.pt());
            break;
         }
      }

      for(const auto& eGammaCollection : eGammaCollections)
      {
         const std::string &name = eGammaCollection.first;
         if ( eGammaCollection.second.size() == 0 ) continue;
         if ( useEndcap )
         {
            auto& highestEGCandidate = eGammaCollection.second[0];
            EGalg_rate_hists[name]->Fill(highestEGCandidate.pt());
         }
         else // !useEndcap
         {
            // Can't assume the highest candidate is in the barrel
            for(const auto& candidate : eGammaCollection.second)
            {
               if ( fabs(candidate.eta()) < 1.479 )
               {
                  EGalg_rate_hists[name]->Fill(candidate.pt());
                  break;
               }
            }
         }
      }
   }
}


// ------------ method called once each job just before starting event loop  ------------
void 
L1EGRateStudiesRecHits::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1EGRateStudiesRecHits::endJob() 
{
   // Rate or efficiency study?
   if ( !doEfficiencyCalc )
   {
      // We currently have a rate pdf, we want cdf, so we integrate (downward in pt is inclusive)
      // We normalize to 30MHz as this will be the crossing rate of filled bunches in SLHC
      // (in parallel processing mode, fill dummy hist with event counts so they can be added later)
      edm::Service<TFileService> fs;
      TH1F* event_count = fs->make<TH1F>("eventCount", "Event Count", 1, -1, 1);
      event_count->SetBinContent(1, eventCount);
      integrateDown(dyncrystal_rate_hist);
      for(auto& hist : EGalg_rate_hists)
      {
         integrateDown(hist.second);
      }
   }
}

// ------------ method called when starting to processes a run  ------------
void 
L1EGRateStudiesRecHits::beginRun(edm::Run const& run, edm::EventSetup const& es)
{
   //edm::ESHandle<HepPDT::ParticleDataTable> pdt;
   //es.getData(pdt);
   //if ( !ParticleTable::instance() ) ParticleTable::instance(&(*pdt));
}

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1EGRateStudiesRecHits::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1EGRateStudiesRecHits::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1EGRateStudiesRecHits::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1EGRateStudiesRecHits::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ user methods (ncsmith)
void 
L1EGRateStudiesRecHits::integrateDown(TH1F * hist) {
   // integral includes overflow and underflow bins
   double integral=0.;
   for(int i=hist->GetNbinsX()+1; i>=0; i--)
   {
      integral += hist->GetBinContent(i);
      hist->SetBinContent(i, integral);
   }
}

void
L1EGRateStudiesRecHits::fill_tree(const l1slhc::L1EGCrystalCluster& cluster) {
   for(Size_t i=0; i<treeinfo.crystal_pt.size(); ++i)
   {
      treeinfo.crystal_pt[i] = cluster.GetCrystalPt(i);
   }
   treeinfo.cluster_pt = cluster.pt();
   treeinfo.crystalCount = cluster.GetExperimentalParam("crystalCount");
   treeinfo.cluster_energy = cluster.energy();
   treeinfo.eta = cluster.eta();
   treeinfo.phi = cluster.phi();
   treeinfo.hovere = cluster.hovere();
   treeinfo.iso = cluster.isolation();
   treeinfo.bremStrength = cluster.bremStrength();
   treeinfo.e2x5 = cluster.GetExperimentalParam("E2x5");
   treeinfo.e3x5 = cluster.GetExperimentalParam("E3x5");
   treeinfo.e5x5 = cluster.GetExperimentalParam("E5x5");
   treeinfo.passed = cluster_passes_cuts(cluster);
   treeinfo.uslPt = cluster.GetExperimentalParam("upperSideLobePt");
   treeinfo.lslPt = cluster.GetExperimentalParam("lowerSideLobePt");
   treeinfo.corePt = cluster.GetExperimentalParam("uncorrectedPt");
   treeinfo.E_core = cluster.GetExperimentalParam("uncorrectedE");
   treeinfo.phiStripContiguous0 = cluster.GetExperimentalParam("phiStripContiguous0");
   treeinfo.phiStripOneHole0 = cluster.GetExperimentalParam("phiStripOneHole0");
   treeinfo.phiStripContiguous3p = cluster.GetExperimentalParam("phiStripContiguous3p");
   treeinfo.phiStripOneHole3p = cluster.GetExperimentalParam("phiStripOneHole3p");
   // Gen and reco pt get filled earlier
   crystal_tree->Fill();
}

bool
L1EGRateStudiesRecHits::cluster_passes_cuts(const l1slhc::L1EGCrystalCluster& cluster) const {
   // return true;
   
   // Currently this producer is optimized based on cluster isolation and shower shape
   // the previous H/E cut has been removed for the moment.
   // The following cut is based off of what was shown in the Phase-2 meeting
   // 23 June 2016.  Only the barrel is considered.  And track isolation
   // is not included.
   if ( fabs(cluster.eta()) < 1.479 )
   {
      //std::cout << "Starting passing check" << std::endl;
      float cluster_pt = cluster.pt();
      float clusterE2x5 = cluster.GetExperimentalParam("E2x5");
      float clusterE5x5 = cluster.GetExperimentalParam("E5x5");
      float cluster_iso = cluster.isolation();
      bool passIso = false;
      bool passShowerShape = false;
      
      if ( ( -0.92 + 0.18 * TMath::Exp( -0.04 * cluster_pt ) < (clusterE2x5 / clusterE5x5)) ) {
      passShowerShape = true; }
      if ( (( 0.99 + 5.6 * TMath::Exp( -0.061 * cluster_pt )) > cluster_iso ) ) {
          passIso = true; }
      if ( passShowerShape && passIso ) {
          //std::cout << " --- Passed!" << std::endl;
      return true; }
   }
   return false;
}

bool
L1EGRateStudiesRecHits::checkTowerExists(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps) const {
   for (const auto& tp : tps)
   {
      if ( tp.id() == ((EBDetId) cluster.seedCrystal()).tower() )
      {
         if ( tp.compressedEt() > 0 )
         {
            return true;
         }
         break;
      }
   }
   return false;
}

//void
//L1EGRateStudiesRecHits::checkRecHitsFlags(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps, const EcalRecHitCollection &ecalRecHits) const {
//   if ( cluster_passes_cuts(cluster) )
//   {
//      if ( debug ) std::cout << "Event (pt = " << cluster.pt() << ") passed cuts, ";
//      if ( debug && checkTowerExists(cluster, tps) )
//         std::cout << "\x1B[32mtower exists!\x1B[0m" << std::endl;
//      else if ( debug )
//         std::cout << "\x1B[31mtower does not exist!\x1B[0m" << std::endl;
//      if ( debug ) std::cout << "Here are the cluster seed crystal reco flags:" << std::endl;
//      for(auto hit : ecalRecHits)
//      {
//         if( hit.id() == cluster.seedCrystal() )
//         {
//            const std::map<int, std::string> flagDefs {
//               { EcalRecHit::kGood, "channel ok, the energy and time measurement are reliable" },
//               { EcalRecHit::kPoorReco, "the energy is available from the UncalibRecHit, but approximate (bad shape, large chi2)" },
//               { EcalRecHit::kOutOfTime, "the energy is available from the UncalibRecHit (sync reco), but the event is out of time" },
//               { EcalRecHit::kFaultyHardware, "The energy is available from the UncalibRecHit, channel is faulty at some hardware level (e.g. noisy)" },
//               { EcalRecHit::kNoisy, "the channel is very noisy" },
//               { EcalRecHit::kPoorCalib, "the energy is available from the UncalibRecHit, but the calibration of the channel is poor" },
//               { EcalRecHit::kSaturated, "saturated channel (recovery not tried)" },
//               { EcalRecHit::kLeadingEdgeRecovered, "saturated channel: energy estimated from the leading edge before saturation" },
//               { EcalRecHit::kNeighboursRecovered, "saturated/isolated dead: energy estimated from neighbours" },
//               { EcalRecHit::kTowerRecovered, "channel in TT with no data link, info retrieved from Trigger Primitive" },
//               { EcalRecHit::kDead, "channel is dead and any recovery fails" },
//               { EcalRecHit::kKilled, "MC only flag: the channel is{ EcalRecHit::killed in the real detector" },
//               { EcalRecHit::kTPSaturated, "the channel is in a region with saturated TP" },
//               { EcalRecHit::kL1SpikeFlag, "the channel is in a region with TP with sFGVB = 0" },
//               { EcalRecHit::kWeird, "the signal is believed to originate from an anomalous deposit (spike) " },
//               { EcalRecHit::kDiWeird, "the signal is anomalous, and neighbors another anomalous signal  " },
//               { EcalRecHit::kHasSwitchToGain6, "at least one data frame is in G6" },
//               { EcalRecHit::kHasSwitchToGain1, "at least one data frame is in G1" }
//            };
//            for(auto& flag : flagDefs)
//            {
//               if ( hit.checkFlag(flag.first) )
//               {
//                  if ( flag.first == EcalRecHit::kGood && debug ) std::cout << "\x1B[32m";
//                  if ( debug ) std::cout << "    " << flag.second << std::endl;
//                  if ( flag.first == EcalRecHit::kGood && debug ) std::cout << "\x1B[0m";
//
//                  if ( checkTowerExists(cluster, tps) )
//                     RecHitFlagsTowerHist->Fill(flag.first);
//                  else
//                     RecHitFlagsNoTowerHist->Fill(flag.first);
//               }
//            }
//         }
//      }
//   }
//}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGRateStudiesRecHits);

