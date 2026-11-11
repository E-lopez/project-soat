import { QueryResponseChunk } from "../models/interfaces/QueryResponseChunk"

const BASE_URL = import.meta.env.DEV ? 'http://127.0.0.1:8000' : ''

export interface QueryResponse {
  answer: string
  sources: string[]
}

export interface IndexResponse {
  indexed: number
  message: string
}

export async function createIndex(): Promise<IndexResponse> {
  const health = await fetch(`${BASE_URL}/health`, { method: 'GET' })
  console.log("REsponse from createIndex:", health);
  const res = await fetch(`${BASE_URL}/v1/create-index`, { 
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
    },
  })
  if (!res.ok) throw new Error('Failed to initialize knowledge base.')
  return res.json() as Promise<IndexResponse>
}


export async function* sendQuery(question: string, company: string): AsyncGenerator<QueryResponseChunk, void, unknown> {
  const res = await fetch(`${BASE_URL}/v1/query/hybrid-search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: question, company: company || '' }),
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({})) as { detail?: string }
    throw new Error(body.detail ?? 'Request failed.')
  }
  if (!res.body) {
    throw new Error('Response body is empty or not streamable.');
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split(/\r?\n\r?\n/);
      buffer = events.pop() || '';

      for (const event of events) {
        const trimmed = event.trim();
        if (!trimmed) continue;

        for (const event of trimmed.split(/\r?\n/)) {
          if (event.startsWith('data:')) {
            const jsonString = event.slice(5).trim();
            if (!jsonString) continue;

            try {
              const parsed = JSON.parse(jsonString) as QueryResponseChunk;
              yield parsed;
            } catch (e) {
              console.error('Failed to parse stream JSON chunk:', jsonString, e);
            }
          }
        }
      }
    }

  }
  finally {
    reader.releaseLock();
  }
}
