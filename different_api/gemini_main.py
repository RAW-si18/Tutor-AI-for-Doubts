import google.generativeai as genai # pip install -q -U google-generativeai

# -----------------------------------------------------------FUNCTION-----------------------------------------------------------
def arr_extraction(arr,i):
    dbt_type = arr[i]["input_type"]
    if dbt_type=='equation':
        input_dbt = arr[i]['equations']
    else:
        input_dbt = arr[i]["student_input"]
    return dbt_type, input_dbt

def empty_teacher_response(arr):
    for i in range(len(arr)):
        arr[i]["teacher_response"] = ""
    return arr

def gemini_chat(prblm_st, arr_interaction):
    model = genai.GenerativeModel('gemini-1.5-flash')
    arr_interaction = empty_teacher_response(arr_interaction)
    chat = model.start_chat(history=[])
    prompt = """
    give your prompt here as per requirement of teacher
    """ 
    input_bot = prompt + '\nProblem Statement: ' + prblm_st
    dbt_type, input_dbt = arr_extraction(arr_interaction,0)
    if dbt_type != 'equation':
        input_dbt = input_bot + '\n' + dbt_type + ": " + input_dbt
    else:
        input_dbt = [input_bot + '\n' + dbt_type + ": "] + input_dbt

    response = chat.send_message(
        input_dbt
        )
    arr_interaction[0]["teacher_response"] = response.text
    print(arr_interaction[0]["interaction_number"],". ",response.text)

    for i in range(1, len(arr_interaction)):
        dbt_type, input_dbt = arr_extraction(arr_interaction,i)

        if dbt_type != 'equation':
            input_dbt = dbt_type + ": " + input_dbt
        else:
            input_dbt = [dbt_type + ": "] + input_dbt

        response = chat.send_message(
            input_dbt
            )
        arr_interaction[i]["teacher_response"] = response.text
        print(arr_interaction[i]["interaction_number"],". ",response.text)
    return arr_interaction

# -----------------------------------------------------------MAIN---------------------------------------------------

if __name__ == "__main__":
    GOOGLE_API_KEY = 'YOUR_API'

    genai.configure(api_key=GOOGLE_API_KEY)
    
    prb_st = r""" 
    A projectile is thrown from a point O on the ground at an angle 45° from the vertical and with a speed of 5 √2 m/s . 
    The projectile at the highest point of its trajectory splits into two equal parts. One part falls vertically down to the ground, 0.5 s after the splitting. 
    The other part, t seconds after the splitting, falls to the ground at a distance x meters from the point O. 
    The acceleration due to gravity g = 10 m/s2 . The value of t is ________.
    """

    arr = [ 
    {
        "interaction_number": 1,
        "student_input": "I'm confused about how to calculate the time of flight of a projectile. Can you explain?",
        "input_type": "request for help",
        "teacher_response": "Sure! To find the time of flight, we start by breaking down the initial velocity into its components. What do you think those components are?"
    },
    {
        "interaction_number": 2,
        "student_input": "The initial velocity has horizontal and vertical components. The horizontal component is \( v_{0x} \) and the vertical component is \( v_{0y} \).",
        "input_type": "response",
        "teacher_response": "Correct. Now, what equation do we use to find the time of flight?"
    },
    {
        "interaction_number": 3,
        "student_input": "Time of flight can be found using \( t = \frac{2v_{0y}}{g} \), assuming no air resistance.",
        "input_type": "equation",
        "equations": ["t = \\frac{2v_{0y}}{g}"],
        "teacher_response": "Exactly. Let's calculate the time of flight for \( v_{0y} = 20 \, \text{m/s} \) and \( g = 9.8 \, \text{m/s}^2 \)."
    },
    {
        "interaction_number": 4,
        "student_input": "The time of flight is \( t = \\frac{2 \\times 20}{9.8} \\approx 4.08 \, \text{s} \).",
        "input_type": "equation",
        "equations": ["t = \\frac{2 \\times 20}{9.8} = 4.08 \\, \\text{s}"],
        "teacher_response": "Good. Now, let's determine the range of the projectile. What formula do we use for range?"
    },
    {
        "interaction_number": 5,
        "student_input": "The range is \( R = v_{0x} \times t \), where \( v_{0x} \) is the horizontal component of the initial velocity.",
        "input_type": "equation",
        "equations": ["R = v_{0x} \\times t"],
        "teacher_response": "Correct. Calculate the range assuming \( v_{0x} = 25 \, \text{m/s} \) and \( t = 4.08 \, \text{s} \)."
    }
    ]

    new_arr = gemini_chat(prb_st,arr)