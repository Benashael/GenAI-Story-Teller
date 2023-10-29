import streamlit as st
from transformers import pipeline

# Create a text generation pipeline
story_gen = pipeline("text-generation", "pranavpsv/gpt2-genre-story-generator")

# Streamlit app title and description
st.title("AI Story Generator")
st.write("Generate creative stories with the power of AI!")

# Input prompt
user_input = st.text_area("Enter a story prompt:", "<BOS> Once upon a time, in a galaxy far, far away...")

# Generate and display the story
if st.button("Generate Story"):
    with st.spinner("Generating story..."):
        generated_story = story_gen(user_input, max_length=300, num_return_sequences=1, do_sample=True)[0]['generated_text']
    st.write("Generated Story:")
    st.write(generated_story)

# Footer and acknowledgment
st.sidebar.text("Powered by Hugging Face Transformers")
st.sidebar.markdown("[pranavpsv/gpt2-genre-story-generator](https://huggingface.co/pranavpsv/gpt2-genre-story-generator)")
