import time
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

console = Console()


# 1. This simulates chunks arriving from an API (like OpenAI or Anthropic)
def mock_llm_stream():
    chunks = [
        "# Streaming Demo\n\n",
        "This response is arriving in **real-time** chunk by chunk.\n\n",
        "## Code Highlight\n",
        "```python\n",
        "import ", "rich\n",
        "print(", "'Hello World'", ")\n",
        "```\n\n",
        "### Done!\n",
        "The formatting auto-updates as the Markdown syntax becomes complete."
    ]
    for chunk in chunks:
        time.sleep(0.25)  # Simulate network latency
        yield chunk


# 2. Main loop to catch chunks and update the live console view
full_response = ""

# The 'Live' context manager keeps the terminal screen stable during updates
with Live(Markdown(full_response), console=console, refresh_per_second=10) as live:
    for chunk in mock_llm_stream():
        full_response += chunk

        # Update the live display with the cumulative parsed Markdown
        live.update(Markdown(full_response))
