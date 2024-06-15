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
    Given the following problem, generate 15 interaction from an average high-school student to solve the problem working with a teacher. Interactions should include, combination of correct and incorrect equations from student and asking for help and clarifications from the teacher to help solve the problem. In the end student should have solved the problem successfully.  
    
    Student input should be either just an equation to be reviewed by the teacher or a request for help. Mark the input with an attribute  “input type” of “equation” or “request for help”.  
    
    If the student input has equations, extract them as an array of equations as “equations” attribute for the interaction.  
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
    A heavy yo-yo of mass $M=1.4 \mathrm{~kg}$ and outer radius $R$ initially sits at rest on a floor and against a wall, as shown.
    A string of negligible mass is wrapped around the yo-yo's axle which has radius $r=0.88 R$.
    The floor and the wall are made of the same material, so the coefficient of static friction between the cylinder and each surface is $\mu_{s}=0.49$.
    What maximum tension force $T$ can the string exert on the cylinder without causing the yo-yo to rotate?  
    """

    arr = [ 
        { 
            "interaction_number": 1, 
            "student_input": "I don't quite understand where to start with this yo-yo problem. Can you help me?", 
            "input_type": "request for help", 
            "teacher_response": "Sure! First, let's identify the forces acting on the yo-yo. What do you think they are?" 
        }, 
        { 
            "interaction_number": 2, 
            "student_input": "Well, there's the weight of the yo-yo, the tension in the string, and friction from the floor and wall.", 
            "input_type": "request for help", 
            "teacher_response": "Correct. Now, let's write down the force equations. What is the force due to gravity?" 
        }, 
        { 
            "interaction_number": 3, 
            "student_input": "The force due to gravity is \( F_g = Mg \).", 
            "input_type": "equation", 
            "equations": ["F_g = Mg"], 
            "teacher_response": "Right. And for \( M = 1.4 \, \text{kg} \) and \( g = 9.8 \, \text{m/s}^2 \), what is \( F_g \)?" 
        }, 
        { 
            "interaction_number": 4, 
            "student_input": "\( F_g = 1.4 \times 9.8 = 13.72 \, \text{N} \).", 
            "input_type": "equation", 
            "equations": ["F_g = 1.4 \times 9.8 = 13.72 \, \text{N}"], 
            "teacher_response": "Good. Now, let's consider the forces from the floor and the wall. What are the static friction forces?" 
        }, 
        { 
            "interaction_number": 5, 
            "student_input": "The static friction forces are \( f_s = \mu_s N \), where \( N \) is the normal force.", 
            "input_type": "equation", 
            "equations": ["f_s = \mu_s N"], 
            "teacher_response": "Yes. Since the yo-yo is in equilibrium, the normal forces from the floor and wall balance the weight and the tension. Can you write the equilibrium conditions for the forces?" 
        }, 
        { 
            "interaction_number": 6, 
            "student_input": "Hmm, let me try. For the vertical forces, \( N_{floor} = F_g \). And for the horizontal forces, \( N_{wall} = T \).", 
            "input_type": "equation", 
            "equations": ["N_{floor} = F_g", "N_{wall} = T"], 
            "teacher_response": "You're on the right track. But remember, there are friction forces too. Let's consider the torque next. How do you express torque?" 
        }, 
        { 
            "interaction_number": 7, 
            "student_input": "Torque is \( \tau = rF \sin(\theta) \).", 
            "input_type": "equation", 
            "equations": ["\tau = rF \sin(\theta)"], 
            "teacher_response": "Correct. Since the yo-yo should not rotate, the net torque must be zero. Can you set up the torque equilibrium equation?" 
        }, 
        { 
            "interaction_number": 8, 
            "student_input": "The torque due to tension is \( \tau_T = T \cdot r \), and the torques due to friction forces are \( \tau_{f, floor} = f_{s, floor} \cdot R \) and \( \tau_{f, wall} = f_{s, wall} \cdot R \).", 
            "input_type": "equation", 
            "equations": ["\tau_T = T \cdot r", "\tau_{f, floor} = f_{s, floor} \cdot R", "\tau_{f, wall} = f_{s, wall} \cdot R"], 
            "teacher_response": "Remember that friction acts at the points of contact. The friction from the floor prevents slipping horizontally, and from the wall, it prevents slipping vertically. Let's refine the torque equation with correct directions." 
        }, 
        { 
            "interaction_number": 9, 
            "student_input": "So, \( \tau_T = T \cdot r \). For the friction forces, \( \tau_{f, floor} = \mu_s N_{floor} \cdot R \) and \( \tau_{f, wall} = \mu_s N_{wall} \cdot R \).", 
            "input_type": "equation", 
            "equations": ["\tau_T = T \cdot r", "\tau_{f, floor} = \mu_s N_{floor} \cdot R", "\tau_{f, wall} = \mu_s N_{wall} \cdot R"], 
            "teacher_response": "Right. Since the normal force from the wall is \( N_{wall} = T \), and from the floor \( N_{floor} = F_g \), plug these into the torque equation." 
        }, 
        { 
            "interaction_number": 10, 
            "student_input": "The torque equilibrium equation is \( T \cdot r = \mu_s F_g \cdot R + \mu_s T \cdot R \).", 
            "input_type": "equation", 
            "equations": ["T \cdot r = \mu_s F_g \cdot R + \mu_s T \cdot R"], 
            "teacher_response": "Excellent. Now substitute \( r = 0.88R \) and simplify the equation." 
        }, 
        { 
            "interaction_number": 11, 
            "student_input": "\( T \cdot 0.88R = \mu_s F_g \cdot R + \mu_s T \cdot R \).", 
            "input_type": "equation", 
            "equations": ["T \cdot 0.88R = \mu_s F_g \cdot R + \mu_s T \cdot R"], 
            "teacher_response": "Good. Now factor out \( R \) and solve for \( T \)." 
        }, 
        { 
            "interaction_number": 12, 
            "student_input": "\( T \cdot 0.88 = \mu_s F_g + \mu_s T \).", 
            "input_type": "equation", 
            "equations": ["T \cdot 0.88 = \mu_s F_g + \mu_s T"], 
            "teacher_response": "That's correct. Substitute \( \mu_s = 0.49 \) and \( F_g = 13.72 \, \text{N} \)." 
        }, 
        { 
            "interaction_number": 13, 
            "student_input": "\( T \cdot 0.88 = 0.49 \times 13.72 + 0.49T \).", 
            "input_type": "equation", 
            "equations": ["T \cdot 0.88 = 0.49 \times 13.72 + 0.49T"], 
            "teacher_response": "Good. Now solve for \( T \)." 
        }, 
        { 
            "interaction_number": 14, 
            "student_input": "\( T \cdot 0.88 - 0.49T = 6.7228 \). So, \( T (0.88 - 0.49) = 6.7228 \).", 
            "input_type": "equation", 
            "equations": ["T \cdot 0.88 - 0.49T = 6.7228", "T (0.88 - 0.49) = 6.7228"], 
            "teacher_response": "Yes. Continue solving for \( T \)." 
        }, 
        { 
            "interaction_number": 15, 
            "student_input": "\( T \cdot 0.39 = 6.7228 \). Therefore, \( T = \frac{6.7228}{0.39} \approx 17.24 \, \text{N} \).", 
            "input_type": "equation", 
            "equations": ["T \cdot 0.39 = 6.7228", "T = \frac{6.7228}{0.39} \approx 17.24 \, \text{N}"], 
            "teacher_response": "Excellent! You've found the maximum tension force without causing the yo-yo to rotate." 
        } 
    ]

    new_arr = gemini_chat(prb_st,arr)