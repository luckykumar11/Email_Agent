"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth-context";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/company", label: "Company Profile" },
  { href: "/email-config", label: "Email Configuration" },
  { href: "/signature", label: "Email Signature" },
  { href: "/preferences", label: "Email Preferences" },
  { href: "/agent", label: "Email Agent" },
  { href: "/history", label: "Email History" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { logout, user } = useAuth();

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4 flex flex-col">
      <div className="mb-8">
        <h1 className="text-xl font-bold">Email Agent</h1>
        {user && <p className="text-sm text-gray-400 mt-1">{user.name}</p>}
      </div>
      <nav className="flex-1 space-y-1">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            className={`block px-3 py-2 rounded text-sm ${
              pathname === link.href
                ? "bg-blue-600 text-white"
                : "text-gray-300 hover:bg-gray-800"
            }`}
          >
            {link.label}
          </Link>
        ))}
      </nav>
      <button
        onClick={logout}
        className="mt-auto px-3 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-gray-800 rounded"
      >
        Logout
      </button>
    </aside>
  );
}
