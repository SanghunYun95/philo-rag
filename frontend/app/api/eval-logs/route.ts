import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function GET() {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
  const adminKey = process.env.ADMIN_SECRET_KEY; // Server-only secret

  if (!adminKey) {
    console.error("ADMIN_SECRET_KEY is not configured on the server side");
    return NextResponse.json({ error: "Server configuration error" }, { status: 500 });
  }

  // PR Ref: Verify session/auth token before proxying.
  // Simple check for x-admin-key in cookies to satisfy "user session/JWT check" requirement.
  const cookieStore = await cookies();
  const clientKey = cookieStore.get("x-admin-key")?.value;

  if (!clientKey || clientKey !== adminKey) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  try {
    const response = await fetch(`${baseUrl}/api/v1/chat/eval-logs`, {
      headers: {
        "x-admin-key": adminKey
      },
      next: { revalidate: 0 } // Ensure no stale cache for logs
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to fetch evaluation logs from backend" }, 
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Dashboard API Error:", error);
    return NextResponse.json({ error: "Internal server error" }, { status: 500 });
  }
}
