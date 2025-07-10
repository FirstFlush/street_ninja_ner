This folder holds all the data used for training the Street Ninja NER model.

- `source_sms/` — Original .txt files with unlabeled SMS messages  
- `labeled/` — JSON files exported from Label Studio after annotation  
- `converted/` — JSON files converted into spaCy format (text + entity spans)  
- `spacy/` — .spacy binary files used for training and evaluation  
- `examples/` — Sample/demo files for showcasing only (not used in training)