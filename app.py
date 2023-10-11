import streamlit as st
import speech_recognition as sr
import openai

# Set your OpenAI API key here
openai.api_key = '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'

@st.cache_data()
def convert_voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        st.write("Recording complete.")

    try:
        voice_input = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        st.write("Voice input not understood")
    except sr.RequestError as e:
        st.write(f"Could not request results for voice input; {e}")
    
    return voice_input

def story_generator():
    st.title("GenAI Storyteller")

    # Input text to generate a story
    user_input = st.text_area("Enter a text prompt for the story:")

    # Input field for genre
    genre = st.selectbox("Select the story genre:", ["Fantasy", "Science Fiction", "Mystery", "Romance", "Other"])

    # Option to use voice input
    use_voice = st.checkbox("Use voice input")

    if use_voice:
        voice_input = convert_voice_to_text()
        if voice_input:
            st.write("Voice input: " + voice_input)

    # Story length slider
    story_length = st.slider("Select Story Length (Tokens)", min_value=10, max_value=500, value=100)

    # Style and tone selection
    style_tone = st.selectbox("Select Style/Tone:", ["Neutral", "Formal", "Humorous", "Mysterious", "Romantic"])

    @st.cache_data()
    def generate_story():
        if user_input:
            if use_voice and voice_input:
                # Include the selected genre and voice input in the prompt
                prompt = f"Write me a {genre.lower()} story: {voice_input}"
            else:
                # Include the selected genre and text input in the prompt
                prompt = f"Write me a {genre.lower()} story: {user_input}"

            # Customize the prompt based on style/tone
            if style_tone != "Neutral":
                prompt = f"{style_tone} tone: {prompt}"

            # Use GPT-3 to generate the story
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=story_length,
            )
            generated_story = response.choices[0].text
            return generated_story

    if st.button("Generate Story"):
        generated_story = generate_story()
        st.write("Generated Story:")
        st.write(generated_story)
    else:
        st.warning("Please enter a prompt to generate a story")

def about():
    st.title("About GenAI Storyteller")
    st.write("GenAI Storyteller is a Streamlit app that allows you to generate stories using OpenAI's GPT-3.")
    st.write("To use the app:")
    st.write("1. Select 'Story Generator' from the top menu.")
    st.write("2. Enter a text prompt or choose 'Use voice input' to speak your prompt.")
    st.write("3. Select the story genre, style/tone, and story length.")
    st.write("4. Click 'Generate Story' to create a story based on your input.")
    st.write("Feel free to experiment and enjoy generating unique stories!")

# Main app
st.title("GenAI Storyteller")
selected_page = st.selectbox("Menu", ["Story Generator", "About"])

if selected_page == "Story Generator":
    story_generator()
elif selected_page == "About":
    about()
