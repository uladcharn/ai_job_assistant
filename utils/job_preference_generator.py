from utils.ai_agent import Agent
from utils.jobnova_api_mock import test_my_function_api
import json

prompt = """

You are an experienced job searching agent who helps find jobs based on a candidate request. 
Your task is to collect and understand job seekers' intent based on their job preferences in natural language 
(e.g., 'Looking for a Data Analyst role in the Bay Area at a startup'). You should identify job-related attributes like role, location, salary, domain, 
and experience level and parse this information in JSON file formatted as follows:

{
    "Role": [name(s) of jobs, composed in a list],
    "Salary": [salary for a job, either in a range or by itself (e.g., 100,000 or 80,000-150,000). Default as 50,000-200,000],
    "Experience": [years of experience (e.g., 2, or 1-3, if a range is included). Include 0-10 by DEFAULT if none indicated]
    "Location": [location for the given role that is closest to a user. If a user said something like "Bay Area" or "New England", return job postings for cities relevant to the region],
    "Domain": [the domain of the field. Extract it based on the user-indicated Role by default.],
    "Company Type": [a company type (i.e., Startup, Mid-size, Large, Small Business, etc.). include them all in a list by default if no preference was given],
} - generate every single value for each key in a list. Do not ignore default entrees

ALWAYS ask a user again if you do not understand user prompt. The user should always indicate the job role and their location. 
If you do not see or do not understand user indicating the job location or the job role (or both), ALWAYS GO BACK and ask user again 
by creating a corresponding message. 

"""

abot = Agent(prompt)

def job_search(user_input):

    response = abot(user_input)
    print(response)
    
    if '{' in response:
        response = response[response.find('{'):response.rfind('}')+1]
        new_json = json.loads(response)
        with open('./json_dumps/ai_json.json', "w") as f:
            json.dump(new_json, f, indent=4)

        ### testing an API call 
        top_jobs = test_my_function_api()

        ### Saving jobs

        with open("./json_dumps/top_job_preferences.json", "w") as f:
            json.dump(top_jobs, f, indent=4)

    else:
        return response