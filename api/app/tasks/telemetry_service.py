import time
from typing import Any, Generator, Optional, Dict

from app.functions.llm_utils import calculate_cost
from app.schemas.Dto.UsageStats import UsageStats
import json


class TelemetryBedrockClient:
  def __init__(self, bedrock_client: Any):
    self.bedrock_client = bedrock_client

  def invoke_model(
      self,
      model_id: str,
      body: str,
      trace_context: Optional[UsageStats] = None,
      **kwargs
  ):
    raw_response = self.bedrock_client.invoke_model(
      modelId=model_id,
      body=body,
      **kwargs
    )

    raw_body_bytes = raw_response['body'].read()
    parsed_body = json.loads(raw_body_bytes.decode('utf-8'))

    headers = raw_response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
    latency = int(headers.get("x-amzn-bedrock-invocation-latency", 0))

    input_tokens, output_tokens = self._extract_token_usage(model_id, parsed_body)

    try:
       is_cached = "cache_read" in str(parsed_body)
       cost = calculate_cost(model_id, input_tokens, output_tokens, is_cached)
    except ValueError:
       cost = 0.0

    if trace_context is not None:
       trace_context.populate(
          model_id=model_id,
          input_tokens=input_tokens,
          output_tokens=output_tokens,
          cost=cost,
          latency=latency
       )

    return parsed_body
  

  def invoke_model_with_response_stream(
      self,
      model_id: str,
      body: str,
      trace_context: Optional[UsageStats] = None,
      **kwargs
  ) -> dict:
    start_time = time.time()
    
    raw_response = self.bedrock_client.invoke_model_with_response_stream(
      modelId=model_id,
      body=body,
      **kwargs
    )

    original_stream = raw_response.get("body")

    def stream_interceptor() -> Generator[dict, None, None]:
        input_tokens = 0
        output_tokens = 0
        
        for event in original_stream:
            # Pass the chunk directly to the consumer so streaming isn't delayed
            yield event
            
            # Check for metadata/usage chunks emitted near the end of the stream
            chunk = event.get("chunk")
            if chunk:
                chunk_data = json.loads(chunk.get("bytes", b"{}").decode("utf-8"))
                
                # Claude 3/3.5 sends usage in 'message_start' and 'message_delta'
                if chunk_data.get("type") == "message_start":
                    usage = chunk_data.get("message", {}).get("usage", {})
                    input_tokens = usage.get("input_tokens", 0)
                    
                elif chunk_data.get("type") == "message_delta":
                    usage = chunk_data.get("usage", {})
                    output_tokens = usage.get("output_tokens", 0)

        latency = int((time.time() - start_time) * 1000)

        # Optional: Extract headers if needed
        headers = raw_response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
        header_latency = int(headers.get("x-amzn-bedrock-invocation-latency", latency))

        try:
            cost = calculate_cost(model_id, input_tokens, output_tokens, is_cached_read=False)
        except ValueError:
            cost = 0.0

        # 3. Populate trace context after stream completion
        if trace_context is not None:
            trace_context.populate(
                model_id=model_id,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                latency=header_latency or latency
            )

    raw_response["body"] = stream_interceptor()
    return raw_response


  def _extract_token_usage(self, model_id: str, response_body: Dict[str, Any]) -> tuple[int, int]:
      """Extracts token counts according to provider-specific payloads."""
      if "anthropic" in model_id:
          usage = response_body.get("usage", {})
          return usage.get("input_tokens", 0), usage.get("output_tokens", 0)
      elif "amazon.nova" in model_id:
          usage = response_body.get("usage", {})
          return usage.get("inputTokens", 0), usage.get("outputTokens", 0)
      elif "meta.llama" in model_id:
          return response_body.get("prompt_token_count", 0), response_body.get("generation_token_count", 0)
      elif "amazon.titan" in model_id:
          return response_body.get("inputTextTokenCount", 0), 0
      return 0, 0

