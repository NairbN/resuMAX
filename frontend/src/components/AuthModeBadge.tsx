"use client";

const isMockAuth = process.env.NEXT_PUBLIC_USE_MOCK_AUTH === "true";
const isMockApi = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";

export function AuthModeBadge() {
  const authLabel = isMockAuth ? "Auth: Mock" : "Auth: Firebase";
  const authTone = isMockAuth ? "bg-amber-500/90 text-black" : "bg-emerald-500/90 text-black";
  const apiLabel = isMockApi ? "API: Mock" : "API: Real";
  const apiTone = isMockApi ? "bg-amber-500/90 text-black" : "bg-blue-400/90 text-black";

  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-50 flex flex-col items-end gap-2">
      <span className={`rounded-full px-3 py-1 text-sm font-semibold shadow-lg ${authTone}`}>
        {authLabel}
      </span>
      <span className={`rounded-full px-3 py-1 text-sm font-semibold shadow-lg ${apiTone}`}>
        {apiLabel}
      </span>
    </div>
  );
}
