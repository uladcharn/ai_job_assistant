import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
from utils.job_preference_generator import job_search

st.title("Job Recommendation System")
st.header("This chatbot assists you in searching jobs ")

user_query = st.text_area("Enter your search here")

if st.button("Search"):
    resp = job_search(user_query)

    if resp is None:

        with open('./json_dumps/ai_json.json', 'r') as f:
            ai_jobs = json.load(f)

        st.title("You are looking for:")

        for key in ai_jobs.keys():
            all_items = ', '.join(ai_jobs[key])
            if all_items is None:
                all_items = "No preference"
            st.write(f"**{key}**: {all_items}")

        with open('./json_dumps/top_job_preferences.json', 'r') as f:
            ai_recommendations = json.load(f)

        st.title("Jobs found:")

        st.divider()

        for rec in ai_recommendations:
            for key in rec.keys():
                if key == "title":
                    st.header(rec[key])
                else:
                    st.write(f"**{key.capitalize()}**: {rec[key]}")
            st.divider()
            

    else:
        st.write(resp)

