# Summer student project about feasibility study for rare W decay to Ds + photon

## CMSSW setup
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv

#setup nanoAOD-tools
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j 8

#This package
git clone https://github.com/cecilecaillol/WToDsGamma.git
scram b -j 8
```


