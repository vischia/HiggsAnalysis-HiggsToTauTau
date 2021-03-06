#!/bin/bash

echo "Combining VHTT shape files and running horizontal interpolation"

lltCategories="emt,mmt" 
zhCategories="mmmt_zh,mmet_zh,mmme_zh,mmtt_zh,eemt_zh,eeet_zh,eeem_zh,eett_zh" 
lttCategories="ett_sm,mtt_sm" 

domorph() 
{
  echo "Morphing file $1, samples tau tau $2, WW $3, categories $4" 
  echo "110->140, in 0.5"
  horizontal-morphing.py \
    --categories="$4"\
    --samples="$2,$3" \
    --uncerts="" --masses="110,115,120,125,130,135,140" --step-size=0.5 \
    -i $1 
  #horizontal-morphing.py \
    #--categories="$4"\
    #--samples="$3" \
    #--uncerts="" --masses="110,120,130,140" --step-size=0.5 \
    #-i $1 
  echo "140->145, in 1.0"
  horizontal-morphing.py \
    --categories="$4"\
    --samples="$3,$2" \
    --uncerts="" --masses="140,145" --step-size=1 \
    -i $1 
  echo "124.5->126.5, in 0.1"
  horizontal-morphing.py \
    --categories="$4"\
    --samples="$2,$3" \
    --uncerts="" --masses="124,127" --step-size=0.1 \
    -i $1 
}

morph() 
{
  echo "LLT channels"
  domorph $1 "WH{MASS}" "WH_hww{MASS}"  "${lltCategories}"
  domorph $1 "ZH_htt{MASS}" "ZH_hww{MASS}"  "${zhCategories}"
}

echo "Improving ZH shapes"
python improve_zh_shapes.py vhtt_4l.inputs-sm-7TeV.root \
  vhtt_4l.inputs-sm-7TeV-improved.root  

python improve_zh_shapes.py vhtt_4l.inputs-sm-8TeV.root \
  vhtt_4l.inputs-sm-8TeV-improved.root  

#cp vhtt_4l.inputs-sm-7TeV.root \
  #vhtt_4l.inputs-sm-7TeV-improved.root  

#cp vhtt_4l.inputs-sm-8TeV.root \
  #vhtt_4l.inputs-sm-8TeV-improved.root  

echo "Combining 7TeV"
hadd -f vhtt.inputs-sm-7TeV.root \
  vhtt_4l.inputs-sm-7TeV-improved.root \
  vhtt_llt.inputs-sm-7TeV.root

echo "Combining 8TeV"
hadd -f vhtt.inputs-sm-8TeV.root \
  vhtt_4l.inputs-sm-8TeV-improved.root \
  vhtt_llt.inputs-sm-8TeV.root

echo "Adding 145 point WH"
python llt_145.py

echo "Morphing 7TeV"
morph vhtt.inputs-sm-7TeV.root 

echo "Morphing 8TeV"
morph vhtt.inputs-sm-8TeV.root 
