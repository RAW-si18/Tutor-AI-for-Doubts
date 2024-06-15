import anthropic # pip install anthropic

api_key = "your_api_key"
client = anthropic.Anthropic(api_key=api_key)
chat_history = []

def empty_teacher_response(arr):
    for i in range(len(arr)):
        arr[i]["teacher_response"] = ""
    return arr

def arr_extraction(arr,i):
    dbt_type = arr[i]["input_type"]
    if dbt_type=='equation':
        input_dbt = arr[i]['equations']
    else:
        input_dbt = arr[i]["student_input"]
    return dbt_type, input_dbt

def add_message(role, content):
    message = {"role": role, "content": content}
    chat_history.append(message)
    
def claude_module(user_dbt):
    add_message("user", user_dbt)

    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=chat_history
    )

    assistant_message = response.content[0].text
    add_message("assistant", assistant_message)

    return assistant_message

def claude_chat(prblm_st, arr_interaction):
    arr_interaction = empty_teacher_response(arr_interaction)

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
        input_dbt = input_bot + '\n' + dbt_type + ": " + repr(input_dbt)

    response = claude_module(input_dbt)
    arr_interaction[0]["teacher_response"] = response

    for i in range(1, len(arr_interaction)):
        dbt_type, input_dbt = arr_extraction(arr_interaction,i)

        if dbt_type != 'equation':
            input_dbt = dbt_type + ": " + input_dbt
        else:
            input_dbt = dbt_type + ": " + repr(input_dbt)

        response = claude_module(input_dbt)
        arr_interaction[i]["teacher_response"] = response
    return arr_interaction

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
    }
]

output = claude_chat(prb_st, arr)
print("[")
for i in output:
    print("\n"+repr(i)+"\n")
print("]")