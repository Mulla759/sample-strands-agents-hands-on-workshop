"""Interactive multi-turn chat for the Recruiter Finder agent.

This is the full "build the harness" assembly from Modules 1-4, pointed at
recruiting instead of customer service:

  - Agent loop + tools      (Module 1)  recruiter_tools.py
  - Hooks                   (Module 2)  hooks.py (SearchBudgetHook)
  - Skills + steering       (Module 3)  skills/ + steering_handlers.py
  - Session manager         (Module 4)  SnapshotSessionManager + LocalFileStorage

The session is persisted to disk, so quit the script and run it again with the
same --session-id and the agent remembers your search and shortlist context.

From the cloned repo root:

    cd samples/recruiter-finder
    pip install -r requirements.txt
    python chat.py                       # uses the default session id
    python chat.py --session-id alice    # resume/keep a named session

Type 'quit', 'exit', or press Ctrl+C to stop.
"""

import argparse

from strands import Agent, AgentSkills
from strands.models import BedrockModel
from strands.session import SnapshotSessionManager
from strands.storage import LocalFileStorage

# AWS-sponsored events / AWS credits: credits only cover Amazon Nova models, not Claude.
# To switch, pass model=BedrockModel(model_id="...") to Agent(...).
# Nova model IDs: https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-amazon.html
#   amazon.nova-micro-v1:0  — fastest, text-only, lowest cost
#   amazon.nova-lite-v1:0   — low-cost, multimodal (text, image, video)
#   amazon.nova-pro-v1:0    — balanced accuracy/speed, multimodal (recommended)
#
# Run locally without AWS credentials using Ollama (https://ollama.com/download):
#   1. Install Ollama and run: ollama pull llama3.1
#   2. pip install strands-agents[ollama]
#   3. Use OllamaModel: from strands.models import OllamaModel
#      model = OllamaModel(host="http://localhost:11434", model_id="llama3.1")
#      agent = Agent(model=model, tools=[...], session_manager=..., system_prompt=...)
#   Other models with tool support: llama3.2, qwen2.5, qwen3, mistral
from hooks import SearchBudgetHook
from recruiter_tools import (
    search_recruiters, get_recruiter_details, get_placements,
    add_to_shortlist, view_shortlist,
)
from steering_handlers import ShortlistWorkflowHandler, tone_handler

SYSTEM_PROMPT = """You are a recruiter-finder agent that helps candidates find and
qualify recruiters, build a shortlist, and draft outreach. Activate the relevant
skill (boolean-sourcing, recruiter-qualification, outreach) for step-by-step guidance.

Important guidelines:
- Search first (search_recruiters), then inspect (get_recruiter_details,
  get_placements), then shortlist (add_to_shortlist) — in that order.
- Qualify before recommending: niche focus, placement volume, response rate.
  Flag red flags instead of pitching weak matches.
- Use the data returned by tools; never invent recruiter details or metrics.
- If there are previous messages in the conversation history, use that context
  to continue without asking the user to repeat information."""


def main():
    parser = argparse.ArgumentParser(description="Multi-turn chat with a persistent recruiter-finder agent.")
    parser.add_argument(
        "--session-id",
        default="recruiter-session-001",
        help="Session id to persist/resume (default: recruiter-session-001).",
    )
    args = parser.parse_args()

    # SnapshotSessionManager persists the whole agent as one atomic blob via the
    # unified Storage backend. Use LocalFileStorage for dev; swap it for
    # S3Storage (strands.storage.S3Storage) in production without other changes.
    # Reusing the same session_id across runs restores the prior conversation.
    session_manager = SnapshotSessionManager(
        session_id=args.session_id,
        storage=LocalFileStorage("./sessions"),
    )

    agent = Agent(
        tools=[
            search_recruiters, get_recruiter_details, get_placements,
            add_to_shortlist, view_shortlist,
        ],
        hooks=[SearchBudgetHook(max_calls=4)],
        plugins=[
            AgentSkills(skills=["./skills"]),
            ShortlistWorkflowHandler(),
            tone_handler,
        ],
        system_prompt=SYSTEM_PROMPT,
        # context_manager="auto" offloads large tool results, compresses old
        # messages into summaries, and fires proactive compression at 85% usage.
        context_manager="auto",
        session_manager=session_manager,
    )

    restored = len(agent.messages)
    print(f"Recruiter finder agent (persistent session: {args.session_id}) - type 'quit' to exit.")
    if restored:
        print(f"Restored {restored} message(s) from a previous session.")
    print("Try: \"Find me recruiters who place backend engineers in fintech.\"")
    print("Then quit and run again - it remembers your search.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Your conversation is saved.")
            break

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye! Your conversation is saved.")
            break
        if not user_input:
            continue

        print("\nAgent: ", end="")
        result = agent(user_input)

        # A steering handler can pause a tool call for human approval (interrupt).
        # Answer each pending interrupt, then resume the agent with the responses.
        while result.stop_reason == "interrupt":
            responses = []
            for interrupt in result.interrupts:
                answer = input(f"\n\nApproval needed ({interrupt.name}): {interrupt.reason}\nApprove? (y/N): ")
                responses.append({
                    "interruptResponse": {
                        "interruptId": interrupt.id,
                        "response": answer.strip().lower() == "y",
                    }
                })
            print("\nAgent: ", end="")
            result = agent(responses)
        print()


if __name__ == "__main__":
    main()
