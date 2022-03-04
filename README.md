multimodal machine translation(MMT) 
# Our dependency

* PyTorch version == 1.9.1
* Python version == 3.6.7
* timm version == 0.4.12
* vizseq version == 0.1.15
* nltk verison == 3.6.4
* sacrebleu version == 1.5.1

# Install fairseq

```bash
cd fairseq_mmt
pip install --editable ./
```

# multi30k data & flickr30k entities
Multi30k data from [here](https://github.com/multi30k/dataset) and [here](https://www.statmt.org/wmt17/multimodal-task.html)  
flickr30k entities data from [here](https://github.com/BryanPlummer/flickr30k_entities)  
We get multi30k text data from [Revisit-MMT](https://github.com/LividWo/Revisit-MMT)
```bash
cd fairseq_mmt
git clone https://github.com/BryanPlummer/flickr30k_entities.git
cd flickr30k_entities
unzip annotations.zip

# create a directory
flickr30k
├─ flickr30k-images
├─ test2017-images
├─ test_2016_flickr.txt
├─ test_2017_flickr.txt
├─ test_2017_mscoco.txt
├─ test_2018_flickr.txt
├─ testcoco-images
├─ train.txt
└─ val.txt
```

# Image feature
```bash
# please read scripts/README.md
python3 scripts/get_img_feat.py --dataset train
```

# Train and Test
```bash
sh preprocess.sh
sh train_mmt.sh
sh translation_mmt.sh
```

# Create masking data
```bash
pip3 install stanfordcorenlp 
wget https://nlp.stanford.edu/software/stanford-corenlp-latest.zip
unzip stanford-corenlp-latest.zip
cd fairseq_mmt
cat data/multi30k/train.en data/multi30k/valid.en data/multi30k/test.2016.en > train_val_test2016.en
python3 get_and_record_noun_from_f30k_entities.py 
python3 record_color_people_position.py

# create en-de masking data
cd data/masking
python3 match_origin2bpe_position.py
python3 create_masking_multi30k.py         # create mask1-4 & color & people data 

sh preprocess_mmt.sh
```

# Visualization
```bash

```