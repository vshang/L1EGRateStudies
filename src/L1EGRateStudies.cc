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
      const l1slhc::L1EGCrystalCluster * findHighestPtCluster(const l1slhc::L1EGCrystalClusterCollection&, double, double) const;
      bool checkDeltaR(const reco::Candidate::PolarLorentzVector&, const reco::Candidate::PolarLorentzVector&, double) const;
      
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
      
      int nHistBins;
      double histLow;
      double histHigh;
      double histetaLow;
      double histetaHigh;
      std::vector<TH1F *> histograms;
      std::vector<TH1F *> eta_histograms;
      TH1F * efficiency_denominator_hist;
      TH1F * efficiency_denominator_eta_hist;
      TH1F * oldEGalg_efficiency_hist;
      TH1F * oldEGalg_efficiency_eta_hist;
      TH1F * oldEGalg_rate_hist;
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
      // We want to plot efficiency vs. pt and eta, for various hovere and isolation cuts
      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            std::stringstream name;
            name << "crystalEG_efficiency_hovere" << i << "_iso" << j;
            std::stringstream title;
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");Gen. pT (GeV);Efficiency";
            histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistBins, histLow, histHigh);
            name.str("");
            name << "crystalEG_efficiency_hovere" << i << "_iso" << j << "_eta";
            title.str("");
            title << "Crystal-level EG Trigger (hovere "  << hovere_cut << ", iso " << ecal_isolation_cut << ");Gen. #eta;Efficiency";
            eta_histograms[i*cut_steps+j] = fs->make<TH1F>(name.str().c_str(), title.str().c_str(), nHistBins, histetaLow, histetaHigh);
         }
      }
      oldEGalg_efficiency_hist = fs->make<TH1F>("oldEG_efficiency", "Old EG Trigger;Gen. pT (GeV);Efficiency", nHistBins, histLow, histHigh);
      oldEGalg_efficiency_eta_hist = fs->make<TH1F>("oldEG_efficiency_eta", "Old EG Trigger;Gen. #eta;Efficiency", nHistBins, histetaLow, histetaHigh);

      // We don't want to save these, we'll just be dividing by them after looping through all events
      efficiency_denominator_hist = new TH1F("gen_pt", "Old EG Trigger;Gen. pT (GeV); Counts", nHistBins, histLow, histHigh);
      efficiency_denominator_eta_hist = new TH1F("gen_eta", "Old EG Trigger;Gen. #eta; Counts", nHistBins, histetaLow, histetaHigh);
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
   
   if ( doEfficiencyCalc ) {
      // Only one electron is produced in singleElectron files
      // we look for that electron in the reconstructed data within some deltaR cut, 
      // and if we find it, it goes in the numerator
      reco::GenParticle trueElectron = genParticles[0];
      efficiency_denominator_hist->Fill(genParticles[0].pt());
      efficiency_denominator_eta_hist->Fill(genParticles[0].eta());

      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            auto highestCluster = findHighestPtCluster(crystalClusters, hovere_cut, ecal_isolation_cut);
            reco::Candidate::PolarLorentzVector clusterP4(highestCluster->et, highestCluster->eta, highestCluster->phi, 0.);
            if ( highestCluster->hovere < hovere_cut 
                  && highestCluster->ECALiso < ecal_isolation_cut 
                  && checkDeltaR(clusterP4, genParticles[0].polarP4(), 0.1) ) {
               histograms[i*cut_steps+j]->Fill(genParticles[0].pt());
               eta_histograms[i*cut_steps+j]->Fill(genParticles[0].eta());
            }
         }
      }
      
      if ( checkDeltaR(highestEGCandidate->polarP4(), genParticles[0].polarP4(), 0.1) ) {
         oldEGalg_efficiency_hist->Fill(genParticles[0].pt());
         oldEGalg_efficiency_eta_hist->Fill(genParticles[0].eta());
      }
   } else {
      // Fill rate histograms
      for(int i=0; i<cut_steps; i++) {
         double hovere_cut = hovere_cut_min+(hovere_cut_max-hovere_cut_min)*i/(cut_steps-1);
         for(int j=0; j<cut_steps; j++) {
            double ecal_isolation_cut = ecal_isolation_cut_min+(ecal_isolation_cut_max-ecal_isolation_cut_min)*j/(cut_steps-1);
            auto highestCluster = findHighestPtCluster(crystalClusters, hovere_cut, ecal_isolation_cut);
            if ( highestCluster->hovere < hovere_cut 
                  && highestCluster->ECALiso < ecal_isolation_cut ) {
               histograms[i*cut_steps+j]->Fill(highestCluster->et);
            }
         }
      }
      oldEGalg_rate_hist->Fill(highestEGCandidate->pt());
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
      for(auto it=histograms.begin(); it!=histograms.end(); it++) {
         (*it)->Divide(efficiency_denominator_hist);
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
L1EGRateStudies::findHighestPtCluster(const l1slhc::L1EGCrystalClusterCollection& clusters, double hovere_cut, double iso_cut) const {
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

bool 
L1EGRateStudies::checkDeltaR(const reco::Candidate::PolarLorentzVector& a, const reco::Candidate::PolarLorentzVector& b, double radius) const {
   double deta = a.eta() - b.eta();
   double dphi = a.phi() - b.phi();
   return sqrt(pow(deta,2)+pow(dphi,2)) < radius;
}

//define this as a plug-in
DEFINE_FWK_MODULE(L1EGRateStudies);
