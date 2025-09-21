
import { type NextRequest } from 'next/server'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const profileId = searchParams.get('profileId')

  if (!profileId) {
    return new Response('Missing profileId', { status: 400 })
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/insights/${profileId}`);
    if (!res.ok) {
      throw new Error('Failed to fetch insights');
    }
    const data = await res.json();
    return Response.json({ data });
  } catch (error) {
    return new Response('Error fetching insights', { status: 500 });
  }
}
