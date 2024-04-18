from flask import Flask, request, send_from_directory, jsonify
import spacy
import random
from fuzzywuzzy import fuzz
import string

app = Flask(__name__, static_url_path='/static', static_folder='static')
nlp = spacy.load("en_core_web_sm")

# Greeting patterns
greeting_patterns = ["hello", "hi", "hii", "hey", "howdy"]

# Define responses for greetings
greeting_responses = [
    "Welcome! I'm here to assist you with any questions you have.",
    "Hello! How can I help you today?",
    "Hi there! Feel free to ask me anything you'd like to know.",
    "Greetings! I'm here to provide assistance. What can I do for you?"
]

# Define a list of questions and their corresponding answers
question_answers = {
    "What is your name?": "I am a Mira.",
    "How are you?": "I'm a fine, but thanks for asking!",
    "What is the weather today?": "I'm sorry, I cannot provide weather information at the moment.",
    "Why did i pick to attend this college?": "You choose to attend MCE because of its outstanding academic programs, vibrant campus life, and strong industry connections, all of which align perfectly with your educational and career goals."
}
# Function to answer questions based on pre-defined answers
def answer_question(question):
    # Process the question using spaCy
    question_doc = nlp(question)

    # Initialize variables to store the best match and its similarity score
    best_match = None
    best_similarity = 0

    # Iterate over the predefined questions and find the best match
    for key_question, answer in question_answers.items():
        similarity = fuzz.partial_ratio(question.lower(), key_question.lower())
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = answer

    # If a match with sufficient similarity is found, return the corresponding answer
    if best_similarity > 80:  # Adjust the similarity threshold as needed
        return best_match
    # If the question matches the specific query about ATL Marathon eligibility
    if "can participate in atl marathon?" in question.lower():
        return "Students from both ATL and Non-ATL schools are eligible to participate. Non-ATL schools can collaborate with ATL schools to form teams."
    
    if "rewards for the top teams?" in question.lower():
        return "The top teams will receive internships through the Student Innovator Program with leading corporates of India, certificates from AIM, NITI Aayog, and many more interesting opportunities at the conclusion of the Marathon."
    if "deadline for submitting entries?" in question.lower():
        return "The last date to submit entries is 26th January 2024, 11:59 PM."
    if "submit the application for the atl marathon?" in question.lower():
        return "You can submit your application in your student profile."
    if "participating students receive a certificate?" in question.lower():
        return "Yes, all participating students will receive a certificate of Participation from AIM, NITI Aayog."
    if "a team submit entries for more than one problem statement?" in question.lower():
        return "Yes, a team may submit entries for more than one problem statement. However, a separate application form must be filled out for each problem statement."
    if "limit on the number of teams that can participate from a school?" in question.lower():
        return "No, there is no limit. Maximum number of teams from every school is encouraged."
    if "documents are required for online application aubmission?" in question.lower():
        return "The online application form submission will include a Research Document (description of the innovation/solution) and a Video submission (capturing a 360-degree view of the working prototype/solution)."
    if "provide support to the student teams?" in question.lower():
        return "ATL In-Charge, School Teachers, Mentors of Change, Alumni, and external mentors from the local ATL ecosystem may support the student teams."
    if "ideal composition of a team?" in question.lower():
        return "Each team should consist of a maximum of 3 students (class 6th to 12th). ATL schools are encouraged to include other school and/or community students in the team composition."
    if "individual member entry allowed?" in question.lower():
        return "No, individual member entry is not allowed. Teams must consist of a minimum of 2 members."
    if "special certificates for schools with a high number of participating teams?" in question.lower():
        return "Yes, special certificates from AIM, NITI Aayog will be given to all schools that have more than 25 teams participating in ATL Marathon."
    
    
    
    

    # If no matching question is found, return a default response
    return "I'm sorry, I don't have an answer to that question."

def recognize_intent(user_input):
    # Remove punctuation from the user input
    user_input_cleaned = user_input.translate(str.maketrans('', '', string.punctuation))
    doc = nlp(user_input_cleaned.lower())

    # Check if the user input contains a greeting
    for token in doc:
        if token.text in greeting_patterns:
            return "greeting"
        
         # Check if the user input is a question
    if user_input.endswith("?"):
        return "question"
    
        
    # Check if the user input indicates the admission intent
    if "admission" in user_input_cleaned.lower() or "admission form" in user_input_cleaned.lower():
        return "admission"
    
    # Check if the user input indicates the course intent
    if "course" in user_input_cleaned.lower() or "programme" in user_input_cleaned.lower():
        return "course"

    # Default intent
    return "unknown"





# Function to generate response based on recognized intent
def generate_response(intent, user_input):
    if intent == "greeting":
        return random.choice(greeting_responses), intent
    if intent == "question":
        if user_input in question_answers:
            return question_answers[user_input]
        else:
            return "I'm sorry, I don't have an answer to that question."

    
    # If the intent is unknown
    return "I'm sorry, I didn't understand that. Can you please rephrase your word?", intent

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        data = request.json
        user_input = data['message']

        if user_input.lower() == 'greeting':
            response = random.choice(greeting_responses)
            intent = 'greeting'
        else:
            intent = recognize_intent(user_input)
            if intent == "question":
                response = answer_question(user_input)
            else:
                response, _ = generate_response(intent, user_input)

        return jsonify({'response': response, 'intent': intent})

    return jsonify({'error': 'Method Not Allowed'}), 405

if __name__ == "__main__":
    app.run(debug=True)
