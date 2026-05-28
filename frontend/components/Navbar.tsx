import Link from 'next/link';
import { SignedIn, SignedOut, UserButton } from '@clerk/nextjs';
import { Sparkles } from 'lucide-react';

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/70 bg-white/80 backdrop-blur">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2 font-bold text-brand-900">
          <span className="flex h-9 w-9 items-center justify-center rounded-2xl bg-brand-600 text-white shadow-glow">
            <Sparkles className="h-5 w-5" />
          </span>
          CoFounder Connect
        </Link>
        <div className="flex items-center gap-3 text-sm font-semibold">
          <Link href="/#pricing" className="hidden text-slate-600 hover:text-brand-600 sm:block">
            Pricing
          </Link>
          <SignedOut>
            <Link href="/sign-in" className="text-slate-600 hover:text-brand-600">
              Sign in
            </Link>
            <Link href="/sign-up" className="rounded-full bg-brand-600 px-4 py-2 text-white shadow-glow hover:bg-brand-500">
              Join free
            </Link>
          </SignedOut>
          <SignedIn>
            <Link href="/dashboard" className="rounded-full bg-brand-600 px-4 py-2 text-white hover:bg-brand-500">
              Dashboard
            </Link>
            <UserButton afterSignOutUrl="/" />
          </SignedIn>
        </div>
      </nav>
    </header>
  );
}
