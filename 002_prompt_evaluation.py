from dotenv import load_dotenv
from anthropic import Anthropic
from statistics import mean
import json
import re
import ast
load_dotenv()
client= Anthropic()
model="haiku-4-6"
def add_user_message(messages,text):  # appends a user-role message dict to the messages list
    user_message={
        "role":"user",
        "content":text
    }
    messages.append(user_message)

def chat(messages,system=None,temprature=0.0):  # sends messages to Claude API and returns the text response
    params={
        "model":model,
        "max_tokens":1000,
        "messages":messages,
        "temprature":temprature
    }
    if system:
        params["system"]=system
    response=client.messages.create(**params)
    return response.content[0].text

def add_assistant_message(messages,text):  # appends an assistant-role message dict to the messages list
    assistant_message={
        "role":"assistant",
        "content":text
    }
    messages.append(assistant_message)

def genrate_dataset():  # asks Claude to generate a JSON array of AWS task evaluation cases
    prompt="""
            Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
            that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
            each representing task that requires Python, JSON, or a Regex to complete.

            Example output:
            ```json
            [
                {
                    "task": "Description of task",
                    "format": "json" or "python" or "regex",
                    "solution_criteria":"Key criteria for evaluating the solution"
                },
                ...additional
            ]
            ```

            * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
            * Focus on tasks that do not require writing much code

            Please generate 3 objects.
            """
    message_block=[]
    add_user_message(message_block,prompt)
    add_assistant_message(message_block,"```json")
    text=chat(message_block,stop_sequence=["```"])
    return json.loads(text)

dataset = genrate_dataset

with open("dataset.json","W")as f:
     json.dump(dataset,f,indent=2)

def run_prompt(test_case):  # builds a solve-this-task prompt from test_case and returns Claude's code output
    """merges the prompt and text case input,then returns the result"""
    prompt= f"""Please solve the following task:
    {test_case["task"]}
    * Respond only with Python, JSON, or plain Regex
    * Do not add any comments or commentary or explanation
    """
    message_block=[]
    add_user_message(message_block,prompt)
    add_assistant_message(message_block,"```code")
    output= chat(message_block,stop_sequence=["```"])
    return output


def grade_by_modal(test_case,output):  # uses Claude as a judge to score the solution 1-10 and return strengths/weaknesses/reasoning
    eval_prompt= f"""
        You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

        Original Task:
        <task>
        {test_case["task"]}
        </task>

        Solution to Evaluate:
        <solution>
        {output}
        </solution>

        Criteria you should use to evalutate the solution:
        <criteria>
        {test_case["solution_criteria"]}
        </criteria>


        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10

        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
            """
    message_block=[]
    add_user_message(message_block,eval_prompt)
    add_assistant_message(message_block,"```json")
    eval_text=chat(message_block,stop_sequences=["```"])
    return json.loads(eval_text)

def validate_json(text):  # returns 10 if text is valid JSON, 0 otherwise
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
     return 0

def validate_python(text):  # returns 10 if text is valid Python syntax (via ast.parse), 0 otherwise
    try:
        ast.parse(text.strip())
        return 10
    except SystemError:
        return 0

def validate_regex(text):  # returns 0 if text is an invalid regex pattern, implicitly 10 if valid
    try:
        re.compile(text.strip())
    except re.error:
        return 0
    
def grade_syntax(response,test_case):  # routes to the correct validator (json/python/regex) based on test_case["format"]
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    if format == "python":
        return validate_python(response)
    else :
        return validate_regex(response)


def run_test_case(test_case):  # runs one test case end-to-end: generates output, grades it by model + syntax, returns averaged score

    """calls run_prompt,then grades the result"""
    output = run_prompt(test_case)
    model_grade = grade_by_modal(test_case,output)
    model_score= model_grade["score"]
    reasoning=model_grade["reasoning"]
    syntax_score = grade_syntax(output,test_case)
    score = (model_score + syntax_score)/2
    return{
        "output":output,
        "test_case":test_case,
        "score":score,
        "reasoing":reasoning,
    }

def run_eval(dataset):  # iterates over all test cases, collects results, prints the average score, and returns the full results list
    """Loads the dataset and call run_test_case with each case"""
    results =[]
    for  test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    average_score=mean([result["score"]for result in results])
    print(f"Average score:{average_score}")
    
    return results

with open("dataset.json","r") as f:
    dataset = json.load(f)

results = run_eval(dataset)
print(json.dumps(results,indent=2))