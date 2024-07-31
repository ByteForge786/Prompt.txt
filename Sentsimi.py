import re

past_oriented_words = [
    'yesterday', 'ago', 'before', 'earlier', 'previous', 'last', 'past', 
    'former', 'old', 'ancient', 'historical', 'once', 'formerly', 'initially',
    'originally', 'previously', 'prior', 'bygone', 'elapsed', 'recent',
    'did', 'was', 'were', 'had', 'happened', 'occurred', 'took place'
]

def is_past_question(text):
    text = text.lower()
    words = re.findall(r'\w+', text)
    
    past_score = 0
    
    # Check for past-oriented words
    for word in words:
        if word in past_oriented_words:
            past_score += 1
    
    # Check for past tense verb endings
    past_tense_endings = ['ed', 'd']
    for word in words:
        if any(word.endswith(ending) for ending in past_tense_endings):
            past_score += 0.5
    
    # Check for question starting with 'did'
    if words and words[0] == 'did':
        past_score += 1
    
    # You can adjust this threshold as needed
    return past_score > 0.5

def chatbot_response(user_input):
    if is_past_question(user_input):
        return "It seems you're asking about something from the past."
    else:
        return "Your question doesn't appear to be about the past. How can I help you with current or future matters?"

# Example usage
print(chatbot_response("What happened yesterday?"))
print(chatbot_response("Did you go to the store?"))
print(chatbot_response("Tell me about ancient civilizations."))
print(chatbot_response("What's the weather like today?"))
print(chatbot_response("Will it rain tomorrow?"))
