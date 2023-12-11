import streamlit as st
import openai
import os

# Function to generate stories based on user inputs
def generate_stories(api_key, genre, tone, max_words, prompt, num_stories, purpose):
    # Adjust word count to the nearest 10
    max_words = round(max_words / 10) * 10
    
    # Prompt engineering
    user_prompt = f"Write a {tone} {genre} story, up to {max_words} words: {prompt} for {purpose}"
    
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            engine="text-davinci-003",
            prompt=user_prompt,
            max_tokens=max_words,
            n=num_stories,
            stop=None,
        )
        return [choice.text.strip() for choice in response.choices]
    #except openai.error.OpenAIError as e:
        #print(f"OpenAI API Error: {e}")
        #return [f"Error: {str(e)}"] * num_stories
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"An unexpected error occurred: {e}")
        return [f"Error: An unexpected error occurred."] * num_stories

openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = openai.OpenAI(temperature=0.7, openai_api_key=os.getenv('OPENAI_API_KEY'))

# Streamlit app
st.title("GenAI Story Teller")

# User inputs
api_key = st.secrets["API_KEY"]
#api_key = os.environ.get(API_KEY)
genre = st.selectbox("Select Genre:", ["Sci-Fi", "Mystery", "Fantasy", "Adventure", "Thriller", "Comedy"])
tone = st.selectbox("Select Tone:", ["Positive", "Negative", "Neutral"])
purpose = st.selectbox("Select Purpose:", ["Education", "Storytelling for Children", "Entertainment", "Inspiration"])
max_words = st.slider("Select Maximum Words:", 100, 500, 250, 10)
num_stories = st.slider("Select Number of Stories:", 1, 5, 3, 1)
prompt = st.text_input("Enter Prompt (less than 15 words):")

# Generate stories on button click
if st.button("Generate Stories"):
    if api_key and genre and tone and max_words and prompt and len(prompt.split()) <= 15:
        # Call the generate_stories function
        generated_stories = generate_stories(api_key, genre, tone, max_words, prompt, num_stories, purpose)
        
        # Display generated stories or errors
        for i, story in enumerate(generated_stories):
            st.subheader(f"Generated Story {i + 1} for {purpose}:")
            st.write(story)
    else:
        st.error("Please fill in all fields correctly.")
