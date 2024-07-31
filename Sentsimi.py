from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define reference sentences
reference_sentences = {
    "past_days": [
        "Tell me about yesterday",
        "What happened last week",
        "Events from recent days",
        "Information about the past few days"
    ],
    "past_months": [
        "Tell me about last month",
        "What happened in recent months",
        "Events from the past few months",
        "Information about previous months"
    ],
    "past_years": [
        "Tell me about last year",
        "What happened in past years",
        "Events from years ago",
        "Historical information from previous years"
    ]
}

# Create reference embeddings
reference_embeddings = {
    category: model.encode(sentences) 
    for category, sentences in reference_sentences.items()
}

def identify_time_frame(user_input, threshold=0.6):
    # Encode user input
    input_embedding = model.encode(user_input)
    
    # Calculate similarities
    similarities = {}
    for category, embeddings in reference_embeddings.items():
        category_similarities = [1 - cosine(input_embedding, ref_emb) for ref_emb in embeddings]
        similarities[category] = np.mean(category_similarities)
    
    # Find the most similar category
    best_category = max(similarities, key=similarities.get)
    
    if similarities[best_category] > threshold:
        return best_category
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
print(chatbot_response("What events occurred two days ago?"))
print(chatbot_response("Can you tell me about historical events from a decade ago?"))
print(chatbot_response("What happened in the previous month?"))
