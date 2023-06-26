import os
""" Year dependent configurations / files """

ANALYSISTRIGGER = {
    #'2018': {'w':'(1)','tt':'(1)'}
    '2018': {'w':'(1)','tt':'(HLT_IsoMu24)'}
}

ANALYSISCHANNELCUT = {
    #'w':'(nPhoton>0)',
    #'tt':'(nPhoton>0&&(nMuon>0||nElectron>0))'
    'w':'(1)',
    'tt':'(1)'
}

ANALYSISGRL = {
    '2018': 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
}

cmssw=os.environ['CMSSW_BASE']
ANALYSISCUT={'': {'w' : '-c "%s"'%ANALYSISCHANNELCUT['w'],'tt' : '-c "%s"'%ANALYSISCHANNELCUT['tt']}}

## for data, json selection
#for y in ANALYSISTRIGGER:
#  ANALYSISCUT[y]={}
#  for c in ANALYSISTRIGGER[y]:
#    ANALYSISCUT[y][c]='--cut %s&&%s --json %s'%(ANALYSISTRIGGER[y][c],ANALYSISCHANNELCUT[c],cmssw+'/src/CMSDASTools/Analysis/data/'+ANALYSISGRL[y])

## for MC, no json
for y in ANALYSISTRIGGER:
  ANALYSISCUT[y]={}
  for c in ANALYSISTRIGGER[y]:
    ANALYSISCUT[y][c]='--cut %s&&%s '%(ANALYSISTRIGGER[y][c],ANALYSISCHANNELCUT[c])
