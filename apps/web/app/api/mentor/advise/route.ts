
import { type NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const { prompt } = await request.json()

  if (!prompt) {
    return new Response('Missing prompt', { status: 400 })
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/mentor/advise`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });
    if (!res.ok) {
      throw res; // Throw the response object instead of a generic error
    }
    const data = await res.json();
    return Response.json({ data });
  } catch (error) {
    // Attempt to parse error as JSON if it's a Response object
    if (error instanceof Response) {
      const errorBody = await error.json();
      return new Response(JSON.stringify(errorBody), { status: error.status, headers: { 'Content-Type': 'application/json' } });
    }
    return new Response(error.message || 'An unknown error occurred', { status: 500 });
  }
}
