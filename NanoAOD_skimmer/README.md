# Analysis

Code to make flat trees from NanoAOD with baseline analysis preselection and keeping only variables of interest.

## To run locally on a file
```
voms-proxy-init --voms=cms --valid=48:0
python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py output root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/130000/45DF9722-B3E4-844B-81DC-1C48ABD84B06.root --bi $CMSSW_BASE/src/WToDsGamma/NanoAOD_skimmer/scripts/keep_in.txt --bo $CMSSW_BASE/src/WToDsGamma/NanoAOD_skimmer/scripts/keep_out.txt -c "1" -I WToDsGamma.NanoAOD_skimmer.WToDsGamma_analysis analysis_wmc
```

## To submit jobs for full datasets over Condor

First edit python/EraConfig.py (data or MC, object preselection in NanoAOD) and scripts/runNtuplizer (which channel to run, where to store the output files)

For MC:

```
python $CMSSW_BASE/src/WToDsGamma/NanoAOD_skimmer/scripts/runNtuplizer.py --in $CMSSW_BASE/src/WToDsGamma/NanoAOD_skimmer/data/listSamplesMC.txt
```

For data: 

```
python $CMSSW_BASE/src/WToDsGamma/NanoAOD_skimmer/scripts/runNtuplizer.py --in $CMSSW_BASE/src/WToDsGamma/NanoAOD_skimmer/data/listSamplesMuonData.txt
```

And follow the instructions printed on the screen (dont forget to type the new voms-proxy-init command printed). 

