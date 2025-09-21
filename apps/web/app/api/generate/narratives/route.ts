
import { type NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const { motifs, lineage_contexts, audience_segments } = await request.json()

  if (!motifs || !lineage_contexts || !audience_segments) {
    return new Response('Missing required fields', { status: 400 })
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/generate/narratives`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ motifs, lineage_contexts, audience_segments }),
    });
    if (!res.ok) {
      throw new Error('Failed to generate narratives');
    }
    const data = await res.json();
    return Response.json({ data });
  } catch (error) {
    return new Response('Error generating narratives', { status: 500 });
  }
}
