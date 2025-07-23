from ...common.io import FileReader, ConsoleWriter
from pathlib import Path


class MissedEntityHandler:

    def __init__(
            self, 
            file_reader: FileReader = FileReader(), 
            console_writer: ConsoleWriter = ConsoleWriter()
    ):
        self.file_reader = file_reader
        self.console_writer = console_writer

    def echo_missed_entities(self, json_path: Path):

        results = self.file_reader.json_from_file(json_path)

        for example in results.get("examples", []):
            for ent in example.get("missing", []):
                text = example.get("text", "[No text]")
                self.console_writer.echo(f"MISS: {ent['label']} | '{ent['text']}' in: {text}")

        self.console_writer.echo("\n=== Wrong Entities (False Positives) ===")
        for example in results.get("examples", []):
            for ent in example.get("wrong", []):
                text = example.get("text", "[No text]")
                self.console_writer.echo(f"WRONG: {ent['label']} | '{ent['text']}' in: {text}")
