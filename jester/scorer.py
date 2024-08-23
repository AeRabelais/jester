import requests
from jester.prompts import GPTParsedResume, ScoreCard
from jester.settings import settings

def create_scorecard(parsed_resume: GPTParsedResume, resume_path: str, contents: str, num_pages: int) -> ScoreCard:
    
    score_card = {
        "name": parsed_resume.name,
        "email": parsed_resume.email,
        "phone": parsed_resume.phone,
        "american": parsed_resume.american,
        "github": parsed_resume.github_url,
        "linkedin": parsed_resume.linkedin_url,
        "years_experience": parsed_resume.years_experience,
        "ai_score": parsed_resume.ai_score,
        "ai_score_reasoning": parsed_resume.ai_score_reasoning,
        "hopper_ratio": None,
        "github_activity": None,
        "niches": None,
        "optionals": None,
        "final_rating": None,
        "status": None,
        "fail_reason": None,
        "resume_path": None,
    }

    score_card["hopper_ratio"] = hopper_ratio(parsed_resume.longest_held_job, parsed_resume.total_number_jobs)
    score_card["github_activity"] = has_active_github(parsed_resume.github_url)
    score_card["niches"] = find_niches(skills=parsed_resume.skills)
    score_card["is_catgirl"] = "rust" in parsed_resume.skills
    score_card["optionals"] = find_optionals(skills=parsed_resume.skills)

    status, fail_reason = get_pass_status(score_card, contents, num_pages)

    score_card["status"] = status
    score_card["fail_reason"] = fail_reason

    if status == "pass":
        score_card["final_rating"] = calculate_final_rating(score_card)

    score_card["resume_path"] = resume_path

    return score_card
    

def hopper_ratio(longest_held_job: int, total_number_jobs: int) -> float:
    
    return longest_held_job / total_number_jobs

def find_niches(skills: list[str]) -> list[str]:  
    
    niches = skills - settings.popular_languages

    return niches

def find_optionals(skills: list[str]) -> list[str]:
    
    optionals = []
    for skill in skills:
        if skill in settings.optional_skills:
            optionals.append(skill)

    return optionals

def get_pass_status(score_card: dict, contents: str, num_pages: int) -> bool:
    # Check for the mandatory skills.
    for skill in settings.mandatory_skills:
        if skill not in contents:
            return "fail", f"Missing mandatory skill: {skill}"
        
    # Check located in America
    if not score_card["american"]:
        return "fail", f"Applicant is not located in America."
    
    # Check that Github is provided.
    if score_card["github"] is None:
        return "fail", f"Github URL is missing."
    
    # If the number of resume pages is over 2.
    if num_pages > 2:
        return "fail", f"Resume is too long."
    
    return "pass"


def calculate_final_rating(score_card: dict) -> float:
    
    # AI Score
    final_score = score_card["ai_score"]

    # Hopper Ratio
    if score_card["hopper_ratio"] < 1:
        final_score -= 1
    else:
        final_score += 1

    # GitHub Activity
    if score_card["github_activity"]:
        final_score += 2

    # Niches
    if len(score_card["niches"]) > 0:
        final_score += 1
    
    # Optionals
    if len(score_card["optionals"]) > 0:
        final_score += ( len(score_card["optionals"]) * 0.5 )
    
    # Catgirl
    if score_card["is_catgirl"]:
        final_score += 0.5

    return final_score
    

def has_active_github(github_url: str) -> bool:
    # Extract the username from the URL
    if "github.com" not in github_url:
        raise ValueError("Invalid GitHub URL")
    username = github_url.split("github.com/")[1]
    if "/" in username:
        username = username.split("/")[0]
    
    # Define the GitHub API endpoint for user events
    api_url = f"https://api.github.com/users/{username}/events/public"
    
    # Make a request to the GitHub API
    response = requests.get(api_url)
    if response.status_code != 200:
        return f"Failed to fetch data: {response.status_code}"
    
    events = response.json()
    event_count = len(events)  # Count the number of events in the response
    
    return event_count > 200





