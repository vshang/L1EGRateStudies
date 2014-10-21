// -*- C++ -*-
//
// Package:    L1EGRateStudies
// Class:      L1EGRateStudies
// 
/**\class L1EGRateStudies L1EGRateStudies.cc SLHCUpgradeSimulations/L1EGRateStudies/src/L1EGRateStudies.cc

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

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/SLHC/interface/L1EGCrystalCluster.h"

#include "DataFormats/EgammaReco/interface/SuperCluster.h"
#include "DataFormats/EgammaReco/interface/SuperClusterFwd.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"

#include "FastSimulation/BaseParticlePropagator/interface/BaseParticlePropagator.h"
#include "FastSimulation/Particle/interface/ParticleTable.h"

#include "SimDataFormats/SLHC/interface/StackedTrackerTypes.h"
#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
#include "SLHCUpgradeSimulations/L1TrackTrigger/interface/L1TkElectronTrackMatchAlgo.h"

#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
//
// class declaration
//
class L1EGRateStudies : public edm::EDAnalyzer {
   typedef std::vector<TTTrack<Ref_PixelDigi_>> L1TkTrackCollectionType;

   public:
      explicit L1EGRateStudies(const edm::ParameterSet&);
      ~L1EGRateStudies();

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
      void checkRecHitsFlags(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps, const EcalRecHitCollection &ecalRecHits) const;
      
      // ----------member data ---------------------------
      bool doEfficiencyCalc;
      bool useOfflineClusters;
      bool debug;
      bool useEndcap;
      
      double genMatchDeltaRcut;
      double genMatchRelPtcut;
      
      int eventCount;
      std::vector<edm::InputTag> L1EGammaInputTags;
      edm::InputTag L1CrystalClustersInputTag;
      edm::InputTag offlineRecoClusterInputTag;
      edm::InputTag L1TrackInputTag;
            
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

      // EcalRecHits flags
      TH1I * RecHitFlagsTowerHist;
      TH1I * RecHitFlagsNoTowerHist;

      // Crystal pt stuff
      TTree * crystal_tree;
      struct {
         std::array<float, 6> crystal_pt;
         float cluster_pt;
         float cluster_energy;
         float hovere;
         float iso;
         float deltaR = 0.;
         float gen_pt = 0.;
         float denom_pt = 0.;
         float reco_pt = 0.;
         bool  passed = false;
         int   nthCandidate = -1;
         bool  endcap = false;
         float uslE = 0.;
         float lslE = 0.;
         float raw_pt = 0.;
         float trackDeltaR;
         float trackP;
         float trackRInv;         
         float trackChi2;
      } treeinfo;

      // (pt_reco-pt_gen)/pt_gen plot
      TH2F * reco_gen_pt_hist;

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
L1EGRateStudies::L1EGRateStudies(const edm::ParameterSet& iConfig) :
   doEfficiencyCalc(iConfig.getUntrackedParameter<bool>("doEfficiencyCalc", false)),
   useOfflineClusters(iConfig.getUntrackedParameter<bool>("useOfflineClusters", false)),
   debug(iConfig.getUntrackedParameter<bool>("debug", false)),
   useEndcap(iConfig.getUntrackedParameter<bool>("useEndcap", false)),
   genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.1)),
   genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
   nHistBins(iConfig.getUntrackedParameter<int>("histogramBinCount", 10)),
   nHistEtaBins(iConfig.getUntrackedParameter<int>("histogramEtaBinCount", 20)),
   histLow(iConfig.getUntrackedParameter<double>("histogramRangeLow", 0.)),
   histHigh(iConfig.getUntrackedParameter<double>("histogramRangeHigh", 50.)),
   histetaLow(iConfig.getUntrackedParameter<double>("histogramRangeetaLow", -2.5)),
   histetaHigh(iConfig.getUntrackedParameter<double>("histogramRangeetaHigh", 2.5))
{
   eventCount = 0;
   L1EGammaInputTags = iConfig.getParameter<std::vector<edm::InputTag>>("L1EGammaInputTags");
   L1EGammaInputTags.push_back(edm::InputTag("l1extraParticles:All"));
   L1EGammaInputTags.push_back(edm::InputTag("l1extraParticlesUCT:All"));
   L1CrystalClustersInputTag = iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag");
   L1TrackInputTag = iConfig.getParameter<edm::InputTag>("L1TrackInputTag");
   
   edm::Service<TFileService> fs;
   
   // If using offline-reco clusters, label dR & related hists appropriately
   std::string drLabel("(Gen-Reco);Counts");
   if ( useOfflineClusters ) drLabel = "(vs. Offline Reco.);Counts";

   // Make a set of histograms to fill, depending on if we are doing rate or efficiency
   if ( doEfficiencyCalc )
   {
      auto thresholds = iConfig.getUntrackedParameter<std::vector<int>>("turnOnThresholds");
      offlineRecoClusterInputTag = iConfig.getParameter<edm::InputTag>("OfflineRecoClustersInputTag");

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
      dyncrystal_deta_hist = fs->make<TH1F>("dyncrystalEG_deta", ("Dynamic Crystal Trigger;d#eta "+drLabel).c_str(), 50, -0.1, 0.1);
      dyncrystal_dphi_hist = fs->make<TH1F>("dyncrystalEG_dphi", ("Dynamic Crystal Trigger;d#phi "+drLabel).c_str(), 50, -0.1, 0.1);
      dyncrystal_dphi_bremcut_hist = fs->make<TH1F>("dyncrystalEG_dphi_bremcut", ("Dynamic Crystal Trigger;d#phi "+drLabel).c_str(), 50, -0.1, 0.1);
      dyncrystal_2DdeltaR_hist = fs->make<TH2F>("dyncrystalEG_2DdeltaR_hist", "Dynamic Crystal Trigger;d#eta;d#phi;Counts", 50, -0.05, 0.05, 50, -0.05, 0.05);

      for(auto& inputTag : L1EGammaInputTags)
      {
         const std::string &name = inputTag.encode();
         EGalg_efficiency_hists[name] = fs->make<TH1F>((name+"_efficiency_pt").c_str(), (name+";Gen. pT (GeV);Efficiency").c_str(), nHistBins, histLow, histHigh);
         EGalg_efficiency_eta_hists[name] = fs->make<TH1F>((name+"_efficiency_eta").c_str(), (name+";Gen. #eta;Efficiency").c_str(), nHistEtaBins, histetaLow, histetaHigh);
         // Implicit conversion from int to double
         for(int threshold : thresholds)
         {
            EGalg_efficiency_reco_hists[name][threshold] = fs->make<TH1F>((name+"_threshold"+std::to_string(threshold)+"_efficiency_reco_pt").c_str(), (name+";Offline reco. pT (GeV);Efficiency").c_str(), nHistBins, histLow, histHigh);
            EGalg_efficiency_gen_hists[name][threshold] = fs->make<TH1F>((name+"_threshold"+std::to_string(threshold)+"_efficiency_gen_pt").c_str(), (name+";Gen. pT (GeV);Efficiency").c_str(), nHistBins, histLow, histHigh);
         }
         EGalg_deltaR_hists[name] = fs->make<TH1F>((name+"_deltaR").c_str(), (name+";#Delta R "+drLabel).c_str(), 50, 0., genMatchDeltaRcut);
         EGalg_deta_hists[name] = fs->make<TH1F>((name+"_deta").c_str(), (name+";d#eta "+drLabel).c_str(), 50, -0.1, 0.1);
         EGalg_dphi_hists[name] = fs->make<TH1F>((name+"_dphi").c_str(), (name+";d#phi "+drLabel).c_str(), 50, -0.1, 0.1);
         EGalg_2DdeltaR_hists[name] = fs->make<TH2F>((name+"_2DdeltaR").c_str(), ";d#eta;d#phi;Counts", 50, -0.05, 0.05, 50, -0.05, 0.05);
         EGalg_reco_gen_pt_hists[name] = fs->make<TH2F>((name+"_reco_gen_pt").c_str(), (name+";Gen. pT (GeV);(reco-gen)/gen;Counts").c_str(), 40, 0., 50., 40, -0.3, 0.3); 
      }

      reco_gen_pt_hist = fs->make<TH2F>("reco_gen_pt" , "EG relative momentum error;Gen. pT (GeV);(reco-gen)/gen;Counts", 40, 0., 50., 40, -0.3, 0.3); 
      brem_dphi_hist = fs->make<TH2F>("brem_dphi_hist" , "Brem. strength vs. d#phi;Brem. Strength;d#phi;Counts", 40, 0., 2., 40, -0.05, 0.05); 

      efficiency_denominator_hist = fs->make<TH1F>("gen_pt", "Gen. pt;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_reco_hist = fs->make<TH1F>("reco_pt", "Offline reco. pt;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_eta_hist = fs->make<TH1F>("gen_eta", "Gen. #eta;Gen. #eta; Counts", nHistEtaBins, histetaLow, histetaHigh);
   }
   else
   {
      dyncrystal_rate_hist = fs->make<TH1F>("dyncrystalEG_rate" , "Dynamic Crystal Trigger;ET Threshold (GeV);Rate (kHz)", nHistBins, histLow, histHigh);
      for(auto& inputTag : L1EGammaInputTags)
      {
         const std::string &name = inputTag.encode();
         EGalg_rate_hists[name] = fs->make<TH1F>((name+"_rate").c_str() , (name+";ET Threshold (GeV);Rate (kHz)").c_str(), nHistBins, histLow, histHigh);
      }
   }
   RecHitFlagsTowerHist = fs->make<TH1I>("recHitFlags_tower", "EcalRecHit status flags when tower exists;Flag;Counts", 20, 0, 19);
   RecHitFlagsNoTowerHist = fs->make<TH1I>("recHitFlags_notower", "EcalRecHit status flags when tower exists;Flag;Counts", 20, 0, 19);

   crystal_tree = fs->make<TTree>("crystal_tree", "Crystal cluster individual crystal pt values");
   crystal_tree->Branch("pt", &treeinfo.crystal_pt, "1:2:3:4:5:6");
   crystal_tree->Branch("cluster_pt", &treeinfo.cluster_pt);
   crystal_tree->Branch("cluster_energy", &treeinfo.cluster_energy);
   crystal_tree->Branch("cluster_hovere", &treeinfo.hovere);
   crystal_tree->Branch("cluster_iso", &treeinfo.iso);
   crystal_tree->Branch("deltaR", &treeinfo.deltaR);
   crystal_tree->Branch("gen_pt", &treeinfo.gen_pt);
   crystal_tree->Branch("denom_pt", &treeinfo.denom_pt);
   crystal_tree->Branch("reco_pt", &treeinfo.reco_pt);
   crystal_tree->Branch("passed", &treeinfo.passed);
   crystal_tree->Branch("nthCandidate", &treeinfo.nthCandidate);
   crystal_tree->Branch("endcap", &treeinfo.endcap);
   crystal_tree->Branch("uslE", &treeinfo.uslE);
   crystal_tree->Branch("lslE", &treeinfo.lslE);
   crystal_tree->Branch("raw_pt", &treeinfo.raw_pt);
   crystal_tree->Branch("trackDeltaR", &treeinfo.trackDeltaR);
   crystal_tree->Branch("trackP", &treeinfo.trackP);
   crystal_tree->Branch("trackRInv", &treeinfo.trackRInv);
   crystal_tree->Branch("trackChi2", &treeinfo.trackChi2);
}


L1EGRateStudies::~L1EGRateStudies()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1EGRateStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   eventCount++;

   // electron candidates
   std::map<std::string, l1extra::L1EmParticleCollection> eGammaCollections;
   for(const auto& inputTag : L1EGammaInputTags)
   {
      if (inputTag.encode().compare("l1extraParticles:All") == 0) continue;
      if (inputTag.encode().compare("l1extraParticlesUCT:All") == 0) continue;
      edm::Handle<l1extra::L1EmParticleCollection> handle;
      iEvent.getByLabel(inputTag, handle);
      if ( handle.product() == nullptr )
         std::cout << "There is no product of type " << inputTag.encode() << std::endl;
      else
         eGammaCollections[inputTag.encode()] = *handle.product();

      // Special case: Run 1, UCT alg. iso/niso are exclusive, we want to make inclusive EGamma available too
      if (inputTag.encode().find("l1extraParticlesUCT") != std::string::npos)
      {
         auto& collection = eGammaCollections["l1extraParticlesUCT:All"];
         collection.insert(begin(collection), begin(*handle.product()), end(*handle.product()));
      }
      else if (inputTag.encode().find("l1extraParticles") != std::string::npos)
      {
         auto& collection = eGammaCollections["l1extraParticles:All"];
         collection.insert(begin(collection), begin(*handle.product()), end(*handle.product()));
      }
   }

   // electron candidate extra info from Sacha's algorithm
   l1slhc::L1EGCrystalClusterCollection crystalClusters;
   edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;      
   iEvent.getByLabel(L1CrystalClustersInputTag,crystalClustersHandle);
   crystalClusters = (*crystalClustersHandle.product());

   // Generator info (truth)
   edm::Handle<reco::GenParticleCollection> genParticleHandle;
   reco::GenParticleCollection genParticles;
   iEvent.getByLabel("genParticles", genParticleHandle);
   genParticles = *genParticleHandle.product();

   // Trigger tower info (trigger primitives)
   edm::Handle<EcalTrigPrimDigiCollection> tpH;
   iEvent.getByLabel(edm::InputTag("ecalDigis:EcalTriggerPrimitives"), tpH);
   EcalTrigPrimDigiCollection triggerPrimitives = *tpH.product();

   // EcalRecHits for looking at flags in the cluster seed crystal
   edm::Handle<EcalRecHitCollection> pcalohits;
   iEvent.getByLabel("ecalRecHit","EcalRecHitsEB",pcalohits);
   EcalRecHitCollection ecalRecHits = *pcalohits.product();

   // L1 Tracks
   edm::Handle<L1TkTrackCollectionType> l1trackHandle;
   iEvent.getByLabel(L1TrackInputTag, l1trackHandle);

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
      
      // Get offline cluster info
      edm::Handle<reco::SuperClusterCollection> offlineRecoClustersHandle;
      iEvent.getByLabel(offlineRecoClusterInputTag, offlineRecoClustersHandle);
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
         particle.setID(genParticles[0].pdgId());
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
      treeinfo.denom_pt = trueElectron.pt();
      if ( fabs(trueElectron.eta()) > 1.479 )
         treeinfo.endcap = true;
      else
         treeinfo.endcap = false;
      efficiency_denominator_eta_hist->Fill(trueElectron.eta());
      if ( offlineRecoFound ) {
         treeinfo.reco_pt = reco_electron_pt;
         efficiency_denominator_reco_hist->Fill(reco_electron_pt);
      }
      else
      {
         treeinfo.reco_pt = 0.;
      }
      for(const auto& cluster : crystalClusters)
      {
         clusterCount++;
         if ( reco::deltaR(cluster, trueElectron) < genMatchDeltaRcut
              && fabs(cluster.pt()-trueElectron.pt())/trueElectron.pt() < genMatchRelPtcut )
         {
            treeinfo.nthCandidate = clusterCount;
            treeinfo.deltaR = reco::deltaR(cluster, trueElectron);
            // track matching stuff
            double min_track_dr = 999.;
            edm::Ptr<TTTrack<Ref_PixelDigi_>> matched_track;
            for(size_t track_index=0; track_index<l1trackHandle->size(); ++track_index)
            {
               edm::Ptr<TTTrack<Ref_PixelDigi_>> ptr(l1trackHandle, track_index);
               double dr = L1TkElectronTrackMatchAlgo::deltaR(L1TkElectronTrackMatchAlgo::calorimeterPosition(cluster.phi(), cluster.eta(), cluster.energy()), ptr);
               if ( dr < min_track_dr )
               {
                  min_track_dr = dr;
                  matched_track = ptr;
               }
            }
            treeinfo.trackDeltaR = min_track_dr;
            treeinfo.trackP = matched_track->getMomentum().mag();
            treeinfo.trackRInv = matched_track->getRInv();
            treeinfo.trackChi2 = matched_track->getChi2();
            std::cout << "Track dr: " << min_track_dr << ", chi2: " << matched_track->getChi2() << ", dp: " << (treeinfo.trackP-cluster.energy())/cluster.energy() << std::endl;
            fill_tree(cluster);
            checkRecHitsFlags(cluster, triggerPrimitives, ecalRecHits);

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
               brem_dphi_hist->Fill( cluster.bremStrength(), reco::deltaPhi(cluster, trueElectron) );
               break;
            }
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
         checkRecHitsFlags(cluster, triggerPrimitives, ecalRecHits);

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
L1EGRateStudies::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1EGRateStudies::endJob() 
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
L1EGRateStudies::beginRun(edm::Run const& run, edm::EventSetup const& es)
{
   edm::ESHandle<HepPDT::ParticleDataTable> pdt;
   es.getData(pdt);
   if ( !ParticleTable::instance() ) ParticleTable::instance(&(*pdt));
}

// ------------ method called when ending the processing of a run  ------------
/*
void 
L1EGRateStudies::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
L1EGRateStudies::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
L1EGRateStudies::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
L1EGRateStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ user methods (ncsmith)
void 
L1EGRateStudies::integrateDown(TH1F * hist) {
   // integral includes overflow and underflow bins
   double integral=0.;
   for(int i=hist->GetNbinsX()+1; i>=0; i--)
   {
      integral += hist->GetBinContent(i);
      hist->SetBinContent(i, integral);
   }
}

void
L1EGRateStudies::fill_tree(const l1slhc::L1EGCrystalCluster& cluster) {
   for(Size_t i=0; i<treeinfo.crystal_pt.size(); ++i)
   {
      treeinfo.crystal_pt[i] = cluster.GetCrystalPt(i);
   }
   treeinfo.cluster_pt = cluster.pt();
   treeinfo.cluster_energy = cluster.energy();
   treeinfo.hovere = cluster.hovere();
   treeinfo.iso = cluster.isolation();
   treeinfo.passed = cluster_passes_cuts(cluster);
   treeinfo.uslE = cluster.GetExperimentalParam("upperSideLobeEnergy");
   treeinfo.lslE = cluster.GetExperimentalParam("lowerSideLobeEnergy");
   treeinfo.raw_pt = cluster.GetExperimentalParam("uncorrectedPt");
   // Gen and reco pt get filled earlier
   crystal_tree->Fill();
}

bool
L1EGRateStudies::cluster_passes_cuts(const l1slhc::L1EGCrystalCluster& cluster) const {
   float cut_pt = cluster.GetExperimentalParam("uncorrectedPt");
   if ( fabs(cluster.eta()) > 1.479 )
   {
      if ( cluster.hovere() < 22./cut_pt
           && cluster.isolation() < 64./cut_pt+0.1
           && cluster.GetCrystalPt(4)/(cluster.GetCrystalPt(0)+cluster.GetCrystalPt(1)) < ( (cut_pt < 40) ? 0.18*(1-cut_pt/70.):0.18*3/7. ) )
      {
         return true;
      }
   }
   else
   {
      if ( cluster.hovere() < 14./cut_pt+0.05
           && cluster.isolation() < 40./cut_pt+0.1
           && cluster.GetCrystalPt(4)/(cluster.GetCrystalPt(0)+cluster.GetCrystalPt(1)) < ( (cut_pt < 30) ? 0.18*(1-cut_pt/100.):0.18*0.7 ) )
      {
         return true;
      }
   }
   return false;
}

bool
L1EGRateStudies::checkTowerExists(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps) const {
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

void
L1EGRateStudies::checkRecHitsFlags(const l1slhc::L1EGCrystalCluster &cluster, const EcalTrigPrimDigiCollection &tps, const EcalRecHitCollection &ecalRecHits) const {
   if ( cluster_passes_cuts(cluster) )
   {
      if ( debug ) std::cout << "Event (pt = " << cluster.pt() << ") passed cuts, ";
      if ( debug && checkTowerExists(cluster, tps) )
         std::cout << "\x1B[32mtower exists!\x1B[0m" << std::endl;
      else if ( debug )
         std::cout << "\x1B[31mtower does not exist!\x1B[0m" << std::endl;
      if ( debug ) std::cout << "Here are the cluster seed crystal reco flags:" << std::endl;
      for(auto hit : ecalRecHits)
      {
         if( hit.id() == cluster.seedCrystal() )
         {
            const std::map<int, std::string> flagDefs {
               { EcalRecHit::kGood, "channel ok, the energy and time measurement are reliable" },
               { EcalRecHit::kPoorReco, "the energy is available from the UncalibRecHit, but approximate (bad shape, large chi2)" },
               { EcalRecHit::kOutOfTime, "the energy is available from the UncalibRecHit (sync reco), but the event is out of time" },
               { EcalRecHit::kFaultyHardware, "The energy is available from the UncalibRecHit, channel is faulty at some hardware level (e.g. noisy)" },
               { EcalRecHit::kNoisy, "the channel is very noisy" },
               { EcalRecHit::kPoorCalib, "the energy is available from the UncalibRecHit, but the calibration of the channel is poor" },
               { EcalRecHit::kSaturated, "saturated channel (recovery not tried)" },
               { EcalRecHit::kLeadingEdgeRecovered, "saturated channel: energy estimated from the leading edge before saturation" },
               { EcalRecHit::kNeighboursRecovered, "saturated/isolated dead: energy estimated from neighbours" },
               { EcalRecHit::kTowerRecovered, "channel in TT with no data link, info retrieved from Trigger Primitive" },
               { EcalRecHit::kDead, "channel is dead and any recovery fails" },
               { EcalRecHit::kKilled, "MC only flag: the channel is{ EcalRecHit::killed in the real detector" },
               { EcalRecHit::kTPSaturated, "the channel is in a region with saturated TP" },
               { EcalRecHit::kL1SpikeFlag, "the channel is in a region with TP with sFGVB = 0" },
               { EcalRecHit::kWeird, "the signal is believed to originate from an anomalous deposit (spike) " },
               { EcalRecHit::kDiWeird, "the signal is anomalous, and neighbors another anomalous signal  " },
               { EcalRecHit::kHasSwitchToGain6, "at least one data frame is in G6" },
               { EcalRecHit::kHasSwitchToGain1, "at least one data frame is in G1" }
            };
            for(auto& flag : flagDefs)
            {
               if ( hit.checkFlag(flag.first) )
               {
                  if ( flag.first == EcalRecHit::kGood && debug ) std::cout << "\x1B[32m";
                  if ( debug ) std::cout << "    " << flag.second << std::endl;
                  if ( flag.first == EcalRecHit::kGood && debug ) std::cout << "\x1B[0m";

                  if ( checkTowerExists(cluster, tps) )
                     RecHitFlagsTowerHist->Fill(flag.first);
                  else
                     RecHitFlagsNoTowerHist->Fill(flag.first);
               }
            }
         }
      }
   }
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGRateStudies);
