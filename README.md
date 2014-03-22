Follow https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects#Recipe_in_612_SLHC6_patch1
(although you can omit anything related to L1TrackTriggerObjects, as we are not using track-trigger integration)

Then, assuming all is well in your enviroment, move to SLHCUpgradeSimulations, and checkout this repository:

git clone https://github.com/nsmith-/L1EGRateStudies.git

Then build.  If you are at wisconsin, you'll need to be at an sl5 machine, i.e. login02 or login04.  Once there,
some environment tweaks are necessary, you can just add this snippet to your ~/.bashrc

if echo $HOSTNAME|grep -q 'login0[24]'; then
        # SLC5 machine
        echo "Setting up SLC5 tweaks"
        declare -x SCRAM_ARCH="slc5_amd64_gcc462"
        export PATH=~nsmith/slc5/bin:$PATH
        export LD_LIBRARY_PATH=~nsmith/slc5/lib
fi

This is to fix the 'unknown option short' problem when attempting to checkout packages with git.  I compiled
a newer version of git.
