import { NextResponse } from "next/server";
import { signup } from "@/app/(auth)/lib/auth-client";

export async function POST(request: Request) {
  try {
    const { name, email, password } = await request.json();
    const result = await signup({ name, email, password });

    if (!result.ok) {
      return NextResponse.json({ ok: false, error: result.error }, { status: 400 });
    }

    console.log("[auth] signup success", { userId: result.userId, email, name });
    return NextResponse.json({ ok: true, userId: result.userId });
  } catch (error) {
    console.error("[auth] signup error", error);
    return NextResponse.json({ ok: false, error: "Unexpected error" }, { status: 500 });
  }
}
