from collections import OrderedDict
from CRABClient.UserUtilities import config
import os

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile

config = config()

config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName      = 'Analysis'
config.JobType.maxMemoryMB     = 3500
config.JobType.priority        = 2
config.Data.splitting      = 'FileBased'
config.Data.unitsPerJob        = 3 # events / job when using EventAwareLumiBased
config.Data.publication        = False

#config.Data.totalUnits      = 15 # for tests


config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.ignoreGlobalBlacklist = True # Needed to add this to process the VBF H125 sample & HLTPhysics & DYJets
#config.Site.whitelist          = ['T2_US_Wisconsin',] # Needed to remove this to process the VBF H125 sample & HLTPhysics & DYJets

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
dataMap['QCD-PU0'] = {'das' : '/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'}
##dataMap['QCD-PU140'] = {'das' : '/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TPU140_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'}
dataMap['QCD-PU200'] = {'das' : '/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TPU200_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'}
##dataMap['minBias-PU0'] = {'das' : '/SingleNeutrino/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'}
##dataMap['minBias-PU140'] = {'das' : '/SingleNeutrino/PhaseIIFall17D-L1TPU140_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'}
dataMap['minBias-PU200'] = {'das' : '/SingleNeutrino/PhaseIIFall17D-L1TPU200_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW'}
#dataMap['TTbar-PU0'] = {'das' : '/TT_TuneCUETP8M2T4_14TeV-powheg-pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v2/GEN-SIM-DIGI-RAW'}
#dataMap['TTbar-PU140'] = {'das' : '/TT_TuneCUETP8M2T4_14TeV-powheg-pythia8/PhaseIIFall17D-L1TPU140_93X_upgrade2023_realistic_v5-v2/GEN-SIM-DIGI-RAW'}
#dataMap['TTbar-PU200'] = {'das' : '/TT_TuneCUETP8M2T4_14TeV-powheg-pythia8/PhaseIIFall17D-L1TPU200_93X_upgrade2023_realistic_v5-v2/GEN-SIM-DIGI-RAW'}

# dasgoclient --query="dataset=/SingleNeutrino/PhaseIIFall17D-L1T*_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW"
# dasgoclient --query="dataset=/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1T*_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW"

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    datasets = OrderedDict()
   
    base = os.getenv("CMSSW_BASE")
    print "Base: ",base
    for k in dataMap.keys() :
        config.General.requestName = '20181027_%s_Calibrated_v2' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.JobType.psetName        = 'crabby_jets.py'
        if 'minBias' in k :
            config.JobType.psetName        = 'rate_crabby_jets.py'
        config.Data.inputDataset = dataMap[ k ][ 'das' ]
        if 'PU200' in k or 'PU140' in k :
            config.Data.unitsPerJob        = 20 # events / job when using EventAwareLumiBased
        else :
            config.Data.unitsPerJob        = 3 # events / job when using EventAwareLumiBased
        print 'submitting config:'
        print config
        submit(config)
