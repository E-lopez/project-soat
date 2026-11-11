import asyncio
import random

from app.constants.llm_pricing import BEDROCK_PRICING

default_promt = "You are a helpful assistant designed to extract structured data from legal documents."

async def execute_with_backoff(prompt, primary, secondary, result_type, create_agent_func, system_prompt=default_promt, max_retries=3):
    """
    Executes an agent run with exponential backoff on 503/429 errors.
    Switches to secondary model after retries fail or immediately on specific errors.
    """
    current_model = primary
    
    for attempt in range(max_retries + 1):
        try:
            print(f"Attempt {attempt + 1}: Using primary model")
            agent = create_agent_func(current_model, result_type, system_prompt)
            return await agent.run(prompt)

        except Exception as e:
            error_str = str(e)
            is_retryable = "503" in error_str or "429" in error_str
            
            if not is_retryable or attempt == max_retries:
                if current_model == primary and secondary:
                    print(f"Primary failed. Switching to secondary: {secondary}")
                    current_model = secondary

                    agent = create_agent_func(current_model, result_type, system_prompt)
                    return await agent.run(prompt)
                raise e

            # Exponential Backoff Calculation: 2^attempt + jitter
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"{error_str[:50]}... Retrying in {wait_time:.2f}s")
            await asyncio.sleep(wait_time)


def calculate_cost(model_id: str, input_tokens: int, output_tokens: int, is_cached_read: bool = False) -> float:
    """Calculates model call costs including Anthropic prompt caching discount."""
    model = BEDROCK_PRICING.get(model_id)
    if not model:
        raise ValueError(f"Model ID '{model_id}' is not in the pricing database.")

    if is_cached_read and "prompt_cache_read_per_1k" in model:
        input_rate = model["prompt_cache_read_per_1k"]
    else:
        input_rate = model["input_per_1k"]

    input_cost = (input_tokens / 1000) * input_rate
    output_cost = (output_tokens / 1000) * model["output_per_1k"]
    
    return round(input_cost + output_cost, 6)