import Link from "next/link";
import { useRouter } from "next/navigation";
import { logout } from "@/app/(auth)/lib/auth-client";
import { routes } from "@/lib/routes";

const navItems = [
  { label: "Dashboard", href: routes.dashboard },
  { label: "Profile", href: "/profile" },
  { label: "Jobs", href: "/jobs" },
  { label: "Optimizations", href: "/optimizations" },
];

export function Navbar() {
  const router = useRouter();

  async function handleLogout() {
    try {
      await logout();
    } catch {
      // ignore logout errors for now
    }
    router.push(routes.home);
  }

  return (
    <header className="flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-5 py-4 shadow-sm shadow-black/30">
      <div className="flex items-center gap-3">
        <div className="h-9 w-9 rounded-full bg-emerald-400" />
        <div className="text-lg font-semibold tracking-tight">resuMAX</div>
      </div>
      <nav className="hidden items-center gap-6 text-sm text-white/80 md:flex">
        {navItems.map((item) => (
          <Link key={item.href} href={item.href} className="hover:text-emerald-200">
            {item.label}
          </Link>
        ))}
      </nav>
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-full bg-white/20" />
        <button onClick={handleLogout} className="text-sm text-white/70 hover:text-emerald-200">
          Logout
        </button>
      </div>
    </header>
  );
}
