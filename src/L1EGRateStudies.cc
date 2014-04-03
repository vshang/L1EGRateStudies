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

#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/SLHC/interface/L1EGCrystalCluster.h"

#include "DataFormats/L1Trigger/interface/L1EmParticle.h"
#include "DataFormats/L1Trigger/interface/L1EmParticleFwd.h"


// For sorting
namespace l1extra {
  class EtComparator {
  public:
    bool operator()(const l1extra::L1EmParticle a, const l1extra::L1EmParticle b) const {
      double et_a = 0.0;
      double et_b = 0.0;    
      if (cosh(a.eta()) > 0.0) et_a = a.energy()/cosh(a.eta());
      if (cosh(b.eta()) > 0.0) et_b = b.energy()/cosh(b.eta());
      
      return et_a > et_b;
    }
  };
  class ClusterETComparator {
  public:
    bool operator()(const l1slhc::L1EGCrystalCluster a, const l1slhc::L1EGCrystalCluster b) const {
      return a.et > b.et;
    }
  };
}

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
      const l1slhc::L1EGCrystalCluster * findHighestPtCluster(const l1slhc::L1EGCrystalClusterCollection&) const;
      inline double deltaR(const reco::Candidate::PolarLorentzVector& a, const reco::Candidate::PolarLorentzVector& b){return reco::deltaR(a,b);};
      double deltaR(const l1slhc::L1EGCrystalCluster& a, const reco::Candidate::PolarLorentzVector& b); 
      
      // ----------member data ---------------------------
      bool doEfficiencyCalc;
      
      double hovere_cut_min;
      double hovere_cut_max;
      double ecal_isolation_cut_min;
      double ecal_isolation_cut_max;
      int cut_steps;
      
      int eventCount;
      edm::InputTag L1EGammaInputTag;
      edm::InputTag L1CrystalClustersInputTag;
      // electron candidates
      l1extra::L1EmParticleCollection eGammaCollection;
      edm::Handle<l1extra::L1EmParticleCollection> EGammaHandle;
      // electron candidate extra info from Sacha's algorithm
      l1slhc::L1EGCrystalClusterCollection crystalClusters;
      edm::Handle<l1slhc::L1EGCrystalClusterCollection> crystalClustersHandle;      
      // Generator info (truth)
      edm::Handle<reco::GenParticleCollection> genParticleHandle;
      reco::GenParticleCollection genParticles;
      
      int nHistBins, nHistEtaBins;
      double histLow;
      double histHigh;
      double histetaLow;
      double histetaHigh;
      std::vector<TH1F *> histograms;
      std::vector<TH1F *> eta_histograms;
      std::vector<TH1F *> deltaR_histograms;
      TH1F * efficiency_denominator_hist;
      TH1F * efficiency_denominator_eta_hist;
      TH1F * oldEGalg_efficiency_hist;
      TH1F * oldEGalg_efficiency_eta_hist;
      TH1F * oldEGalg_deltaR_hist;
      TH1F * oldEGalg_rate_hist;

      // hovere and iso distributions
      TH1F * hovere_hist;
      TH1F * ecalIso_hist;

      // (pt_reco-pt_gen)/pt_gen plot
      TH1F * reco_gen_pt_hist;
      TH1F * oldAlg_reco_gen_pt_hist;
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
   hovere_cut_min(iConfig.getUntrackedParameter<double>("hovere_cut_min", 0.5)),
   hovere_cut_max(iConfig.getUntrackedParameter<double>("hovere_cut_max", 2.)),
   ecal_isolation_cut_min(iConfig.getUntrackedParameter<double>("ecal_isolation_cut_min", 1.)),
   ecal_isolation_cut_max(iConfig.getUntrackedParameter<double>("ecal_isolation_cut_max", 4.)),
   cut_steps(iConfig.getUntrackedParameter<int>("cut_steps", 4)),
   nHistBins(iConfig.getUntrackedParameter<int>("histogramBinCount", 95)),
   nHistEtaBins(iConfig.getUntrackedParameter<int>("histogramEtaBinCount", 20)),
   histLow(iConfig.getUntrackedParameter<double>("histogramRangeLow", 4.5)),
   histHigh(iConfig.getUntrackedParameter<double>("histogramRangeHigh", 99.5)),
   histetaLow(iConfig.getUntrackedParameter<double>("histogramRangeetaLow", -2.5)),
   histetaHigh(iConfig.getUntrackedParameter<double>("histogramRangeetaHigh", 2.5))
{
   //now do what ever initialization is needed
   eventCount = 0;
   L1EGammaInputTag = iConfig.getParameter<edm::InputTag>("L1EGammaInputTag");
   L1CrystalClustersInputTag = iConfig.getParameter<edm::InputTag>("L1CrystalClustersInputTag");
   
   edm::Service<TFileService> fs;
   
   // Make a set of histograms to fill, depending on if we are doing rate or efficiency
   histograms.resize(cut_steps*cut_steps);
   if ( doEfficiencyCalc ) {
      eta_histograms.resize(cut_steps*cut_steps);
      deltaR_histograms.resize(cut_steps*cut_steps);
      // We want to plot efficiency vs. pt and eta, for various hovere and isolation cuts
      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            std::stringstream name;
            name << "crystalEG_efficiency_hovere" << i << "_iso" << j << "_pt";
            std::stringstream title;
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");Gen. pT (GeV);Efficiency";
            histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistBins, histLow, histHigh);
            name.str("");
            name << "crystalEG_efficiency_hovere" << i << "_iso" << j << "_eta";
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");Gen. #eta;Efficiency";
            eta_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistEtaBins, histetaLow, histetaHigh);
            name.str("");
            name << "crystalEG_deltaR_hovere" << i << "_iso" << j;
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");#Delta R (Gen-Reco);Counts";
            deltaR_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), 30, 0, 0.1);
         }
      }
      oldEGalg_efficiency_hist = fs->make<TH1F>("oldEG_efficiency_pt", "Old EG Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      oldEGalg_efficiency_eta_hist = fs->make<TH1F>("oldEG_efficiency_eta", "Old EG Trigger;Gen. #eta;Efficiency", nHistEtaBins, histetaLow, histetaHigh);
      oldEGalg_deltaR_hist = fs->make<TH1F>("oldEG_deltaR", "Old EG Trigger;#Delta R (Gen-Reco);Counts", 30, 0., 0.1);
      reco_gen_pt_hist = fs->make<TH1F>("reco_gen_pt" , "EG relative momentum error;(pT_{reco}-pT_{gen})/pT_{gen};Counts", 40, -0.2, 0.2); 
      oldAlg_reco_gen_pt_hist = fs->make<TH1F>("oldAlg_reco_gen_pt" , "Old EG relative momentum error;(pT_{reco}-pT_{gen})/pT_{gen};Counts", 40, -0.2, 0.2); 

      // We don't want to save these, we'll just be dividing by them after looping through all events
      efficiency_denominator_hist = new TH1F("gen_pt", "Old EG Trigger;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_eta_hist = new TH1F("gen_eta", "Old EG Trigger;Gen. #eta; Counts", nHistEtaBins, histetaLow, histetaHigh);
   } else {
      // Just want rates as a function of pt, again for various cuts
      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            std::stringstream name;
            name << "crystalEG_rate_hovere" << i << "_iso" << j;
            std::stringstream title;
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");ET Threshold (GeV);Rate (kHz)";
            histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistBins, histLow, histHigh);
         }
      }
      oldEGalg_rate_hist = fs->make<TH1F>("oldEG_rate" , "EG Rates;ET Threshold (GeV);Rate (kHz)", nHistBins, histLow, histHigh);
   }
   hovere_hist = fs->make<TH1F>("hovere" , "EG H/E distribution;HCal energy / ECal energy;Counts", 30, 0, 4); 
   ecalIso_hist = fs->make<TH1F>("ecalIso" , "EG ECal Isolation distribution;ECal Isolation;Counts", 30, 0, 4);
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

   iEvent.getByLabel(L1EGammaInputTag,EGammaHandle);
   eGammaCollection = (*EGammaHandle.product());
   iEvent.getByLabel(L1CrystalClustersInputTag,crystalClustersHandle);
   crystalClusters = (*crystalClustersHandle.product());
   iEvent.getByLabel("genParticles", genParticleHandle);
   genParticles = *genParticleHandle.product();

   // Find highest pt candidates
   double maxPt = -1.;
   l1extra::L1EmParticle * highestEGCandidate = &eGammaCollection[0]; // set only to avoid uninitialized variable complaints
   for(auto it=eGammaCollection.begin(); it!=eGammaCollection.end(); it++) {
      if ( it->pt() > maxPt ) {
         maxPt = it->pt();
         highestEGCandidate = &(*it);
      }
   }
   auto highestCluster = findHighestPtCluster(crystalClusters);
   
   if ( doEfficiencyCalc ) {
      // Only one electron is produced in singleElectron files
      // we look for that electron in the reconstructed data within some deltaR cut, 
      // and if we find it, it goes in the numerator
      efficiency_denominator_hist->Fill(genParticles[0].pt());
      efficiency_denominator_eta_hist->Fill(genParticles[0].eta());

      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            if ( highestCluster->hovere < hovere_cut 
                  && highestCluster->ECALiso < ecal_isolation_cut 
                  && deltaR(*highestCluster, genParticles[0].polarP4()) < 0.1 ) {
               histograms[i*cut_steps+j]->Fill(genParticles[0].pt());
               eta_histograms[i*cut_steps+j]->Fill(genParticles[0].eta());
               deltaR_histograms[i*cut_steps+j]->Fill(deltaR(*highestCluster, genParticles[0].polarP4()));
            }
         }
      }

      // while doing efficiencies, we match up to generated electron
      if ( deltaR(*highestCluster, genParticles[0].polarP4()) < 0.1 ) {
         hovere_hist->Fill(highestCluster->hovere);
         ecalIso_hist->Fill(highestCluster->ECALiso);
         reco_gen_pt_hist->Fill( (highestCluster->et - genParticles[0].pt())/genParticles[0].pt() );
      }
      
      if ( deltaR(highestEGCandidate->polarP4(), genParticles[0].polarP4()) < 0.1 ) {
         oldEGalg_efficiency_hist->Fill(genParticles[0].pt());
         oldEGalg_efficiency_eta_hist->Fill(genParticles[0].eta());
         oldEGalg_deltaR_hist->Fill(deltaR(highestEGCandidate->polarP4(), genParticles[0].polarP4()));
         oldAlg_reco_gen_pt_hist->Fill( (highestEGCandidate->pt() - genParticles[0].pt())/genParticles[0].pt() );
      }
   } else {
      // Fill rate histograms
      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            if ( highestCluster->hovere < hovere_cut 
                  && highestCluster->ECALiso < ecal_isolation_cut ) {
               histograms[i*cut_steps+j]->Fill(highestCluster->et);
            }
         }
      }
      oldEGalg_rate_hist->Fill(highestEGCandidate->pt());
      hovere_hist->Fill(highestCluster->hovere);
      ecalIso_hist->Fill(highestCluster->ECALiso);
   }

   // --- Debug crap below

   // List clusters that did not pass the old algorithm
   auto oldEGP4 = highestEGCandidate->polarP4();
   // Don't do this if we are looking at real electrons!
   if ( !doEfficiencyCalc && highestCluster->et > 40. ) {
      // Show the highest pt Cluster
      double dr = deltaR(*highestCluster, oldEGP4);
      // To be proper, we should use edm::LogInfo("L1EGRateStudies") << "stuff";
      // But this will do for temporary stuff...
      std::cout << "High-pt fake (run,lumi,evt) = (" << iEvent.run() << "," << iEvent.luminosityBlock() << "," << iEvent.id().event() << std::endl;
      std::cout << "\tpt = " << highestCluster->et << ", old EG Candidate pt = " << highestEGCandidate->pt() << ", deltaR = " << dr << std::endl;

      // List the closest clusters to the old EG candidate
      std::cout << "\t---List of clusters close to the old EG Candidate:" << std::endl;
      std::sort(begin(crystalClusters), end(crystalClusters), [&](const l1slhc::L1EGCrystalCluster& a, const l1slhc::L1EGCrystalCluster& b){
         return deltaR(a,oldEGP4) < deltaR(b,oldEGP4);
         });
      for(auto cluster : crystalClusters) {
         std::cout << "\tCluster pt = " << cluster.et << ", eta = " << cluster.eta << ", phi = " << cluster.phi << ", deltaR = " << deltaR(cluster, oldEGP4) << ", hovere = " << cluster.hovere << ", iso = " << cluster.ECALiso << std::endl;
      }
   }
   else if ( doEfficiencyCalc ) {
      // is the closest object the generated e?
      std::sort(begin(crystalClusters), end(crystalClusters), [&](const l1slhc::L1EGCrystalCluster& a, const l1slhc::L1EGCrystalCluster& b){
         return deltaR(a,genParticles[0].polarP4()) < deltaR(b,genParticles[0].polarP4());
         });
      for(auto cluster : crystalClusters) {
         if ( cluster.et == highestCluster->et )
            std::cout << "\x1B[32m"; // green hilight
         std::cout << "\tCluster pt = " << cluster.et << ", eta = " << cluster.eta << ", phi = " << cluster.phi << ", deltaR = " << deltaR(cluster,genParticles[0].polarP4()) << ", hovere = " << cluster.hovere << ", iso = " << cluster.ECALiso << "\x1B[0m" << std::endl;
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
   if ( doEfficiencyCalc ) {
      // Divide through by the denominator histogram
      oldEGalg_efficiency_hist->Divide(efficiency_denominator_hist);
      oldEGalg_efficiency_eta_hist->Divide(efficiency_denominator_eta_hist);
      for(auto& h : histograms) {
         h->Divide(efficiency_denominator_hist);
      }
      for(auto it=eta_histograms.begin(); it!=eta_histograms.end(); it++) {
         (*it)->Divide(efficiency_denominator_eta_hist);
      }
   } else {
      // We currently have an efficiency pdf, we want cdf, so we integrate (downward in pt is inclusive)
      // todo: Apparently, we normalize to 30kHz for some reason
      integrateDown(oldEGalg_rate_hist);
      oldEGalg_rate_hist->Scale(30000./eventCount);
      for(auto it=histograms.begin(); it!=histograms.end(); it++) {
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
   for(int i=hist->GetNbinsX()+1; i>=0; i--) {
      integral += hist->GetBinContent(i);
      hist->SetBinContent(i, integral);
   }
}

const l1slhc::L1EGCrystalCluster * 
L1EGRateStudies::findHighestPtCluster(const l1slhc::L1EGCrystalClusterCollection& clusters) const {
   double maxpt = -1.;
   auto ptr = clusters.begin();
   for(auto it=clusters.begin(); it != clusters.end(); it++) {
      if ( it->et > maxpt ) {
         maxpt = it->et;
         ptr = it;
      }
   }
   return &(*ptr);
}

// Wrapper since L1EGCrystalCluster does not implement the required eta() and phi() getter methods.
double
L1EGRateStudies::deltaR(const l1slhc::L1EGCrystalCluster& a, const reco::Candidate::PolarLorentzVector& b) {
   reco::Candidate::PolarLorentzVector clusterP4(a.et, a.eta, a.phi, 0.);
   return deltaR(clusterP4, b);
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGRateStudies);
