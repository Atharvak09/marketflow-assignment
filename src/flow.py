from crewai import Agent, Task, Crew, LLM

MODEL_ID = "gemini/gemini-1.5-flash"   
def build_flow(keywords: str, threshold: float) -> Crew:
    model = LLM(model=MODEL_ID)

    researcher = Agent(
        role="News Researcher",
        goal="Find up-to-date, factual information and credible sources about the given keywords.",
        backstory="You scan multiple reputable sources and return concise, verifiable points.",
        llm=model,
        verbose=True,
        memory=False,             
        allow_delegation=False,
    )

    analyzer = Agent(
        role="Relevance Analyzer",
        goal=f"Score each found item for relevance to: {keywords}",
        backstory="You critically evaluate and keep only items above the given threshold.",
        llm=model,
        verbose=True,
        memory=False,
        allow_delegation=False,
    )

    summarizer = Agent(
        role="Summarizer",
        goal="Summarize validated insights clearly with brief source attributions.",
        backstory="You turn the filtered list into a short, readable summary.",
        llm=model,
        verbose=True,
        memory=False,
        allow_delegation=False,
    )

    research_task = Task(
        description=(
            f"Find up-to-date, factual information and credible sources about the given keywords: {keywords}.\n"
            "Return 3–6 bullet points with inline source titles and URLs.\n"
            "Be concise and avoid speculation."
        ),
        expected_output="A bullet list of 3–6 facts with short source titles and URLs.",
        agent=researcher,
    )

    analyze_task = Task(
        description=(
            f"Take the researcher's list and score each line 0–1 for relevance to: {keywords}.\n"
            f"Keep only items with score >= {threshold:.2f}.\n"
            "Return a pruned list with (score) prefix, e.g. (0.78) Fact text — [Source Title](URL)."
        ),
        expected_output="A filtered list of items, each prefixed with a score in parentheses.",
        agent=analyzer,
        context=[research_task],
    )

    summarize_task = Task(
        description=(
            "Create a short final summary (5–10 lines max) of the filtered items. "
            "Keep a simple bullet list with clear, neutral wording. Include brief source attributions."
        ),
        expected_output="A concise bullet summary of validated insights.",
        agent=summarizer,
        context=[analyze_task],
    )

    crew = Crew(
        agents=[researcher, analyzer, summarizer],
        tasks=[research_task, analyze_task, summarize_task],
        process="sequential",
        verbose=True,
    )

    print(f"🔧 Using LLM model: {MODEL_ID}")
    return crew
