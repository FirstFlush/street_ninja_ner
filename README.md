# Street Ninja NER Tool

This project is a **Named Entity Recognition (NER)** system designed to parse SMS messages for the [Street Ninja](https://github.com/FirstFlush/street_ninja/) project. It helps extract key entities from user queries, such as resources, addresses, intersections, landmarks, and parameters, while filtering out irrelevant or profane words.

Although this is a side project, it could be integrated into Street Ninja's SMS parsing pipeline if it demonstrates high accuracy and practical value.


## Features

- **Entity Extraction**:
  - Recognizes resource types (e.g., `FOOD`, `SHELTER`, `TOILET`, `WIFI`).
  - Detects addresses, intersections, and landmarks.
  - Extracts specific parameters (e.g., "women's shelter" or "pet-friendly").
- **Preprocessing**:
  - Strips out unnecessary words (e.g., profanity or filler words) before geocoding.
- **CLI Tool**:
  - Streamlined interface to preprocess raw data, train models, and manage workflows.


## Getting Started


### Prerequisites

- Python 3.8+
- spaCy installed (`pip install spacy`)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/FirstFlush/street_ninja.git
   cd street_ninja/ml
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your data:
   - Place your raw JSON data (e.g., Label Studio exports) in the `data/raw/` directory.


## Usage

### CLI Tool

The CLI tool provides a simple way to preprocess data and train models.

#### **Preprocess Raw Data**

Converts raw JSON data into `.spacy` format for training and validation:
```
./cli.py preprocess --input data/raw/your_file.json
```
- Input: Raw JSON file (e.g., Label Studio export).
- Output: Processed data in both `.json` and `.spacy` formats, saved to `data/processed/`.

#### **Train the Model**

Train an NER model using spaCy’s built-in training system:
```
python -m spacy train config.cfg --output ./output --paths.train ./data/processed/spacy_training_data__<date>.spacy --paths.dev ./data/processed/spacy_validation_data__<date>.spacy
```
- `model-best`: Best-performing model (saved in `output/`).
- `model-last`: Final model after training completes.

#### **Test the Model**

Test the trained model on sample queries:
```
import spacy

# Load the trained model
nlp = spacy.load("./output/model-best")

# Test a query
doc = nlp("Looking for a women's shelter near 123 Main St")
for ent in doc.ents:
    print(ent.text, ent.label_)
```


## Notes

- This is a prototype and will likely evolve as I learn more about ML and refine the approach
- It is intended to assist with SMS parsing in the [Street Ninja](https://github.com/FirstFlush/street_ninja/) project but remains a standalone component for now.


## Future Plans

- Improve entity recognition for nuanced queries (e.g., slang or typos).
- Add support for training with larger datasets.
- Integration into the main Street Ninja app.


## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
