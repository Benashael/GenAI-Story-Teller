import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch 

st.title("GenAI Storyteller")

# Load the pre-trained model and tokenizer
model_name = "mosaicml/mpt-7b-storywriter"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Input text to generate a story
user_input = st.text_area("Enter a text prompt for the story:")

# Maximum word length for the generated story
max_word_length = st.slider("Maximum Word Length for Story", min_value=50, max_value=500, value=250)

# Number of story continuations to generate
num_continuations = st.slider("Number of Story Continuations", min_value=1, max_value=5, value=1)

@st.cache_data()
def generate_stories(prompt, num_continuations, max_word_length):
    generated_stories = []
    for _ in range(num_continuations):
        input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=100, truncation=True)
        generated_story = model.generate(input_ids, max_length=max_word_length * 5, num_return_sequences=1, no_repeat_ngram_size=2)
        generated_text = tokenizer.decode(generated_story[0], skip_special_tokens=True)
        # Trim the generated story to the specified word length
        generated_text = " ".join(generated_text.split()[:max_word_length])
        generated_stories.append(generated_text)
    return generated_stories

if st.button("Generate Story"):
    if user_input:
        generated_stories = generate_stories(user_input, num_continuations, max_word_length)
        # Display the generated stories
        for i, story in enumerate(generated_stories):
            st.subheader(f"Story {i+1}")
            st.write(story)
    else:
        st.warning("Please enter a prompt to generate a story.")

if st.button("Save Story"):
    # Save the generated story to a text file
    if generated_stories:
        with open("generated_story.txt", "w") as file:
            file.write(f"Maximum Word Length: {max_word_length}\n\n")
            for i, story in enumerate(generated_stories):
                file.write(f"Story {i+1}:\n")
                file.write(story)
                file.write("\n\n")
        st.success("Story saved to 'generated_story.txt'")
