import { CalendarDays, FileText, MessageCircle, Upload, Video } from 'lucide-react';

const matches = [
  { name: 'Maya Chen', role: 'AI product lead', score: 94, industry: 'Fintech', stage: 'MVP', skills: ['ML', 'Product', 'Fundraising'] },
  { name: 'Andre Patel', role: 'Full-stack founder', score: 88, industry: 'B2B SaaS', stage: 'Pre-seed', skills: ['Next.js', 'Sales', 'Ops'] },
  { name: 'Sofia Rivera', role: 'Growth operator', score: 82, industry: 'Climate', stage: 'Idea', skills: ['Growth', 'Partnerships', 'Pitch'] }
];

const messages = [
  ['Maya', 'Loved your healthcare workflow deck. Want to compare founder-market fit live?'],
  ['Andre', 'I can cover engineering. Looking for customer discovery partner.'],
  ['Sofia', 'Uploaded revised pitch deck with traction slide.']
];

export default function DashboardPage() {
  return (
    <main className="mx-auto max-w-7xl px-6 py-10">
      <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="font-bold text-brand-600">Founder dashboard</p>
          <h1 className="mt-2 text-4xl font-black text-brand-900">Today&apos;s best co-founder matches</h1>
          <p className="mt-3 max-w-2xl text-slate-600">Review AI-ranked profiles, start chats, launch video rooms, and share pitch decks from one workspace.</p>
        </div>
        <button className="inline-flex items-center justify-center gap-2 rounded-full bg-brand-600 px-5 py-3 font-bold text-white shadow-glow hover:bg-brand-500">
          <Upload className="h-4 w-4" /> Upload pitch deck PDF
        </button>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.5fr_0.8fr]">
        <section className="space-y-4">
          {matches.map((match) => (
            <article key={match.name} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
                <div>
                  <div className="flex items-center gap-3">
                    <h2 className="text-2xl font-black text-brand-900">{match.name}</h2>
                    <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-black text-emerald-700">{match.score}% match</span>
                  </div>
                  <p className="mt-1 text-slate-600">{match.role} · {match.industry} · {match.stage}</p>
                </div>
                <div className="flex gap-2">
                  <button className="rounded-full border border-slate-200 p-3 text-brand-600 hover:bg-brand-50" aria-label={`Chat with ${match.name}`}><MessageCircle className="h-5 w-5" /></button>
                  <button className="rounded-full border border-slate-200 p-3 text-brand-600 hover:bg-brand-50" aria-label={`Start video with ${match.name}`}><Video className="h-5 w-5" /></button>
                </div>
              </div>
              <div className="mt-5 flex flex-wrap gap-2">
                {match.skills.map((skill) => (
                  <span key={skill} className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-700">{skill}</span>
                ))}
              </div>
            </article>
          ))}
        </section>

        <aside className="space-y-6">
          <Panel title="Premium matching" icon={<CalendarDays className="h-5 w-5" />}>
            <p className="text-sm text-slate-600">Unlock advanced 30+ factor scoring, unlimited introductions, and priority support for $29/mo.</p>
            <button className="mt-4 w-full rounded-full bg-brand-900 px-4 py-3 font-bold text-white hover:bg-brand-600">Upgrade plan</button>
          </Panel>
          <Panel title="Recent chat" icon={<MessageCircle className="h-5 w-5" />}>
            <div className="space-y-3">
              {messages.map(([name, text]) => (
                <div key={name} className="rounded-2xl bg-slate-50 p-3">
                  <p className="font-bold text-brand-900">{name}</p>
                  <p className="text-sm text-slate-600">{text}</p>
                </div>
              ))}
            </div>
          </Panel>
          <Panel title="Pitch deck" icon={<FileText className="h-5 w-5" />}>
            <p className="text-sm text-slate-600">cofounder-connect-seed.pdf · shared with 3 matches · 42 views</p>
          </Panel>
        </aside>
      </div>
    </main>
  );
}

function Panel({ title, icon, children }: { title: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center gap-2 font-black text-brand-900">{icon}{title}</div>
      {children}
    </section>
  );
}
