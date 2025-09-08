from fastapi import FastAPI, Depends
from typing import List
from pydantic import BaseModel, Field
from utils.ai_agent import Agent
import json
import re

app = FastAPI()

# Job schema
class Job(BaseModel):
    title: str
    location: str
    company_type: str
    domain: str
    salary: int

# Preference schema (AI-generated)
class JobPreferences(BaseModel):
    role: List[str] = Field(alias="Role")
    salary: List[str] = Field(alias="Salary")
    experience: List[str] = Field(alias="Experience")
    location: List[str] = Field(alias="Location")
    domain: List[str] = Field(alias="Domain")
    company_type: List[str] = Field(alias="Company Type")

    class Config:
        populate_by_name = True

def get_db_session():
    # Will be overridden in tests
    return []

@app.post("/recommendations")
def get_recommendations(
    preferences: JobPreferences,
    db: List[Job] = Depends(get_db_session)
):

    def rank_with_ai(job, user_prefs):

        prompt_job_search = f"""
        You are a ranking agent that scores how well a job posting matches user preferences.

        JOB:
        {job}

        Starting with 0, score this job from 0 to 10 based on how well it matches the preferences. 
        Add +2 to the rank if any keyboards from Role match those of the role of the job. Add +3 if all words from user preferred role match the job.
        Add +3 if the job location corresponds to the one from user preferences.
        Add +2 if a job salary is within user-preferred range.
        Add +1 if a job requires years of experience within user preferred range.
        Add +1 if a job is from the same of similar domain to a user-preference

        Respond with only a number.

        """

        abot_rank = Agent(prompt_job_search)

        response = int(abot_rank(user_prefs))

        return response
    
    database = json.dumps(db, indent=4)
    
    json_strings = re.findall(r'\{.*?\}', database, re.DOTALL)

    parsed_jobs = []
    for obj_str in json_strings:
        try:
            parsed_jobs.append(json.loads(obj_str))
        except json.JSONDecodeError:
            print("Invalid JSON:", obj_str)

    scored_jobs = []

    print(preferences.model_dump_json())

    for job in parsed_jobs:
        rank = rank_with_ai(job, preferences.model_dump_json())
        scored_jobs.append((rank, job))
        job["Resemblance"] = f"{rank} of 10"
        print(job)
        print(rank)

    top_10 = sorted(scored_jobs, key=lambda x: x[0], reverse=True)[:10]
    top_10_jobs = [job for _, job in top_10]

    return top_10_jobs