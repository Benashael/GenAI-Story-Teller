import streamlit as st
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the fine-tuned GPT-2 model and tokenizer
model_path = "./fine-tuned-gpt2"
model = GPT2LMHeadModel.from_pretrained(model_path)
tokenizer = GPT2Tokenizer.from_pretrained(model_path)

# Function to generate stories based on user inputs
def generate_story(genre, tone, max_words, prompt, purpose):
    # Combine user inputs to create a prompt
    user_prompt = f"Genre: {genre}, Tone: {tone}, Max Words: {max_words}, Prompt: {prompt}, Purpose: {purpose}. "
    
    # Tokenize the prompt
    input_ids = tokenizer.encode(user_prompt, return_tensors="pt", max_length=100, truncation=True)
    
    # Generate a story using the fine-tuned model
    output = model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
    
    # Decode and return the generated story
    generated_story = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_story

# Streamlit UI
st.title("GenAI Storyteller")
genre = st.selectbox("Select Genre:", ["Sci-Fi", "Mystery", "Fantasy", "Adventure"])
tone = st.selectbox("Select Tone:", ["Positive", "Negative", "Neutral"])
max_words = st.slider("Select Maximum Words:", 0, 500, 250, 10)
prompt = st.text_input("Enter Prompt (less than 15 words):")
purpose = st.selectbox("Select Purpose:", ["Education", "Storytelling for Children", "Entertainment", "Inspiration"])

# Button to generate and display the story
if st.button("Generate Story"):
    generated_story = generate_story(genre, tone, max_words, prompt, purpose)
    st.subheader("Generated Story:")
    st.write(generated_story)
