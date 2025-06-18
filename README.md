#  PersonalTask-AiAgent

A local Python-based AI agent that uses Google's Gemini API with function calling to analyze, debug, modify, and run code files — all with a single prompt.

This project demonstrates an LLM-powered development assistant that can:

- Browse your project files
- Read and understand source code
- Fix bugs in Python files
- Run Python scripts
- Write or modify files
- Use iterative reasoning via tool-calling and memory

---

##  Features

- **Function Calling:** Gemini function-calling support for reading, writing, and executing files.
- **Feedback Loop:** An agent that thinks and acts iteratively until a task is done.
- **CLI Input:** Prompt the agent from the command line or via an interactive shell (REPL mode).
- **Verbose Debug Mode:** See token usage, tool call results, and internal agent thinking.

---

##  Example Interaction

```text
User: Please fix the bug in the calculator.
Model: I want to call get_files_info...
Tool: Here's the result of get_files_info...
Model: I want to call get_file_content...
Tool: Here's the result...
...
Model: I fixed the bug and ran the calculator to ensure it works.
