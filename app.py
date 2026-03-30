# FINAL MARATHIVANI CODE - Text + Audio working, Image with better error handling

import os
from groq import Groq
import gradio as gr
from gtts import gTTS
from huggingface_hub import InferenceClient
import io
import tempfile

# ============== YOUR KEYS ==============
GROQ_API_KEY = "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"   # ← your Groq key
HF_TOKEN = "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"   # ← your Hugging Face token

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
groq_client = Groq()
hf_client = InferenceClient("black-forest-labs/FLUX.1-schnell", token=HF_TOKEN)

def marathivani(topic: str, grade: str = "8-10"):
    try:
        # 1. Text Generation (Working)
        system_prompt = """तुम्ही मराठीवाणी आहात. कक्षा ८-१० च्या विद्यार्थ्यांसाठी सोप्या मराठीत स्पष्ट स्पष्टीकरण द्या."""
        chat = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": f"सोप्या मराठीत '{topic}' चे स्पष्टीकरण द्या."}],
            temperature=0.7, max_tokens=700
        )
        marathi_text = chat.choices[0].message.content

        # 2. Audio (save to a temp file path that Gradio Audio accepts reliably)
        audio_path = None
        try:
            tts = gTTS(text=marathi_text, lang='mr', slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                audio_path = tmp_audio.name
            tts.save(audio_path)
        except Exception as audio_err:
            print("Audio error:", str(audio_err))
            audio_path = None

        # 3. Image (FLUX) - with error catching
        try:
            image_prompt = f"Simple educational diagram explaining {topic} for school students, clean, labeled in Marathi"
            image = hf_client.text_to_image(image_prompt, num_inference_steps=4)
        except Exception as img_err:
            print("Image error:", str(img_err))
            image = None   # fallback

        return marathi_text, image, audio_path

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print("=== FULL ERROR ===", error_msg)
        return error_msg, None, None

# Gradio Interface
with gr.Blocks(title="MarathiVani") as demo:
    gr.Markdown("# 🎓 मराठीवाणी – ग्रामीण महाराष्ट्रासाठी जनरेटिव्ह AI ट्यूटर")
    gr.Markdown("कोणताही विषय टाइप करा → मराठी स्पष्टीकरण + डायग्राम + आवाज मिळवा")
    
    with gr.Row():
        topic = gr.Textbox(label="विषय (उदा. प्रकाशसंश्लेषण)", placeholder="प्रकाशसंश्लेषण")
        grade = gr.Dropdown(["8-10"], value="8-10", label="वर्ग")
    
    btn = gr.Button("Generate", variant="primary")
    
    with gr.Row():
        text_out = gr.Textbox(label="📝 मराठी स्पष्टीकरण", lines=8)
        image_out = gr.Image(label="🖼️ डायग्राम")
        audio_out = gr.Audio(type="filepath", label="🔊 मराठी आवाज")

    btn.click(marathivani, inputs=[topic, grade], outputs=[text_out, image_out, audio_out])

demo.launch(share=True)