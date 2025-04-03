from __future__ import annotations as _annotations
from dataclasses import dataclass
import pydantic_core
import asyncpg
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI


from src.db.db import db , openai_client


@dataclass
class Deps:
    pool: asyncpg.Pool
    openai: AsyncOpenAI


# Initialize the agent
model = OpenAIModel("gpt-4o")
rag_agent = Agent(model, deps_type=Deps)
    

@rag_agent.tool
async def retrieve(context: RunContext[Deps], search_query: str) -> str:
    """Retrieve documentation sections based on a search query.

    Args:
        context: The call context.
        search_query: The search query.
    """
    print("Retrieving..............")
    embedding = await context.deps.openai.embeddings.create(
            input=search_query,
            model='text-embedding-3-small',
        )
    
    assert (
        len(embedding.data) == 1
    ), f'Expected 1 embedding, got {len(embedding.data)}, doc query: {search_query!r}'
    
    embedding = embedding.data[0].embedding
    embedding_json = pydantic_core.to_json(embedding).decode()
    rows = await context.deps.pool.fetch(
        'SELECT chunk FROM text_chunks ORDER BY embedding <-> $1 LIMIT 5',
        embedding_json,
    )
    from_db = '\n\n'.join(
    f'# Chunk:\n{row["chunk"]}\n'
    for row in rows
    ) 
    return from_db

async def run_agent(question: str):
    """Entry point to run the agent and perform RAG-based question answering."""
    # Set up the agent and dependencies

    pool = await db.connect(create_tables=False)

    deps = Deps(openai=openai_client, pool=pool)
    prompt = f"Use the 'retrieve' tool to fetch information to help you answer this question: {question}"
    
    answer = await rag_agent.run(prompt, deps=deps)
        
    return answer.data