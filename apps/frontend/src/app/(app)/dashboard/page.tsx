export default async function DashboardPage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
  const res = await fetch(`${apiBase}/health`, { cache: "no-store" });
  const data = await res.json();

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <p className="text-sm text-gray-600">Status cards and recent activity will go here.</p>
      <div className="rounded-lg border border-slate-700 bg-slate-900/60 p-4">
        <p className="text-sm font-medium">API health: <span className="text-emerald-400">{data.status}</span></p>
      </div>
    </main>
  );
}
