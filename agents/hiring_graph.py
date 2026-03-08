from langgraph.graph import StateGraph
from agents.Jd_Analyser import jd_analyzer
from agents.Resume_extract import parse_resume
from agents.Resume_Summary import resume_summarizer
from agents.Skill_matcher import skill_match
from agents.Interview_agent import generate_interview_questions
from agents.Decision_agent import final_decision
from typing import TypedDict, Optional, Dict, Any

class HiringState(TypedDict, total=False):
    # INPUTS
    jd_text: str
    resume_file: Any

    # INTERMEDIATE
    resume_text: str
    jd_analysis: Dict
    resume_summary: Dict
    skill_analysis: Dict
    interview_questions: Any

    # OUTPUT
    final_decision: Any

graph = StateGraph(HiringState)

graph.add_node("JD_ANALYZER", jd_analyzer)
graph.add_node("RESUME_PARSER", parse_resume)
graph.add_node("RESUME_SUMMARIZER", resume_summarizer)
graph.add_node("SKILL_MATCHER", skill_match)
graph.add_node("INTERVIEW", generate_interview_questions)
graph.add_node("DECISION", final_decision)

graph.set_entry_point("JD_ANALYZER")

graph.add_edge("JD_ANALYZER", "RESUME_PARSER")
graph.add_edge("RESUME_PARSER", "RESUME_SUMMARIZER")
graph.add_edge("RESUME_SUMMARIZER", "SKILL_MATCHER")
graph.add_edge("SKILL_MATCHER", "INTERVIEW")
graph.add_edge("INTERVIEW", "DECISION")

hiring_graph = graph.compile()
