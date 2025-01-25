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


## Notes

- This is a prototype and will likely evolve as I learn more about ML and refine the approach
- It is intended to assist with SMS parsing in the [Street Ninja](https://github.com/FirstFlush/street_ninja/) project but remains a standalone component for now.


## Future Plans

- Improve entity recognition for nuanced queries (e.g., slang or typos).
- Add support for training with larger datasets.
- Integration into the main Street Ninja app.


## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
