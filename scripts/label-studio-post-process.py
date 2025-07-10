from datetime import datetime, timezone
from pathlib import Path
import json
import typer
from typing import Any

app = typer.Typer()

class LabelStudioConverter:

    OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "processed" 

    def convert(self, input_path: Path):
        output_path = self._output_path()
        spacy_data = self._convert(input_path)
        self._save(output_path=output_path, spacy_data=spacy_data)
        print(f"Converted {len(spacy_data)} examples → {self._output_path}")

    def _output_path(self, input_path: Path) -> Path:
        return self.OUTPUT_DIR / f"{input_path.name}__{self._timestamp()}"

    def _timestamp(self) -> str:
        return datetime.now(tz=timezone.utc).strftime("%y-%m-%d_%H-%M-%S")

    def _save(self, output_path: Path, spacy_data: list[dict[str, Any]]):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out:
            json.dump(spacy_data, out, indent=2)

    def _convert(self, input_path: Path) -> list[dict[str, Any]]:
        """Convert Label Studio JSON to spaCy training format."""
        with open(input_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        spacy_data: list[dict[str, Any]] = []

        for item in raw_data:
            text = item["data"]["text"]
            entities = []

            results = item.get("annotations", [])[0].get("result", [])

            for r in results:
                start = r["value"]["start"]
                end = r["value"]["end"]
                label = r["value"]["labels"][0]
                entities.append([start, end, label])

            spacy_data.append({
                "text": text,
                "entities": entities
            })

        return spacy_data


@app.command()
def convert(input_path: Path):
    converter = LabelStudioConverter()
    converter.convert(input_path)


if __name__ == "__main__":
    app()
