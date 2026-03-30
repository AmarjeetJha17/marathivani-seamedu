# MarathiVani – Generative AI Tutor for Rural Maharashtra Students

**Seamedu Awards 2026 – Best Generative AI Project Award**

Multi-modal generative AI application that takes any topic and instantly generates:
- Simple Marathi explanation (Llama-3.1)
- Educational diagram (FLUX.1-schnell)
- Natural Marathi voice-over (gTTS)

### Live Demo
🔗 **https://huggingface.co/spaces/AmarjeetJha04/marathivani**

### Features
- Fully Marathi interface and output
- Text + Image + Audio generation in one click
- Fast inference using Groq + Hugging Face
- Designed for Class 8–10 Science & History students

### Tech Stack
- **Text**: Llama-3.1-8B-Instant (Groq)
- **Image**: FLUX.1-schnell (Hugging Face Inference)
- **Audio**: gTTS (Marathi)
- **UI**: Gradio
- **Deployment**: Hugging Face Spaces

### How to Run Locally
```bash
git clone https://github.com/AmarjeetJha17/marathivani-seamedu.git
cd marathivani-seamedu
pip install -r requirements.txt
python app.py
