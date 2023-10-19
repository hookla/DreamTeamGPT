from agents.chairman import Chairman
from agents.executive import Executive
from agents.secretary import Secretary
from utils.pretty_print_with_wrap import pretty_print_with_wrap
from utils.token_counter import num_tokens_from_messages

# Initialize

# Create a typical C-suite of executives
executives = [
    Executive("CEO", "Strategy", ["Growth", "Profitability"]),
    Executive("CFO", "Finance", ["Cash Flow", "Budget"]),
    Executive("COO", "Operations", ["Efficiency", "Productivity"]),
    Executive("CMO", "Marketing", ["Brand", "Customer Acquisition"]),
    Executive("CTO", "Technology", ["Innovation", "Security"])
]

chairman = Chairman("Chairman Name", executives)
secretary = Secretary("Secretary Name")

minutes = ["todo"]

transcript = [
    "Our new product will enable banks to offer customers instant access saving accounts at rates close to the fixed deposit rate. the objective of this meeting is to explore how we can make that happen."]

# Token limit
TOKEN_LIMIT = 1000

print(transcript)
# Meeting Loop
while not chairman.decide_if_meeting_over(minutes, transcript):

    next_speaker: Executive = chairman.decide_next_speaker(minutes, transcript)

    opinion = next_speaker.opinion(minutes, transcript)
    if num_tokens_from_messages([{"content": opinion}]) + num_tokens_from_messages(
            [{"content": " ".join(transcript)}]) <= TOKEN_LIMIT:
        transcript.append(f"{next_speaker.name}: {opinion}")

    pretty_print_with_wrap(f"\033[94m{next_speaker.name}\033[0m: {opinion}")
