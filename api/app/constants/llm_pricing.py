BEDROCK_PRICING = {
    # --- Anthropic Models ---
    "us.anthropic.claude-sonnet-4-6": {
        "name": "Claude Sonnet 4.6",
        "input_per_1k": 0.00300,
        "output_per_1k": 0.01500,
        "prompt_cache_read_per_1k": 0.00030,
        "prompt_cache_write_per_1k": 0.00375
    },
    # --- Amazon Models ---
    "amazon.titan-embed-text-v2:0": {
        "name": "Titan Embed Text v2",
        "input_per_1k": 0.00002,
        "output_per_1k": 0.00000,
    },
    # --- Meta Models ---
    "meta.llama3-8b-instruct-v1:0": {
        "name": "Llama 3 8B Instruct",
        "input_per_1k": 0.00022,
        "output_per_1k": 0.00022,
    },
    # --- Anthropic Haiku ---
    "us.anthropic.claude-3-5-haiku-20241022": {
        "name": "Claude 3.5 Haiku",
        "input_per_1k": 0.00080,
        "output_per_1k": 0.00400,
        "prompt_cache_read_per_1k": 0.00008,
        "prompt_cache_write_per_1k": 0.00100,
    },
}