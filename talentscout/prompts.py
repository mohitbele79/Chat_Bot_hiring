# Stores system and user prompts
"""
Prompt templates and helpers for candidate information collection and graceful messaging.
"""

def greeting_text() -> str:
    return (
        "Hello! I'm TalentScout — an initial screening assistant. "
        "I will collect some basic details and then ask technical questions based on your tech stack. "
        "You can type 'quit', 'exit' or 'done' anytime to end the chat."
    )

def end_text() -> str:
    return "Thanks for your time! We'll share next steps soon. Good luck!"

def build_candidate_summary(candidate_info: dict) -> str:
    """
    Returns a short human-readable summary of provided candidate info.
    """
    lines = []
    lines.append(f"Name: {candidate_info.get('full_name','-')}")
    lines.append(f"Email: {candidate_info.get('email','-')}")
    lines.append(f"Phone: {candidate_info.get('phone','-')}")
    lines.append(f"Experience: {candidate_info.get('years_experience','-')} years")
    lines.append(f"Desired Position(s): {candidate_info.get('desired_positions','-')}")
    lines.append(f"Location: {candidate_info.get('location','-')}")
    tech = candidate_info.get('tech_stack','-')
    if isinstance(tech, list):
        tech = ", ".join(tech)
    lines.append(f"Tech stack: {tech}")
    return "\n".join(lines)
