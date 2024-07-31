import nltk
from nltk import word_tokenize, pos_tag
from datetime import datetime

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_time_indicators(text):
    tokens = word_tokenize(text.lower())
    tagged = pos_tag(tokens)
    
    time_indicators = {
        'days': 0,
        'months': 0,
        'years': 0
    }
    
    for i, (word, tag) in enumerate(tagged):
        if tag == 'CD':  # Cardinal number
            if i + 1 < len(tagged):
                next_word = tagged[i+1][0]
                if 'day' in next_word:
                    time_indicators['days'] += 1
                elif 'month' in next_word:
                    time_indicators['months'] += 1
                elif 'year' in next_word:
                    time_indicators['years'] += 1
        elif word in ['yesterday', 'today', 'tomorrow']:
            time_indicators['days'] += 1
        elif word in ['week', 'weekly']:
            time_indicators['days'] += 0.5
        elif word in ['month', 'monthly']:
            time_indicators['months'] += 1
        elif word in ['year', 'yearly', 'annual']:
            time_indicators['years'] += 1
        elif word in ['recent', 'recently', 'latest']:
            time_indicators['days'] += 0.5
            time_indicators['months'] += 0.3
        elif word in ['past', 'previous', 'last', 'ago']:
            time_indicators['days'] += 0.3
            time_indicators['months'] += 0.3
            time_indicators['years'] += 0.3
    
    return time_indicators

def identify_time_frame(user_input):
    indicators = extract_time_indicators(user_input)
    max_indicator = max(indicators, key=indicators.get)
    
    if indicators[max_indicator] > 0:
        return f"past_{max_indicator}"
    else:
        return "not_specified"

def chatbot_response(user_input):
    time_frame = identify_time_frame(user_input)
    
    if time_frame == "past_days":
        return "It seems you're asking about something in the past few days."
    elif time_frame == "past_months":
        return "You appear to be inquiring about something from the past few months."
    elif time_frame == "past_years":
        return "I understand you're asking about something from past years."
    else:
        return "I'm not sure about the time frame you're referring to. Could you please be more specific?"

# Example usage
print(chatbot_response("What happened two days ago?"))
print(chatbot_response("Tell me about events from last year"))
print(chatbot_response("Any interesting news from recent months?"))
print(chatbot_response("What's the weather like?"))
