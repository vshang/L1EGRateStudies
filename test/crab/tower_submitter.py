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

#config.Data.totalUnits      = 45 # for tests


config.Site.storageSite        = 'T2_US_Wisconsin'
config.Site.ignoreGlobalBlacklist = True # Needed to add this to process the VBF H125 sample & HLTPhysics & DYJets
#config.Site.whitelist          = ['T2_US_Wisconsin',] # Needed to remove this to process the VBF H125 sample & HLTPhysics & DYJets

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
dataMap['minBias-PU200'] = {'das' : '/NeutrinoGun_E_10GeV/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'}
dataMap['QCD-PU200'] = {'das' : '/QCD_Pt-15To7000_TuneCP5_Flat_14TeV-pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'}

# dasgoclient --query="dataset dataset=/*/*PhaseIIMTDTDRAutumn18DR*/FEVT"

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

        # Tower sum Pu analysis
        config.General.requestName = '20190306_%s_TowerSums_v2' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.JobType.psetName        = 'tower_analyzer_crab.py'
        config.Data.inputDataset = dataMap[ k ][ 'das' ]

        config.Data.unitsPerJob        = 4 # events / job when using EventAwareLumiBased
        config.Data.totalUnits      = 1000 # for tests

        config.Data.outputDatasetTag   = config.General.requestName

        print 'submitting config:'
        print config
        submit(config)


