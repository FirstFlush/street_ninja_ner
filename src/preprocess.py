from datetime import datetime, timezone
import json
import argparse
from pathlib import Path
from spacy.tokens import DocBin
import spacy
from .config import DATA_DIR


class Preprocessor:
    """
    Prepare raw, annotated JSON data from label-studio and output it to
    ml/data/processed as both .json and .spacy formats
    """
    def __init__(self, input_file: str, DATA_DIR: Path):    
        self.input_path = DATA_DIR / "raw" / input_file
        self.timestamp = datetime.now(tz=timezone.utc).strftime('%Y-%m-%d')
        self.output_json_path = self._output_path("json")
        self.output_spacy_path = self._output_path("spacy")

    def _output_path(self, ext:str) -> Path:
        return DATA_DIR / "processed" / f"spacy_training_data__{self.timestamp}.{ext}"

    def preprocess_label_studio_data(self):
        """
        Convert raw Label Studio JSON data into spaCy-compatible training data format
        and save as both .json and .spacy files.
        """
        # Load raw data
        with open(self.input_path, "r") as f:
            raw_data = json.load(f)

        training_data = []
        nlp = spacy.blank("en")  # Create a blank English model
        doc_bin = DocBin()  # Container for serialized spaCy docs

        for item in raw_data:
            text = item["data"]["text"]
            entities = []
            for annotation in item["annotations"]:
                for result in annotation["result"]:
                    start = result["value"]["start"]
                    end = result["value"]["end"]
                    label = result["value"]["labels"][0]
                    entities.append((start, end, label))
            
            # Append to training data for JSON
            training_data.append((text, {"entities": entities}))

            # Create spaCy Doc object for .spacy
            doc = nlp.make_doc(text)
            spans = []
            for start, end, label in entities:
                span = doc.char_span(start, end, label=label)
                if span:
                    spans.append(span)
                else:
                    print(f"Skipping invalid span: {text[start:end]} ({start}, {end})")
            doc.ents = spans
            doc_bin.add(doc)

        # Save the processed data as .json
        with open(self.output_json_path, "w") as f:
            json.dump(training_data, f, indent=4)

        print(f"Processed JSON data saved to {self.output_json_path}")

        # Save the processed data as .spacy
        doc_bin.to_disk(self.output_spacy_path)
        print(f"Processed spaCy data saved to {self.output_spacy_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert raw Label Studio JSON data into spaCy-compatible training format."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input raw JSON file exported from Label Studio."
    )
    args = parser.parse_args()
    Preprocessor(input_file=Path(args.input).name, DATA_DIR=DATA_DIR).preprocess_label_studio_data()
