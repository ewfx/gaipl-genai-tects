# Can replace with LLM based formatting in the future
# Currently, this is a simple rule-based formatting function

def format_debugging_steps(steps):
    """
    Converts a list of steps into a structured logical debugging flow.
    """
    steps = steps.split(". ")  # Convert into list if needed
    structured_steps = []

    for step in steps:
        if "Check" in step or "Verify" in step:
            structured_steps.append(f"{step}, if issue persists, proceed to the next step.")
        elif "Restart" in step or "Rollback" in step or "Reset" in step:
            structured_steps.append(f"If issue is identified, {step}.")
        elif "Analyze" in step or "Investigate" in step:
            structured_steps.append(f"Investigate the root cause by {step}.")
        else:
            structured_steps.append(step)

    return "\n".join(structured_steps)
