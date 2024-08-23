from typing import Literal
from pydantic import BaseModel

class GPTParsedResume(BaseModel):

    name: str 
    email: str
    phone: str | None
    american: bool | None
    skills: list[str] 
    
    github_url: str | None
    linkedin_url: str | None
    ai_score: int
    ai_score_reasoning: str

    years_experience: int | None
    longest_held_job: int 
    total_number_jobs: int 

class ScoreCard(BaseModel):

    name: str
    email: str
    phone: str
    american: bool | None 

    github: str | None
    linkedin: str | None    

    years_experience: int | None
    hopper_ratio: float | None

    github_activity: float | None
    niches: list[str] | None
    optionals: list[str] | None
    ai_score: int 
    ai_score_reasoning: str

    final_rating: float | None
    status: Literal["pass", "fail"] | None

    resume_path: str | None
    

class Prompts(BaseModel):

    instruction_content: str = """Extract the metadata from the resume contents. \
         The applicant is American if they reside or work primarily in an American city. \
        The applicant's longest held job is the job that they have held for the longest period of time. \
        The ai score requires that you to rate the applicant based on 1) how well you believe they've communicated their abilities and 2) how impressive you find this applicant's background and experiences. \
        Please rate applicants from 1 to 3, with 3 being the highest score. 1 would be for forgettable applicants, 2 for good applicants, and 3 for stellar applicants. \
        The ai score reasoning is the justification you provide for the ai score. Give a two to three sentence justification for your score of the applicant. \
        An example justification would look as follows: "This applicant received a 3 because of their extensive history of exploration and stellar results at Google. They also have a strong ability to manage successful teams and design projects.\
        Return all string values in lower case."""

