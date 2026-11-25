import { ArrowUpRight, BadgeCheck, Braces, FlaskConical, ScanLine } from 'lucide-react';
import Link from 'next/link';

const evidence = [
	{ number: '01', title: 'Assessment', detail: 'Timed, role-relevant work', icon: FlaskConical },
	{ number: '02', title: 'Execution', detail: 'Isolated code runtime', icon: Braces },
	{ number: '03', title: 'Evaluation', detail: 'Tests, quality, security', icon: ScanLine },
	{ number: '04', title: 'Passport', detail: 'Explainable skill record', icon: BadgeCheck },
];

export default function Home() {
	return (
		<main className="min-h-full bg-paper text-ink">
			<header className="mx-auto flex max-w-360 items-center justify-between px-5 py-5 sm:px-8 lg:px-12">
				<a href="#top" className="flex items-center gap-3" aria-label="SkillProof home">
					<span className="grid size-9 place-items-center border-2 border-ink bg-signal text-sm font-black">SP</span>
					<span className="text-lg font-bold tracking-tight">SkillProof</span>
				</a>
				<nav className="hidden items-center gap-8 text-sm font-semibold md:flex" aria-label="Primary navigation">
					<a className="hover:text-blue" href="#workflow">How it works</a>
					<a className="hover:text-blue" href="#principles">Principles</a>
					<Link className="hover:text-blue" href="/login">Sign in</Link>
				</nav>
				<Link className="flex min-h-11 items-center gap-2 border-2 border-ink px-4 text-sm font-bold transition-colors hover:bg-ink hover:text-white" href="/register">
					Create account <ArrowUpRight className="size-4" aria-hidden="true" />
				</Link>
			</header>

			<section id="top" className="mx-auto grid max-w-360 border-t-2 border-ink px-5 sm:px-8 lg:grid-cols-[1fr_380px] lg:px-12">
				<div className="py-16 lg:border-r-2 lg:border-ink lg:py-24 lg:pr-12">
					<p className="mb-8 flex items-center gap-3 text-xs font-bold uppercase tracking-[0.18em] text-blue">
						<span className="h-2 w-12 bg-signal" /> Project-based verification
					</p>
					<h1 className="max-w-4xl text-[clamp(3.5rem,8vw,7.75rem)] font-black leading-[0.86] tracking-[-0.065em]">
						Proof over promises.
					</h1>
					<p className="mt-8 max-w-xl text-lg leading-relaxed text-ink/70 sm:text-xl">
						Turn real project work into evidence employers can inspect—and verified skills students can stand behind.
					</p>
				</div>

				<aside id="principles" className="grid content-between border-t-2 border-ink lg:border-t-0 lg:pl-10">
					<div className="border-b-2 border-ink py-6 lg:py-10">
						<p className="text-xs font-bold uppercase tracking-[0.18em] text-ink/55">Platform foundation</p>
						<p className="mt-3 text-5xl font-black tracking-tight">MVP<span className="text-signal">.</span></p>
					</div>
					<div className="grid grid-cols-2 gap-px bg-ink/15">
						<div className="bg-paper py-6 pr-4"><strong className="block text-2xl">API</strong><span className="text-sm text-ink/60">Versioned</span></div>
						<div className="bg-paper py-6 pl-4"><strong className="block text-2xl">Queue</strong><span className="text-sm text-ink/60">Async</span></div>
					</div>
				</aside>
			</section>

			<section id="workflow" className="border-y-2 border-ink bg-white">
				<div className="mx-auto max-w-360 px-5 sm:px-8 lg:px-12">
					<div className="flex items-end justify-between border-b-2 border-ink py-6">
						<h2 className="text-2xl font-black tracking-tight">The evidence chain</h2>
						<p className="text-xs font-bold uppercase tracking-[0.15em] text-ink/55">4 evidence layers</p>
					</div>
					<div className="grid sm:grid-cols-2 lg:grid-cols-4">
						{evidence.map(({ number, title, detail, icon: Icon }, index) => (
							<article key={title} className={`py-8 sm:px-6 ${index > 0 ? 'border-t-2 border-ink sm:border-t-0 sm:border-l-2' : ''}`}>
								<div className="flex items-start justify-between">
									<span className="font-mono text-xs text-ink/45">{number}</span>
									<Icon className="size-6 text-blue" strokeWidth={1.8} aria-hidden="true" />
								</div>
								<h3 className="mt-12 text-xl font-black">{title}</h3>
								<p className="mt-2 text-sm text-ink/60">{detail}</p>
							</article>
						))}
					</div>
				</div>
			</section>
		</main>
	);
}
