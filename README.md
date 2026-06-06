# Antarman AI

🚧 Status: Early Prototype / Active Development

An open-source mental health AI for Indian languages — built for privacy, accessibility, and cultural context.

## Problem statement
Mental health resources in India are scarce, often stigmatized, and frequently unavailable in local languages. Antarman AI aims to change that by exploring a privacy-preserving, culturally aware conversational assistant tailored to Indian languages and users.

## What we're building
We are building a conversational AI assistant for mental health support with an emphasis on Indian languages and local context. In development we are:

- Building a conversational assistant that can support Hindi, Tamil, Telugu, Kannada, and additional Indian languages.
- Designing the system to run locally or via an API to avoid mandatory cloud dependency.
- Grounding responses in clinical knowledge and culturally-aware phrasing.
- Adding real-time crisis detection capabilities to identify and surface high-risk conversations.
- Prioritizing user privacy, safety, and a free-to-use stack.

## Technical approach (Evolving)
This project is research-first and actively evolving. Current technical directions under evaluation include:

- LLM backbone: Evaluating open-weight, multilingual-friendly models suitable for constrained hardware and low-resource languages.
- Fine-tuning strategy: Exploring parameter-efficient adaptation (for example, adapter-style or LoRA-like methods) to reduce compute and memory costs.
- Knowledge retrieval: Implementing a retrieval-augmented generation (RAG) pipeline over curated mental health and clinical sources to ground outputs.
- Crisis detection: A classifier layer to detect high-risk content and trigger safe-handling workflows.
- Safety layer: Content moderation and safety filtering to reduce harmful or unsafe responses.
- Languages: Supporting Indian languages via multilingual embeddings, language-specific adapters, or lightweight local models where appropriate.

Note: Specific models, libraries, and tools will be finalized as research and evaluation progress. We are intentionally keeping choices flexible to balance privacy, accuracy, and deployment constraints.

## Project structure
Antarman-AI/
├── backend/        # Core AI logic and API layer  
├── Docs/           # Research notes, architecture decisions  
├── scratch/        # Experiments and prototypes  
├── main.py         # Entry point  
└── README.md

## Roadmap
- [ ] Define final model stack and language targets
- [ ] Build basic conversational prototype (CLI)
- [ ] Add RAG pipeline over mental health knowledge base
- [ ] Integrate crisis detection classifier
- [ ] Add Indian language support
- [ ] Build simple web/chat UI
- [ ] Safety and evaluation benchmarks
- [ ] Community feedback and iteration

## Getting started
Clone the repository and run the minimal prototype (full setup docs coming soon):

```bash
git clone https://github.com/venky0112/Antarman-AI.git
cd Antarman-AI
pip install -r requirements.txt
python main.py
```

Note: requirements.txt and comprehensive setup instructions are coming soon. This repository is a research prototype and dependencies and setup steps will change as the project matures.

## Contributing
This project is in early stages. Contributions, ideas, and feedback are welcome — please open an issue to start a conversation. If you want to collaborate on language support, safety evaluations, or clinical grounding, describe your proposal in an issue or discussion.

## Ethics & Safety
We are committed to responsible development. Antarman AI is being built with safety checks, crisis detection, and content moderation in mind. We will continue to consult domain experts and follow best practices for research on mental health tools.

## Disclaimer
⚠️ Antarman AI is a research prototype. It is not a substitute for professional mental health care. If you or someone you know is in crisis, please contact a licensed mental health professional or a crisis helpline.

## License
MIT License (placeholder)
