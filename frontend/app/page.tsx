import Link from 'next/link';
import { ArrowRight, BadgeCheck, FileText, MessageSquare, Target, Video, Zap } from 'lucide-react';
import Navbar from '@/components/Navbar';

const factors = ['Founder-market fit', 'Skill coverage', 'Industry depth', 'Stage alignment', 'Working style', 'Risk tolerance'];
const steps = [
  'Create verified founder profile with skills, industry, stage, and co-founder preferences.',
  'Review AI-ranked matches scored across 30+ compatibility signals.',
  'Chat, launch video calls, and share pitch decks before committing to meetings.'
];

export default function HomePage() {
  return (
    <main>
      <Navbar />
      <section className="mx-auto grid max-w-7xl gap-12 px-6 py-20 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-brand-100 bg-white px-4 py-2 text-sm font-semibold text-brand-600 shadow-sm">
            <Zap className="h-4 w-4" /> AI co-founder matching for serious builders
          </div>
          <h1 className="text-5xl font-black tracking-tight text-brand-900 sm:text-6xl">
            Meet compatible co-founders before next idea dies alone.
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            CoFounder Connect ranks founders across skills, industry, stage, availability, work style, goals, and 30+ more factors. Browse free, upgrade to premium for advanced matching and priority support.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link href="/sign-up" className="inline-flex items-center justify-center gap-2 rounded-full bg-brand-600 px-6 py-3 font-bold text-white shadow-glow hover:bg-brand-500">
              Start free <ArrowRight className="h-4 w-4" />
            </Link>
            <Link href="/dashboard" className="inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 py-3 font-bold text-brand-900 hover:border-brand-200">
              View demo dashboard
            </Link>
          </div>
        </div>
        <div className="rounded-[2rem] border border-white bg-white/85 p-6 shadow-glow backdrop-blur">
          <div className="rounded-3xl bg-brand-900 p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-brand-100">Top match</p>
                <h2 className="text-2xl font-bold">Maya Chen</h2>
              </div>
              <span className="rounded-full bg-emerald-400 px-3 py-1 text-sm font-black text-emerald-950">94%</span>
            </div>
            <div className="mt-6 grid grid-cols-2 gap-3 text-sm">
              {factors.map((factor) => (
                <div key={factor} className="rounded-2xl bg-white/10 p-3">
                  <BadgeCheck className="mb-2 h-4 w-4 text-emerald-300" />
                  {factor}
                </div>
              ))}
            </div>
          </div>
          <div className="mt-5 grid gap-4 sm:grid-cols-3">
            <Feature icon={MessageSquare} title="Real-time chat" />
            <Feature icon={Video} title="WebRTC video" />
            <Feature icon={FileText} title="Pitch deck PDF" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid gap-6 md:grid-cols-3">
          {steps.map((step, index) => (
            <div key={step} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-brand-50 font-black text-brand-600">{index + 1}</span>
              <p className="mt-4 text-slate-700">{step}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="pricing" className="mx-auto max-w-7xl px-6 py-16">
        <div className="grid gap-6 lg:grid-cols-2">
          <Plan name="Free" price="$0" points={["Browse founder profiles", "Basic compatibility score", "Limited chat requests"]} />
          <Plan name="Premium" price="$29/mo" highlighted points={["30+ factor advanced matching", "Priority support", "Unlimited chat, video rooms, and pitch deck sharing"]} />
        </div>
      </section>
    </main>
  );
}

function Feature({ icon: Icon, title }: { icon: typeof Target; title: string }) {
  return (
    <div className="rounded-2xl border border-slate-100 bg-white p-4 text-center text-sm font-bold text-brand-900">
      <Icon className="mx-auto mb-2 h-5 w-5 text-brand-600" />
      {title}
    </div>
  );
}

function Plan({ name, price, points, highlighted = false }: { name: string; price: string; points: string[]; highlighted?: boolean }) {
  return (
    <div className={`rounded-3xl border p-8 ${highlighted ? 'border-brand-500 bg-brand-900 text-white shadow-glow' : 'border-slate-200 bg-white text-brand-900'}`}>
      <h3 className="text-2xl font-black">{name}</h3>
      <p className="mt-2 text-4xl font-black">{price}</p>
      <ul className="mt-6 space-y-3">
        {points.map((point) => (
          <li key={point} className="flex items-center gap-3">
            <BadgeCheck className="h-5 w-5 text-emerald-400" /> {point}
          </li>
        ))}
      </ul>
    </div>
  );
}
