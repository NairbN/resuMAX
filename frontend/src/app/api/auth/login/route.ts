import { NextResponse } from "next/server";
import { login } from "@/app/(auth)/lib/auth-client";

export async function POST(request: Request) {
  try {
    const { email, password } = await request.json();
    const result = await login({ email, password });

    if (!result.ok) {
      return NextResponse.json({ ok: false, error: result.error }, { status: 401 });
    }

    console.log("[auth] login success", { userId: result.userId, email });
    return NextResponse.json({ ok: true, userId: result.userId });
  } catch (error) {
    console.error("[auth] login error", error);
    return NextResponse.json({ ok: false, error: "Unexpected error" }, { status: 500 });
  }
}
