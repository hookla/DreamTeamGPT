from agents.chairman import Chairman
from agents.sme import SME
from utils.print_with_wrap import print_with_wrap

# Initialize

# Create a typical C-suite of executives
SMEs = [
    SME("CEO", "Corporate Strategy", ["Market Entry", "Competitive Positioning"]),
    SME("CFO", "Financial Products", ["Rate Management", "Regulatory Compliance"]),
    SME("COO", "Operational Efficiency", ["Scalability", "Cost Optimization"]),
    SME("CMO", "Customer Acquisition", ["Target Market", "Onboarding Experience"]),
    SME("CTO", "Technical Infrastructure", ["Data Security", "System Integration"]),
    SME("CRO", "Risk Management", ["Fraud Detection", "Compliance"]),
    SME("CCO", "Customer Experience", ["UX/UI Design", "Customer Support"]),
    SME("CPO", "Product Management", ["Feature Rollout", "Customer Feedback"])
]

chairman = Chairman("Chairman", SMEs)


transcript = ["profitable childrens toy for christmas."]

print(transcript)
while not chairman.decide_if_meeting_over(transcript):
    speaker: SME = chairman.decide_next_speaker(transcript)

    opinion = speaker.opinion(transcript)

    print_with_wrap(f"\033[94m{speaker.name}\033[0m: {opinion}")
