"""AgentCore entrypoint for the Recruiter Finder agent (Module 5 pattern).

Deploys the same harness built in chat.py to Amazon Bedrock AgentCore Runtime,
where memory, identity, and observability are managed for you.

Deploy (see the module-05 README / notebook for the full walkthrough):

    sudo npm install -g @aws/agentcore@1.0.1 --ignore-scripts
    agentcore create --name recruitfind --template empty
    cd recruitfind && agentcore add runtime --name RecruitFind --language python
    # copy main.py, recruiter_tools.py, steering_handlers.py, hooks.py,
    # and skills/ into app/RecruitFind/, then uv init --bare + uv add
    agentcore deploy
    agentcore invoke --runtime RecruitFind \
      --payload '{"prompt": "Find recruiters who place data scientists in health tech"}'
"""

import json
import logging
import os
from strands import Agent, AgentSkills
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from hooks import SearchBudgetHook
from recruiter_tools import (
    search_recruiters, get_recruiter_details, get_placements,
    add_to_shortlist, view_shortlist,
)
from steering_handlers import ShortlistWorkflowHandler, tone_handler

logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

SYSTEM_PROMPT = """You are a recruiter-finder agent that helps candidates find and
qualify recruiters, build a shortlist, and draft outreach. Activate the relevant
skill (boolean-sourcing, recruiter-qualification, outreach) for step-by-step guidance.

Important guidelines:
- Search first (search_recruiters), then inspect (get_recruiter_details,
  get_placements), then shortlist (add_to_shortlist) — in that order.
- Qualify before recommending: niche focus, placement volume, response rate.
  Flag red flags instead of pitching weak matches.
- Use the data returned by tools; never invent recruiter details or metrics."""

_agent = None
_pending_interrupts = []

def get_agent():
    global _agent
    if _agent is None:
        _agent = Agent(
            tools=[
                search_recruiters, get_recruiter_details, get_placements,
                add_to_shortlist, view_shortlist,
            ],
            hooks=[SearchBudgetHook(max_calls=4)],
            plugins=[
                AgentSkills(skills=[os.path.join(os.path.dirname(__file__), "skills")]),
                ShortlistWorkflowHandler(),
                tone_handler,
            ],
            system_prompt=SYSTEM_PROMPT,
            context_manager="auto",
        )
    return _agent


def interrupt_response(interrupts):
    """Describe the tool calls waiting for human approval so the caller can answer them."""
    return {
        "status": "interrupted",
        "interrupts": [
            {"interruptId": interrupt.id, "name": interrupt.name, "reason": interrupt.reason}
            for interrupt in interrupts
        ],
    }


@app.entrypoint
def invoke(payload, context):
    global _pending_interrupts
    agent = get_agent()

    # Resume a paused invocation: {"interrupt_responses": [{"interruptId": "...", "response": true}]}
    interrupt_responses = payload.get("interrupt_responses")
    if interrupt_responses:
        result = agent([{"interruptResponse": response} for response in interrupt_responses])
    else:
        raw_prompt = payload.get("prompt")
        try:
            parsed = json.loads(raw_prompt)
            prompt = parsed.get("prompt", raw_prompt)
        except (TypeError, json.JSONDecodeError):
            prompt = raw_prompt

        if not prompt:
            raise ValueError("Missing required field: prompt")

        # The agent can't take a new prompt until the pending interrupts are answered
        if _pending_interrupts:
            return interrupt_response(_pending_interrupts)

        result = agent(prompt)

    # A steering handler paused a tool call for human approval
    if result.stop_reason == "interrupt":
        _pending_interrupts = list(result.interrupts)
        return interrupt_response(_pending_interrupts)

    _pending_interrupts = []
    return str(result).strip()


if __name__ == "__main__":
    app.run()
