"use client";

const isMock = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true";
const label = isMock ? "Auth: Mock" : "Auth: Firebase";
const tone = isMock ? "bg-amber-500/90 text-black" : "bg-emerald-500/90 text-black";

export function AuthModeBadge() {
  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-50">
      <span className={`rounded-full px-3 py-1 text-sm font-semibold shadow-lg ${tone}`}>
        {label}
      </span>
    </div>
  );
}
