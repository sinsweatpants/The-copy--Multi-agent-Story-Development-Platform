from typing import List, Dict, Any, Tuple

from app.schemas.creative_brief import CreativeBrief
from app.schemas.idea import Idea
from app.schemas.review import Review
from app.schemas.tournament import TournamentTurn

# A centralized repository for prompt engineering.
# This module creates tailored, context-aware prompts for each agent and phase.

def _format_brief(brief: CreativeBrief) -> str:
    """Formats the creative brief into a string for inclusion in prompts."""
    characters = "\n".join([f"- {char.name}: {char.description}" for char in brief.main_characters])
    themes = ", ".join(brief.themes)
    return f"""
    **Creative Brief:**
    - **Core Idea:** {brief.core_idea}
    - **Genre:** {brief.genre}
    - **Target Audience:** {brief.target_audience}
    - **Main Characters:**
    {characters}
    - **Themes:** {themes}
    - **Constraints & Preferences:** {brief.constraints}, {brief.preferences}
    """

def _format_idea(idea: Idea, idea_label: str) -> str:
    """Formats a single idea into a detailed string."""
    return f"""
    **--- {idea_label} ---**
    **Title:** {idea.title}
    **Logline:** {idea.logline}
    **Synopsis:**
    {idea.synopsis}
    **Three-Act Structure:**
    - Act 1: {idea.three_act_structure.get('act_1', 'N/A')}
    - Act 2: {idea.three_act_structure.get('act_2', 'N/A')}
    - Act 3: {idea.three_act_structure.get('act_3', 'N/A')}
    **Key Scenes:**
    {idea.key_scenes}
    **Main Characters:**
    {idea.main_characters}
    """

def create_story_prompt(brief: CreativeBrief, num_variations: int) -> str:
    """
    Creates a prompt for the Story Architect agent to generate initial story structures.
    """
    brief_str = _format_brief(brief)
    return f"""
    As the Story Architect, your task is to generate {num_variations} distinct and compelling story structures based on the provided creative brief.

    For each variation, you must provide:
    1.  **Title:** A working title for the story.
    2.  **Logline:** A single sentence that summarizes the entire story.
    3.  **Synopsis:** A detailed summary (300-500 words) covering the main plot points.
    4.  **Three-Act Structure:** A breakdown of the story into three acts (Setup, Confrontation, Resolution).
    5.  **Key Scenes:** A list of 5-7 pivotal scenes that define the narrative arc.
    6.  **Thematic Elements:** How the story explores the specified themes.
    7.  **Unique Selling Points:** What makes this story concept unique and marketable.

    {brief_str}

    Generate the {num_variations} variations in a structured format. Be creative and ensure the ideas are fundamentally different in their approach to the core concept.
    """

def create_character_enhancement_prompt(story_structure: Dict[str, Any], brief: CreativeBrief) -> str:
    """
    Creates a prompt for the Character Development agent to flesh out characters for a given story structure.
    """
    brief_str = _format_brief(brief)
    story_str = f"""
    **Story Structure to Enhance:**
    - **Title:** {story_structure.get('title')}
    - **Logline:** {story_structure.get('logline')}
    - **Synopsis:** {story_structure.get('synopsis')}
    """
    return f"""
    As the Character Development Agent, your task is to enhance the provided story structure by creating rich, detailed profiles for the main characters.

    Based on the creative brief and the specific story structure below, develop compelling character arcs, motivations, and internal conflicts.

    {brief_str}

    {story_str}

    For each main character mentioned in the brief, provide:
    1.  **Full Name & Archetype:**
    2.  **Motivations (Internal & External):**
    3.  **Core Conflict:**
    4.  **Character Arc:** How do they change from the beginning to the end of the story?
    5.  **Relationship to Other Characters:**

    Integrate these developed characters seamlessly into the provided story structure.
    """

def create_review_prompt(agent_guide: str, ideas: Tuple[Idea, Idea], brief: CreativeBrief) -> str:
    """
    Creates a detailed review prompt for a specialist agent.
    """
    brief_str = _format_brief(brief)
    idea1_str = _format_idea(ideas[0], "Idea A")
    idea2_str = _format_idea(ideas[1], "Idea B")

    return f"""
    **Your Role:** You are a specialist agent tasked with conducting an independent and critical review of two competing story ideas. Your analysis must be based on your specific area of expertise, as defined in your guide.

    **Your Agent Guide:**
    {agent_guide}

    **The Creative Brief (The project's goal):**
    {brief_str}

    **The Two Competing Ideas:**
    {idea1_str}
    {idea2_str}

    **Your Task:**
    Provide a structured review for BOTH Idea A and Idea B. For each idea, you must provide the following, strictly from the perspective of your agent guide:

    1.  **Quality Analysis:**
        - **Score (0-10):**
        - **Justification:**
    2.  **Novelty Analysis:**
        - **Score (0-10):**
        - **Justification:**
    3.  **Impact Analysis:**
        - **Score (0-10):**
        - **Justification:**
    4.  **Strengths:** (List of bullet points)
    5.  **Weaknesses:** (List of bullet points)
    6.  **Recommendations for Improvement:** (List of bullet points)
    7.  **Overall Verdict:** A concise summary of your assessment.

    Finally, provide a **Comparative Analysis** where you directly compare Idea A and Idea B and state which one you believe is superior according to your expertise and why.
    """

def create_tournament_argument_prompt(
    agent_guide: str,
    own_review: Dict[str, Any],
    previous_turns: List[TournamentTurn]
) -> str:
    """
    Creates a prompt for an agent to generate an argument during the tournament.
    """
    review_str = f"**Your Own Previous Review:**\n{own_review}"

    turns_str = ""
    if previous_turns:
        turns_str = "**Previous Arguments in the Debate:**\n"
        for turn in previous_turns:
            turns_str += f"**Turn {turn.turn_number}:**\n"
            for arg in turn.arguments:
                turns_str += f"- **{arg.agent_name} argued for Idea {arg.supporting_idea}:** '{arg.specialized_insight}'\n"

    return f"""
    **Your Role:** You are participating in a competitive tournament of minds. Your goal is to argue effectively for the idea you believe is superior, based on your expertise and your previous review.

    **Your Agent Guide:**
    {agent_guide}

    {review_str}

    {turns_str}

    **Your Task:**
    Formulate a compelling argument. You can choose to:
    - **Reinforce your position:** Provide new evidence or a deeper insight from your specialty to support your preferred idea.
    - **Rebut an opponent:** Directly challenge an argument made by another agent in a previous turn, explaining why their reasoning is flawed from your perspective.
    - **Shift your stance:** If a previous argument has convinced you, you may change your preferred idea, but you must provide a strong justification for this change.

    Your argument must be structured as follows:
    1.  **Supporting Idea:** State clearly if you are arguing for Idea 1 or Idea 2.
    2.  **Strengths Highlighted:** Key strengths of your chosen idea.
    3.  **Weaknesses Criticized:** Flaws in the opposing idea.
    4.  **Specialized Insight:** The core of your argument, from your unique perspective.
    5.  **Rebuttal (Optional):** If you are directly challenging a previous argument, state it here.
    """

def create_final_decision_prompt(
    tournament_turns: List[TournamentTurn],
    agent_reviews: Dict[str, Any],
    winning_idea: Idea
) -> str:
    """
    Creates a prompt for the Master Orchestrator to generate the final report.
    """
    # This is a simplified representation. A real implementation would be more detailed.
    reviews_summary = "\n".join([f"- {agent}: {review['overall_verdict']}" for agent, review in agent_reviews.items()])

    return f"""
    As the Master Orcheator, your task is to synthesize the entire session and generate a final, comprehensive report.

    **Winning Idea:**
    {_format_idea(winning_idea, "Winning Idea")}

    **Agent Reviews Summary:**
    {reviews_summary}

    **Tournament Transcript:**
    {tournament_turns}

    **Your Task:**
    Generate a final decision report that includes:
    1.  **Decision Rationale:** A clear and detailed explanation of why the winning idea was chosen. Synthesize the key arguments from the tournament.
    2.  **Key Strengths:** The most compelling strengths of the winning idea.
    3.  **Addressed Weaknesses:** How potential weaknesses in the winning idea were acknowledged and can be mitigated.
    4.  **Implementation Recommendations:** Actionable next steps for developing this idea further.
    """