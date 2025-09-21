
import { type NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const { profile_id, top_k_contexts, signals_block, constraints } = await request.json()

  if (!profile_id || !top_k_contexts || !signals_block || !constraints) {
    return new Response('Missing required fields', { status: 400 })
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/generate/opportunities`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ profile_id, top_k_contexts, signals_block, constraints }),
    });
    if (!res.ok) {
      throw new Error('Failed to generate opportunities');
    }
    const data = await res.json();
    return Response.json({ data });
  } catch (error) {
    return new Response('Error generating opportunities', { status: 500 });
  }
}
