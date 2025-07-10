# 🥷 NinjaTag


**NinjaTag** is a Machine Learning Named Entity Recognition (NER) system designed to process messy, short-form SMS messages submitted by users of the Street Ninja app. Its purpose is to extract structured information — like the type of resource being requested and the location — in order to route requests to the right services within the Street Ninja system.

This project focuses on building a production-quality NER pipeline tailored to the specific challenges of SMS data:

- Short, often ungrammatical or fragmented messages
- Inconsistent capitalization, slang, or spelling
- Real-world location references that are vague, incomplete, or non-standard
- Entities that blend meaning or overlap

Requests with implied qualifiers like safety, accessibility, or language needs


## ✨ What It Does

This system is designed to extract 3 key types of entities from user messages:

- **RESOURCE** — what the user is asking for (e.g. shelter, wifi, food)
- **LOCATION** — where they want it (e.g. intersection, neighborhood, landmark)
- **QUALIFIER** — constraints on the request (e.g. “for women only”, “pet-friendly”)

These entities are later used to route or match requests within the Street Ninja platform.


## 🎯 Why This Exists

This is a learning-first, build-second machine learning project.

- I’m using this project to learn about **annotation**, **NER modeling**, **data cleaning**, and **ML engineering best practices**
- The system is built with **spaCy**, **Label Studio**, and fully manual annotations
- My goal is not just to get good results, but to understand how to build NER systems that are reliable, modular, and extensible


## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.


## ⚠️ Disclaimer

This project is actively evolving. It’s not intended for general use, production deployment, or distribution.

---

Thanks for checking it out ✌️  