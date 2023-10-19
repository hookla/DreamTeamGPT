from loguru import logger

from agents.chairman import Chairman
from agents.sme import SME
from utils.print_with_wrap import print_with_wrap

logger.disable(__name__)


# Initialize

# Create a typical C-suite of executives
# SMEs = [
#     SME("CEO", "Corporate Strategy", ["Market Entry", "Competitive Positioning"]),
#     SME("CFO", "Financial Products", ["Rate Management", "Regulatory Compliance"]),
#     SME("COO", "Operational Efficiency", ["Scalability", "Cost Optimization"]),
#     SME("CMO", "Customer Acquisition", ["Target Market", "Onboarding Experience"]),
#     SME("CTO", "Technical Infrastructure", ["Data Security", "System Integration"]),
#     SME("CRO", "Risk Management", ["Fraud Detection", "Compliance"]),
#     SME("CCO", "Customer Experience", ["UX/UI Design", "Customer Support"]),
#     SME("CPO", "Product Management", ["Feature Rollout", "Customer Feedback"])
# ]

SMEs = [
    #    SME("Elon Musk", "Innovation and Space Exploration", ["Sustainable Energy", "Space Colonization"]),
    SME("Warren Buffett", "Investment and Capital Allocation", ["Value Investing", "Corporate Governance"]),
    SME("Bill Gates", "Software and Philanthropy", ["Global Health", "Education"]),
    SME("Jeff Bezos", "E-commerce and Logistics", ["Supply Chain", "Customer Experience"]),
    SME("Richard Branson", "Diversified Businesses", ["Branding", "Customer Service"]),
    SME("Mark Zuckerberg", "Social Media and Connectivity", ["Data Privacy", "Global Connectivity"]),
    SME("Larry Page", "Search Engines and AI", ["Information Retrieval", "Machine Learning"]),
    SME("Steve Jobs", "Consumer Electronics", ["Product Design", "User Experience"])
]

chairman = Chairman("Chairman", SMEs)


transcript = ["profitable childrens toy for christmas."]

print(transcript)
while not chairman.decide_if_meeting_over(transcript):
    speaker: SME = chairman.decide_next_speaker(transcript)

    opinion = speaker.opinion(transcript)

    print_with_wrap(f"\033[94m{speaker.name}\033[0m: {opinion}")
