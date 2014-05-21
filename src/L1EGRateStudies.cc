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

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1.h"
#include "TH2.h"

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

//
// class declaration
//
class L1EGRateStudies : public edm::EDAnalyzer {
   public:
      explicit L1EGRateStudies(const edm::ParameterSet&);
      ~L1EGRateStudies();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&);
      //virtual void endRun(edm::Run const&, edm::EventSetup const&);
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&);

      // -- user functions
      void integrateDown(TH1F *);
      inline double deltaR(const reco::Candidate::PolarLorentzVector& a, const reco::Candidate::PolarLorentzVector& b){return reco::deltaR(a,b);};
      double deltaR(const l1slhc::L1EGCrystalCluster& a, const reco::Candidate::PolarLorentzVector& b);
      void fillhovere_isolation_hists(const l1slhc::L1EGCrystalCluster& cluster);
      
      // ----------member data ---------------------------
      bool doEfficiencyCalc;
      bool useOfflineClusters;
      bool debug;
      bool useEndcap;
      
      double hovere_cut_min;
      double hovere_cut_max;
      double ecal_isolation_cut_min;
      double ecal_isolation_cut_max;
      int cut_steps;
      double genMatchDeltaRcut;
      double genMatchRelPtcut;
      
      int eventCount;
      edm::InputTag L1EGammaInputTag;
      edm::InputTag L1EGamma2InputTag;
      edm::InputTag L1CrystalClustersInputTag;
            
      int nHistBins, nHistEtaBins;
      double histLow;
      double histHigh;
      double histetaLow;
      double histetaHigh;
      std::vector<TH1F *> histograms;
      std::vector<TH1F *> eta_histograms;
      std::vector<TH1F *> deltaR_histograms;
      std::vector<TH1F *> deta_histograms;
      std::vector<TH1F *> dphi_histograms;
      TH1F * efficiency_denominator_hist;
      TH1F * efficiency_denominator_eta_hist;
      TH1F * oldEGalg_efficiency_hist;
      TH1F * oldEGalg_efficiency_eta_hist;
      TH1F * oldEGalg_deltaR_hist;
      TH1F * oldEGalg_deta_hist;
      TH1F * oldEGalg_dphi_hist;
      TH1F * oldEGalg_rate_hist;
      TH1F * dynEGalg_efficiency_hist;
      TH1F * dynEGalg_efficiency_eta_hist;
      TH1F * dynEGalg_deltaR_hist;
      TH1F * dynEGalg_deta_hist;
      TH1F * dynEGalg_dphi_hist;
      TH1F * dynEGalg_rate_hist;

      // hovere and iso distributions
      TH1F * hovere_hist_lowpt;
      TH1F * hovere_hist_medpt;
      TH1F * hovere_hist_highpt;
      TH1F * ecalIso_hist_lowpt;
      TH1F * ecalIso_hist_medpt;
      TH1F * ecalIso_hist_highpt;

      // (pt_reco-pt_gen)/pt_gen plot
      TH2F * reco_gen_pt_hist;
      TH2F * oldAlg_reco_gen_pt_hist;
      TH2F * dynAlg_reco_gen_pt_hist;
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
   hovere_cut_min(iConfig.getUntrackedParameter<double>("hovere_cut_min", 0.5)),
   hovere_cut_max(iConfig.getUntrackedParameter<double>("hovere_cut_max", 2.)),
   ecal_isolation_cut_min(iConfig.getUntrackedParameter<double>("ecal_isolation_cut_min", 1.)),
   ecal_isolation_cut_max(iConfig.getUntrackedParameter<double>("ecal_isolation_cut_max", 4.)),
   cut_steps(iConfig.getUntrackedParameter<int>("cut_steps", 4)),
   genMatchDeltaRcut(iConfig.getUntrackedParameter<double>("genMatchDeltaRcut", 0.1)),
   genMatchRelPtcut(iConfig.getUntrackedParameter<double>("genMatchRelPtcut", 0.5)),
   nHistBins(iConfig.getUntrackedParameter<int>("histogramBinCount", 10)),
   nHistEtaBins(iConfig.getUntrackedParameter<int>("histogramEtaBinCount", 20)),
   histLow(iConfig.getUntrackedParameter<double>("histogramRangeLow", 0.)),
   histHigh(iConfig.getUntrackedParameter<double>("histogramRangeHigh", 50.)),
   histetaLow(iConfig.getUntrackedParameter<double>("histogramRangeetaLow", -2.5)),
   histetaHigh(iConfig.getUntrackedParameter<double>("histogramRangeetaHigh", 2.5))
{
   //now do what ever initialization is needed
   eventCount = 0;
   L1EGammaInputTag = iConfig.getParameter<edm::InputTag>("L1EGammaInputTag");
   L1EGamma2InputTag = iConfig.getParameter<edm::InputTag>("L1EGamma2InputTag");
   L1CrystalClustersInputTag = iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag");
   
   edm::Service<TFileService> fs;
   
   // Make a set of histograms to fill, depending on if we are doing rate or efficiency
   histograms.resize(cut_steps*cut_steps);
   if ( doEfficiencyCalc )
   {
      eta_histograms.resize(cut_steps*cut_steps);
      deltaR_histograms.resize(cut_steps*cut_steps);
      deta_histograms.resize(cut_steps*cut_steps);
      dphi_histograms.resize(cut_steps*cut_steps);
      // We want to plot efficiency vs. pt and eta, for various hovere and isolation cuts
      for(int i=0; i<cut_steps; i++)
      {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++)
         {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            std::stringstream name;
            // efficiency
            name << "crystalEG_efficiency_hovere" << i << "_iso" << j << "_pt";
            std::stringstream title;
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");Gen. pT (GeV);Efficiency";
            histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistBins, histLow, histHigh);
            // hovere
            name.str("");
            name << "crystalEG_efficiency_hovere" << i << "_iso" << j << "_eta";
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");Gen. #eta;Efficiency";
            eta_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistEtaBins, histetaLow, histetaHigh);
            // deltaR
            name.str("");
            name << "crystalEG_deltaR_hovere" << i << "_iso" << j;
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");#Delta R (Gen-Reco);Counts";
            deltaR_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), 30, 0, genMatchDeltaRcut);
            // deta
            name.str("");
            name << "crystalEG_deta_hovere" << i << "_iso" << j;
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");d#eta (Gen-Reco);Counts";
            deta_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), 50, -0.1, 0.1);
            // dphi
            name.str("");
            name << "crystalEG_dphi_hovere" << i << "_iso" << j;
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");d#phi (Gen-Reco);Counts";
            dphi_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), 50, -0.1, 0.1);
         }
      }
      oldEGalg_efficiency_hist = fs->make<TH1F>("oldEG_efficiency_pt", "Old EG Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      oldEGalg_efficiency_eta_hist = fs->make<TH1F>("oldEG_efficiency_eta", "Old EG Trigger;Gen. #eta;Efficiency", nHistEtaBins, histetaLow, histetaHigh);
      oldEGalg_deltaR_hist = fs->make<TH1F>("oldEG_deltaR", "Old EG Trigger;#Delta R (Gen-Reco);Counts", 30, 0., genMatchDeltaRcut);
      oldEGalg_deta_hist = fs->make<TH1F>("oldEG_deta", "Old EG Trigger;d#eta (Gen-Reco);Counts", 50, -0.1, 0.1);
      oldEGalg_dphi_hist = fs->make<TH1F>("oldEG_dphi", "Old EG Trigger;d#phi (Gen-Reco);Counts", 50, -0.1, 0.1);
      dynEGalg_efficiency_hist = fs->make<TH1F>("dynEG_efficiency_pt", "Dynamic EG Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      dynEGalg_efficiency_eta_hist = fs->make<TH1F>("dynEG_efficiency_eta", "Dynamic EG Trigger;Gen. #eta;Efficiency", nHistEtaBins, histetaLow, histetaHigh);
      dynEGalg_deltaR_hist = fs->make<TH1F>("dynEG_deltaR", "Dynamic EG Trigger;#Delta R (Gen-Reco);Counts", 30, 0., genMatchDeltaRcut);
      dynEGalg_deta_hist = fs->make<TH1F>("dynEG_deta", "Dynamic EG Trigger;d#eta (Gen-Reco);Counts", 50, -0.1, 0.1);
      dynEGalg_dphi_hist = fs->make<TH1F>("dynEG_dphi", "Dynamic EG Trigger;d#phi (Gen-Reco);Counts", 50, -0.1, 0.1);
      reco_gen_pt_hist = fs->make<TH2F>("reco_gen_pt" , "EG relative momentum error;pT_{gen};(pT_{reco}-pT_{gen})/pT_{gen};Counts", 40, 0., 50., 40, -0.3, 0.3); 
      oldAlg_reco_gen_pt_hist = fs->make<TH2F>("oldAlg_reco_gen_pt" , "Old EG relative momentum error;pT_{gen};(pT_{reco}-pT_{gen})/pT_{gen};Counts", 40, 0., 50., 40, -0.3, 0.3); 
      dynAlg_reco_gen_pt_hist = fs->make<TH2F>("dynAlg_reco_gen_pt" , "Dynamic EG relative momentum error;pT_{gen};(pT_{reco}-pT_{gen})/pT_{gen};Counts", 40, 0., 50., 40, -0.3, 0.3); 

      // We don't want to save these, we'll just be dividing by them after looping through all events
      efficiency_denominator_hist = new TH1F("gen_pt", "Old EG Trigger;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_eta_hist = new TH1F("gen_eta", "Old EG Trigger;Gen. #eta; Counts", nHistEtaBins, histetaLow, histetaHigh);
   }
   else
   {
      // Just want rates as a function of pt, again for various cuts
      for(int i=0; i<cut_steps; i++)
      {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++)
         {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            std::stringstream name;
            name << "crystalEG_rate_hovere" << i << "_iso" << j;
            std::stringstream title;
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");ET Threshold (GeV);Rate (kHz)";
            histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistBins, histLow, histHigh);
         }
      }
      oldEGalg_rate_hist = fs->make<TH1F>("oldEG_rate" , "EG Rates;ET Threshold (GeV);Rate (kHz)", nHistBins, histLow, histHigh);
      dynEGalg_rate_hist = fs->make<TH1F>("dynEG_rate" , "EG Rates;ET Threshold (GeV);Rate (kHz)", nHistBins, histLow, histHigh);
   }
   hovere_hist_lowpt = fs->make<TH1F>("hovere_lowpt" , "EG H/E distribution (0<pT<15);HCal energy / ECal energy;Counts", 30, 0, 4); 
   hovere_hist_medpt = fs->make<TH1F>("hovere_medpt" , "EG H/E distribution (15<pT<35);HCal energy / ECal energy;Counts", 30, 0, 4); 
   hovere_hist_highpt = fs->make<TH1F>("hovere_highpt" , "EG H/E distribution (35<pT<50);HCal energy / ECal energy;Counts", 30, 0, 4); 
   ecalIso_hist_lowpt = fs->make<TH1F>("ecalIso_lowpt" , "EG ECal Isolation distribution (0<pT<15);ECal Isolation;Counts", 30, 0, 4);
   ecalIso_hist_medpt = fs->make<TH1F>("ecalIso_medpt" , "EG ECal Isolation distribution (15<pT<35);ECal Isolation;Counts", 30, 0, 4);
   ecalIso_hist_highpt = fs->make<TH1F>("ecalIso_highpt" , "EG ECal Isolation distribution (35<pT<50);ECal Isolation;Counts", 30, 0, 4);
}


L1EGRateStudies::~L1EGRateStudies()
{
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
   if ( doEfficiencyCalc ) {
      // Clean up our denominator histograms
      delete efficiency_denominator_hist;
      delete efficiency_denominator_eta_hist;
   }
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
   l1extra::L1EmParticleCollection eGammaCollection;
   edm::Handle<l1extra::L1EmParticleCollection> EGammaHandle;
   iEvent.getByLabel(L1EGammaInputTag,EGammaHandle);
   eGammaCollection = (*EGammaHandle.product());

   // electron candidates 2 (alt. algorithm)
   l1extra::L1EmParticleCollection eGammaCollection2;
   edm::Handle<l1extra::L1EmParticleCollection> EGammaHandle2;
   iEvent.getByLabel(L1EGamma2InputTag,EGammaHandle2);
   eGammaCollection2 = (*EGammaHandle2.product());

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

   // Sort clusters so we can always pick highest pt cluster matching cuts
   std::sort(begin(crystalClusters), end(crystalClusters), [](const l1slhc::L1EGCrystalCluster& a, const l1slhc::L1EGCrystalCluster& b){return a.et > b.et;});
   // also sort old algorithm products
   std::sort(begin(eGammaCollection), end(eGammaCollection), [](const l1extra::L1EmParticle& a, const l1extra::L1EmParticle& b){return a.pt() > b.pt();});
   std::sort(begin(eGammaCollection2), end(eGammaCollection2), [](const l1extra::L1EmParticle& a, const l1extra::L1EmParticle& b){return a.pt() > b.pt();});
   
   if ( doEfficiencyCalc )
   {
      reco::Candidate::PolarLorentzVector trueElectron;
      if ( useOfflineClusters )
      {
         // Get offline cluster info
         edm::Handle<reco::SuperClusterCollection> pBarrelCorSuperClustersHandle;
         iEvent.getByLabel("correctedHybridSuperClusters","",pBarrelCorSuperClustersHandle);
         reco::SuperClusterCollection pBarrelCorSuperClusters = *pBarrelCorSuperClustersHandle.product();

         if ( debug ) std::cout << "pBarrelCorSuperClusters corrected collection size : " << pBarrelCorSuperClusters.size() << std::endl;
         if ( debug )
         {
            for(auto& cluster : pBarrelCorSuperClusters)
            {
              std::cout << " pBarrelCorSuperClusters : pt " 
                  << cluster.energy()/std::cosh(cluster.position().eta()) 
                  << " eta " << cluster.position().eta() 
                  << " phi " << cluster.position().phi() << std::endl;
            }
         }
         
         // Find the cluster corresponding to generated electron
         bool trueEfound = false;
         for(auto& cluster : pBarrelCorSuperClusters)
         {
            reco::Candidate::PolarLorentzVector p4;
            p4.SetPt(cluster.energy()*sin(cluster.position().theta()));
            p4.SetEta(cluster.position().eta());
            p4.SetPhi(cluster.position().phi());
            p4.SetM(0.);
            if ( deltaR(p4, genParticles[0].polarP4()) < genMatchDeltaRcut )
            {
               trueElectron = p4;
               trueEfound = true;
               break;
            }
         }
         if ( !trueEfound )
         {
            // if we can't offline reconstruct the generated electron, 
            // it might as well have not existed.
            eventCount--;
            return;
         }
      }
      else // !useOfflineClusters
      {
         trueElectron = genParticles[0].polarP4();
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
      efficiency_denominator_eta_hist->Fill(trueElectron.eta());

      for(int i=0; i<cut_steps; i++)
      {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++)
         {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            
            // Since this iterates in order, we automatically get the highest pt cluster with the given cut
            for(auto cluster : crystalClusters)
            {
               if ( cluster.hovere < hovere_cut 
                     && cluster.ECALiso < ecal_isolation_cut 
                     && deltaR(cluster, trueElectron) < genMatchDeltaRcut
                     && fabs(cluster.et-trueElectron.pt())/trueElectron.pt() < genMatchRelPtcut )
               {
                  histograms[i*cut_steps+j]->Fill(trueElectron.pt());
                  eta_histograms[i*cut_steps+j]->Fill(trueElectron.eta());
                  deltaR_histograms[i*cut_steps+j]->Fill(deltaR(cluster, trueElectron));
                  deta_histograms[i*cut_steps+j]->Fill(trueElectron.eta()-cluster.eta);
                  dphi_histograms[i*cut_steps+j]->Fill(reco::deltaPhi(cluster.phi, trueElectron.phi()));
                  // Found one, don't find more!
                  break;
               }
            }
         }
      }

      for(auto cluster : crystalClusters)
      {
         if ( deltaR(cluster, trueElectron) < genMatchDeltaRcut
              && fabs(cluster.et-trueElectron.pt())/trueElectron.pt() < genMatchRelPtcut)
         {
            fillhovere_isolation_hists(cluster);
            reco_gen_pt_hist->Fill( trueElectron.pt(), (cluster.et - trueElectron.pt())/trueElectron.pt() );
            break;
         }
      }
      
      for(auto oldEGCandidate : eGammaCollection)
      {
         if ( deltaR(oldEGCandidate.polarP4(), trueElectron) < genMatchDeltaRcut &&
              fabs(oldEGCandidate.pt()-trueElectron.pt())/trueElectron.pt() < genMatchRelPtcut )
         {
            oldEGalg_efficiency_hist->Fill(trueElectron.pt());
            oldEGalg_efficiency_eta_hist->Fill(trueElectron.eta());
            oldEGalg_deltaR_hist->Fill(deltaR(oldEGCandidate.polarP4(), trueElectron));
            oldEGalg_deta_hist->Fill(trueElectron.eta()-oldEGCandidate.eta());
            oldEGalg_dphi_hist->Fill(reco::deltaPhi(oldEGCandidate.phi(), trueElectron.phi()));
            oldAlg_reco_gen_pt_hist->Fill( trueElectron.pt(), (oldEGCandidate.pt() - trueElectron.pt())/trueElectron.pt() );
            break;
         }
      }

      for(auto oldEGCandidate : eGammaCollection2)
      {
         if ( deltaR(oldEGCandidate.polarP4(), genParticles[0].polarP4()) < genMatchDeltaRcut &&
              fabs(oldEGCandidate.pt()-genParticles[0].pt())/genParticles[0].pt() < genMatchRelPtcut )
         {
            dynEGalg_efficiency_hist->Fill(genParticles[0].pt());
            dynEGalg_efficiency_eta_hist->Fill(genParticles[0].eta());
            dynEGalg_deltaR_hist->Fill(deltaR(oldEGCandidate.polarP4(), genParticles[0].polarP4()));
            dynEGalg_deta_hist->Fill(genParticles[0].eta()-oldEGCandidate.eta());
            dynEGalg_dphi_hist->Fill(reco::deltaPhi(oldEGCandidate.phi(), genParticles[0].phi()));
            dynAlg_reco_gen_pt_hist->Fill( genParticles[0].pt(), (oldEGCandidate.pt() - genParticles[0].pt())/genParticles[0].pt() );
            break;
         }
      }
   }
   else // !doEfficiencyCalc
   {
      // Fill rate histograms
      for(int i=0; i<cut_steps; i++)
      {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++)
         {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            // List is sorted by pt
            for(const auto& cluster : crystalClusters)
            {
               if ( cluster.hovere < hovere_cut 
                     && cluster.ECALiso < ecal_isolation_cut )
               {
                  histograms[i*cut_steps+j]->Fill(cluster.et);
                  break;
               }
            }
         }
      }

      if ( eGammaCollection.size() > 0 )
      {
         auto& highestEGCandidate = eGammaCollection[0];
         // Don't fill old alg. plots if in endcap
         if ( useEndcap
               || (!useEndcap && fabs(highestEGCandidate.eta()) < 1.479) )
         {
            oldEGalg_rate_hist->Fill(highestEGCandidate.pt());
         }
      }

      if ( eGammaCollection2.size() > 0 )
      {
         auto& highestEGCandidate = eGammaCollection2[0];
         if ( useEndcap
               || (!useEndcap && fabs(highestEGCandidate.eta()) < 1.479) )
         {
            dynEGalg_rate_hist->Fill(highestEGCandidate.pt());
         }
      }
      fillhovere_isolation_hists(crystalClusters[0]);
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
   if ( doEfficiencyCalc )
   {
      // Divide through by the denominator histogram
      oldEGalg_efficiency_hist->Divide(efficiency_denominator_hist);
      oldEGalg_efficiency_eta_hist->Divide(efficiency_denominator_eta_hist);
      dynEGalg_efficiency_hist->Divide(efficiency_denominator_hist);
      dynEGalg_efficiency_eta_hist->Divide(efficiency_denominator_eta_hist);
      for(auto& h : histograms)
      {
         h->Divide(efficiency_denominator_hist);
      }
      for(auto it=eta_histograms.begin(); it!=eta_histograms.end(); it++)
      {
         (*it)->Divide(efficiency_denominator_eta_hist);
      }
   }
   else
   {
      // We currently have an efficiency pdf, we want cdf, so we integrate (downward in pt is inclusive)
      // We normalize to 30MHz as this will be the crossing rate of filled bunches in SLHC
      integrateDown(oldEGalg_rate_hist);
      integrateDown(dynEGalg_rate_hist);
      oldEGalg_rate_hist->Scale(30000./eventCount);
      dynEGalg_rate_hist->Scale(30000./eventCount);
      for(auto it=histograms.begin(); it!=histograms.end(); it++)
      {
         integrateDown(*it);
         (*it)->Scale(30000./eventCount);
      }
   }
}

// ------------ method called when starting to processes a run  ------------
/*
void 
L1EGRateStudies::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

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

// Wrapper since L1EGCrystalCluster does not implement the required eta() and phi() getter methods.
double
L1EGRateStudies::deltaR(const l1slhc::L1EGCrystalCluster& a, const reco::Candidate::PolarLorentzVector& b) {
   reco::Candidate::PolarLorentzVector clusterP4(a.et, a.eta, a.phi, 0.);
   return deltaR(clusterP4, b);
}

void
L1EGRateStudies::fillhovere_isolation_hists(const l1slhc::L1EGCrystalCluster& cluster) {
   if ( cluster.et < 15. )
   {
      hovere_hist_lowpt->Fill(cluster.hovere);
      ecalIso_hist_lowpt->Fill(cluster.ECALiso);
   }
   else if ( cluster.et > 15. && cluster.et < 35. )
   {
      hovere_hist_medpt->Fill(cluster.hovere);
      ecalIso_hist_medpt->Fill(cluster.ECALiso);
   }
   else if ( cluster.et > 35. && cluster.et < 50. )
   {
      hovere_hist_highpt->Fill(cluster.hovere);
      ecalIso_hist_highpt->Fill(cluster.ECALiso);
   }
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGRateStudies);
