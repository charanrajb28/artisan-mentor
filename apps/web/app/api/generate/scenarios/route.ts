
import { type NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const { use_case, capacity, fragility, lead_time } = await request.json()

  if (!use_case || !capacity || !fragility || !lead_time) {
    return new Response('Missing required fields', { status: 400 })
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/generate/scenarios`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ use_case, capacity, fragility, lead_time }),
    });
    if (!res.ok) {
      throw new Error('Failed to generate scenarios');
    }
    const data = await res.json();
    return Response.json({ data });
  } catch (error) {
    return new Response('Error generating scenarios', { status: 500 });
  }
}
