# AGENTS.md — AI Agent Instructions

## RESPONSES

- keep your responses concise and to the point unless the user asks for more detail

## PLANNING MODE

- Always ask clarifying questions
- Never assume design, tech stack or features
- Use deep-dive sub-agents to assist with research
- Use deep-dive sub-agents to review the different aspects of your plan before presenting it to the user
- Install skills using the `npx skill add ...` command for tech stacks, libraries, frameworks, and tools we use in the project
- Store plans in md files in `.agents/plans` directory and use them to track progress and changes

## CHANGE / EDIT MODE

- Never implement code yourself when possible - use sub-agents!
- Identify changes from the plan that that can be implemented in parallel and use sub-agents to implement features efficiently
- When using sub-agents to implement features, act as a coordinator only
- Use the best model for the task - premium models for complex tasks (like coding) and mid-tier models for simpler tasks, like documentation
- After completing features (large or small), always run commands like lint, type check and next build to check code quality

## TESTING

- Use any testing tools, libraries available to the project for testing your changes
- Never assume your changes simply work, always test!
- If the project does not have any testing tools, scripts, MCP tools, skills, etc. available for testing, ask the user whether testing should be skipped.

## UI DESIGN

- Always follow the UI design system when creating or reviewing components or pages.
- Design System: @DESIGN.md
