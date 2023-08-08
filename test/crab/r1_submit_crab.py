from collections import OrderedDict
from CRABClient.UserUtilities import config
import os

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile

config = config()

config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName      = 'Analysis'
config.JobType.maxMemoryMB     = 2500
config.JobType.priority        = 2
config.Data.splitting      = 'FileBased'
config.Data.unitsPerJob        = 3 # events / job when using EventAwareLumiBased
config.Data.publication        = False

#config.Data.totalUnits      = 45 # for tests


config.Site.storageSite        = 'T2_US_Wisconsin'
config.Site.ignoreGlobalBlacklist = True # Needed to add this to process the VBF H125 sample & HLTPhysics & DYJets
#config.Site.whitelist          = ['T2_US_Wisconsin',] # Needed to remove this to process the VBF H125 sample & HLTPhysics & DYJets

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
#dataMap['TTbar-PU200'] = {'das' : '/TT_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v2/FEVT'}
#dataMap['minBias-PU200'] = {'das' : '/MinBias_TuneCP5_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_withNewMB_111X_mcRun4_realistic_T15_v1_ext1-v2/FEVT'}
dataMap['minBias-PU200_v27'] = {'das' : '/MinBias_TuneCP5_14TeV-pythia8/Phase2Fall22DRMiniAOD-PU200_125X_mcRun4_realistic_v2-v1/GEN-SIM-DIGI-RAW-MINIAOD'}
#dataMap['VBFHTT-PU200'] = {'das' : '/VBFHToTauTau_M125_14TeV_powheg_pythia8_correctedGridpack_tuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT'}
#dataMap['VBFHTT-PU200_v27'] = {'das' : '/VBFHToTauTau_M-125_TuneCP5_14TeV-powheg-pythia8/Phase2Fall22DRMiniAOD-PU200_125X_mcRun4_realistic_v2-v1/GEN-SIM-DIGI-RAW-MINIAOD'}
#dataMap['QCD-PU200'] = {'das' : '/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_castor_111X_mcRun4_realistic_T15_v1-v1/FEVT'}
#dataMap['QCD-PU200_v27'] = {'das' : '/QCD_Pt-15To3000_TuneCP5_Flat_14TeV-pythia8/Phase2Fall22DRMiniAOD-PU200_125X_mcRun4_realistic_v2-v1/GEN-SIM-DIGI-RAW-MINIAOD'}

# dasgoclient --query="dataset dataset=/*/*PhaseIIMTDTDRAutumn18DR*/FEVT"
# dasgoclient --query="dataset dataset=/VBFHToTauTau*/Phase2HLTTDR*/FEVT"


#if __name__ == '__main__':
if True:

    # from CRABAPI.RawCommand import crabCommand
    # from CRABClient.ClientExceptions import ClientException
    # from httplib import HTTPException

    # def submit(config):
    #     try:
    #         crabCommand('submit', config = config)
    #     except HTTPException as hte:
    #         print("Failed submitting task: %s" % (hte.headers))
    #     except ClientException as cle:
    #         print("Failed submitting task: %s" % (cle))

    datasets = OrderedDict()
   
    base = os.getenv("CMSSW_BASE")
    print("Base: ",base)
    for k in dataMap.keys() :

        # Normal eff and rate analysis
        config.General.requestName = '20230709_%s_r1_CMSSW_12_5_2_patch1_PallabiJets' % k
        config.JobType.psetName        = 'r1_crabby_jets.py'
        config.Data.inputDataset = dataMap[ k ][ 'das' ]
        config.Data.inputBlocks = [
            dataMap[ k ][ 'das' ] + '#0b9c9825-909a-4fe3-bb4b-80a429017a82',
        ]
        if 'PU200' in k or 'PU140' in k :
            #config.Data.unitsPerJob        = 3 # events / job when using EventAwareLumiBased
            config.Data.unitsPerJob        = 5 # files / job, takes ~ 60min based on 10_5_X MTD samples, 90m for QCD PU200
            config.Data.unitsPerJob        = 10
            #config.Data.totalUnits      = 100 # for tests
        else :
            config.Data.unitsPerJob        = 3 # events / job when using EventAwareLumiBased
            #config.Data.totalUnits      = 30 # for tests
        #config.Data.unitsPerJob        = 2 # events / job when using EventAwareLumiBased
        #config.Data.totalUnits      = 10 # for tests

        config.Data.outputDatasetTag   = config.General.requestName

        # print('submitting config:')
        # print(config)
        # submit(config)


