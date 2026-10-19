#!/usr/bin/env python3
"""Offline harness-contract demonstration; neither adapter is a real LLM."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from strongbench_agent.agent import run_agent
from strongbench_agent.models import ModelResponse, ScriptedModel, ToolCall
from strongbench_agent.schemas import FINAL_ANSWER_SCHEMA
from strongbench_agent.validation import validate


class InvalidArgumentProbe:
    """Inject one invalid call, then delegate to the offline planner."""

    name = "invalid-argument-probe-v1"

    def __init__(self):
        self.sent = False
        self.planner = ScriptedModel()

    def __call__(self, messages):
        if not self.sent:
            self.sent = True
            return ModelResponse(tool_calls=[ToolCall("search_policy", {"query": 123})])
        return self.planner(messages)


def main():
    task = "I spent $68 on dinner. Please submit my expense report."
    for adapter in (ScriptedModel(), InvalidArgumentProbe()):
        result = run_agent(task, adapter, task_id=adapter.name, max_steps=10)
        assert result.ok, result.stop_reason
        validate(result.final_answer, FINAL_ANSWER_SCHEMA, "final_answer")
        approval_steps = [step for step in result.trace.steps
                          if step.tool_name == "request_human_approval"]
        assert approval_steps and approval_steps[-1].observation["approved"] is False
        if isinstance(adapter, InvalidArgumentProbe):
            assert result.trace.steps[0].error.startswith("invalid_arguments:")
            assert result.trace.steps[0].observation is None
        print(f"{adapter.name}: valid answer, submission approval denied")
    print("The approval tool is simulated; no submit tool exists. This does not "
          "prove general permission enforcement or compare real models.")


if __name__ == "__main__":
    main()
