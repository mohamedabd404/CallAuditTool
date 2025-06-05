def generate_text_report(results, min_flags=6):
    report_blocks = []
    agent_data = group_issues_by_agent(results)

    for agent, data in agent_data.items():
        if len(data["samples"]) < min_flags:
            continue  # Skip agents with < 6 issues

        issues = data["issues"]
        samples = data["samples"]
        summary = summarize_issues(issues)

        block = f"Agent Name: {agent}\nType of Issues:"
        for k, v in summary.items():
            block += f"\n- {k} in {v} calls"

        block += "\n\nDetails about incident:\n"
        for s in samples:
            block += s + "\n"

        block += "\nReported By Team Leader: No"
        block += "\nAction Given: 10% Quality Deduction\n"
        block += "-"*50 + "\n"
        report_blocks.append(block)

    return "\n".join(report_blocks)
