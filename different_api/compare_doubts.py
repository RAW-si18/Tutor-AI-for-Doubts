# List of Previous Doubts: 

list_sentences = [
    "What is Newton's first law of motion?",
    "How does Newton's first law relate to inertia?",
    "Can you provide examples of objects in motion and at rest according to Newton's first law?",
    "What is Newton's second law of motion?",
    "How do you calculate force using Newton's second law?",
    "Can you explain the concept of mass in relation to Newton's second law?",
    "How does acceleration relate to force and mass in Newton's second law?",
    "What is the difference between mass and weight in the context of Newton's laws?",
    "Can you explain how force affects an object's motion according to Newton's second law?",
    "How does the direction of force affect an object's motion?",
    "What is the unit of force in the International System of Units (SI)?",
    "Can you explain the concept of a net force?",
    "What is Newton's third law of motion?",
    "How do action and reaction forces relate to Newton's third law?",
    "Can you provide examples of action-reaction pairs in everyday life?",
    "Does every action have an equal and opposite reaction?",
    "How does Newton's third law apply to objects in contact and not in contact?",
    "Can you explain the conservation of momentum in the context of Newton's third law?",
    "What is the relationship between force, momentum, and time in Newton's laws?",
    "How do Newton's laws apply to objects in different reference frames?",
    "Can you explain how friction affects motion according to Newton's laws?",
    "What are the different types of friction, and how do they differ?",
    "How does air resistance impact the motion of objects?",
    "Can you explain the concept of terminal velocity?",
    "How do Newton's laws apply to circular motion?",
    "What is centripetal force, and how does it relate to circular motion?  ",
    " Can you explain how satellites stay in orbit using Newton's laws?",
    "How do Newton's laws apply to the motion of planets and celestial bodies?",
    "Can you explain the concept of impulse and momentum in Newton's laws?",
    "What is the relationship between impulse, momentum, and force?",
    "How does the conservation of momentum apply to collisions?",
    "Can you explain the difference between elastic and inelastic collisions?",
    "How does Newton's second law apply to rotational motion?",
    "What is torque, and how does it relate to rotational motion?",
    "Can you explain the concept of angular momentum?",
    "How do Newton's laws apply to the motion of objects on an inclined plane?",
    "Can you derive the equations for motion on an inclined plane using Newton's laws?",
    "How does the angle of inclination affect the motion of objects on a plane?",
    "Can you explain the concept of equilibrium using Newton's laws?",
    "What are the conditions for static equilibrium?",
    "How do forces acting on an object change when it is in dynamic equilibrium?",
    "Can you explain how Newton's laws apply to simple harmonic motion?",
    "What is Hooke's law, and how does it relate to simple harmonic motion?",
    "Can you derive the equations of motion for simple harmonic oscillators using Newton's laws?",
    "How do Newton's laws apply to the motion of fluids?",
    "Can you explain the concept of buoyancy and Archimedes' principle using Newton's laws?",
    "What is viscosity, and how does it affect the motion of fluids?",
    "How do Newton's laws apply to the behavior of gases?",
    "Can you explain how pressure, volume, and temperature relate to the behavior of gases using Newton's laws?",
    "How do Newton's laws apply to the motion of waves and electromagnetic radiation?"
]

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 

def sent_similarity(t_sentence: str,sentences: list):
    '''sentence similarity'''
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    target_sent=model.encode([t_sentence])
    check_sent=model.encode(sentences)
    similarity_scores = cosine_similarity(target_sent, check_sent)
    best_category_index = np.argmax(similarity_scores)
    best_category = sentences[best_category_index]
    match_per=round((list(similarity_scores)[0][best_category_index])*100,2)
    return best_category,match_per

# Check for: 
sent1 = "How does Newton's third law explain the recoil of a gun after firing a bullet?"
sent2 = "Can you provide examples of how Newton's laws apply to the motion of waves in water?"
sent3 = "How does Newton's second law help us understand the behavior of gases in a container?"
best_matched1, per1 = sent_similarity(sent1,list_sentences)
best_matched2, per2 = sent_similarity(sent2,list_sentences)
best_matched3, per3 = sent_similarity(sent3,list_sentences)

print("Sentence 1: ", sent1, "\nBest matched sentence: ", best_matched1, "\nMatch Percentage: ", per1, "%\n\n")
print("Sentence 2: ", sent2, "\nBest matched sentence: ", best_matched2, "\nMatch Percentage: ", per2, "%\n\n")
print("Sentence 3: ", sent3, "\nBest matched sentence: ", best_matched3, "\nMatch Percentage: ", per3, "%\n\n")