import streamlit as st
from talentscout import llm_client, prompts, conversation, utils
from typing import List

# Initialize session state
conversation.init_session()

st.set_page_config(page_title="TalentScout — Hiring Assistant", layout="wide")

# Sidebar: candidate info form
with st.sidebar:
    st.header("Candidate Details — (fill before chat)")
    name = st.text_input("Full Name", key="name_input")
    email = st.text_input("Email", key="email_input")
    phone = st.text_input("Phone", key="phone_input")
    years = st.number_input("Years of Experience", min_value=0, max_value=50, value=0, step=1, key="exp_input")
    desired = st.text_input("Desired Position(s)", placeholder="e.g., Backend Developer", key="desired_input")
    location = st.text_input("Current Location", key="loc_input")
    tech_raw = st.text_area("Tech Stack (comma separated)", placeholder="e.g., Python, Django, PostgreSQL, React", key="tech_input")
    submit_info = st.button("Save Candidate Info")

    st.markdown("---")
    if st.button("Reset Conversation"):
        conversation.reset_conversation()
        st.rerun()

# Save candidate info to session state when submitted
if submit_info:
    candidate_info = {
        "full_name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "years_experience": int(years),
        "desired_positions": desired.strip(),
        "location": location.strip(),
        "tech_stack": utils.parse_tech_stack(tech_raw)
    }

    # Basic validation
    errors = []
    if candidate_info["full_name"] == "":
        errors.append("Name is required.")
    if not utils.validate_email_address(candidate_info["email"]):
        errors.append("Valid email is required.")
    if not utils.validate_phone_number(candidate_info["phone"]):
        errors.append("Valid phone number is required (digits).")
    if len(candidate_info["tech_stack"]) == 0:
        errors.append("Add at least one technology in Tech Stack.")
    if errors:
        st.sidebar.error(" / ".join(errors))
    else:
        st.session_state.candidate_info = candidate_info
        st.sidebar.success("Candidate info saved.")

st.title("TalentScout — Hiring Assistant")
st.write(prompts.greeting_text())
st.write("")

# Chat area
col1, col2 = st.columns([3, 1])

with col1:
    # Render chat history
    for role, text in st.session_state.messages:
        if role == "assistant":
            st.markdown(f"**Assistant:** {text}")
        else:
            st.markdown(f"**You:** {text}")

    # Input box
    user_input = st.text_input("Type message (or 'done' to finish):", key="user_input")
    send = st.button("Send")

with col2:
    st.subheader("Candidate Summary")
    if st.session_state.candidate_info:
        st.text(prompts.build_candidate_summary(st.session_state.candidate_info))
    else:
        st.info("No candidate info saved. Use the sidebar to add details.")

# Handle sending message
if send and user_input:
    # Save user message
    conversation.add_message("user", user_input)

    # End if keyword
    if conversation.is_end_message(user_input):
        conversation.add_message("assistant", prompts.end_text())
        st.session_state.conversation_active = False

    # Generate questions if user asked
    elif "generate questions" in user_input.lower():
        techs = st.session_state.candidate_info.get("tech_stack", [])
        if not techs:
            conversation.add_message("assistant", "I don't have your tech stack yet. Please add it in the sidebar (Tech Stack) first.")
        else:
            conversation.add_message("assistant", "Generating technical questions — please wait...")
            try:
                qdict = llm_client.generate_questions_via_llm(techs, per_tech=4)
                st.session_state.generated_questions = qdict
                for tech, qs in qdict.items():
                    msg = f"**{tech}**\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(qs)])
                    conversation.add_message("assistant", msg)
            except Exception as e:
                conversation.add_message("assistant", f"Failed to generate via LLM: {e}. Using fallback.")
                qdict = {}
                for tech in techs:
                    qdict[tech] = llm_client.fallback_generate_questions(tech)
                    conversation.add_message("assistant", f"**{tech}**\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(qdict[tech])]))
                st.session_state.generated_questions = qdict
        st.rerun()

    # Otherwise generic reply
    else:
        conversation.add_message(
            "assistant",
            "Thanks — I noted that. If you want me to generate technical questions, type 'generate questions'. "
            "You can also continue the conversation or type 'done' to finish."
        )
    st.rerun()

# If generated questions exist, show them in a tidy panel
if st.session_state.generated_questions:
    st.markdown("---")
    st.subheader("Generated Technical Questions")
    for tech, qs in st.session_state.generated_questions.items():
        with st.expander(tech):
            for i, q in enumerate(qs, start=1):
                st.write(f"{i}. {q}")

# If conversation ended, show closing message
if not st.session_state.conversation_active:
    st.success("Conversation ended. " + prompts.end_text())
