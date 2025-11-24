import { Button } from "@/components/Button";
import { Callout } from "@/components/Callout";
import { Card } from "@/components/Card";
import { Container } from "@/components/Container";
import { ListItem } from "@/components/ListItem";
import { Pill } from "@/components/Pill";
import { SectionHeader } from "@/components/SectionHeader";
import { routes } from "@/lib/routes";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.wrapper}>
      <Container>
        <div className="flex flex-col items-start gap-6 text-left">
          <Pill>
            <span className="font-medium text-emerald-300">resuMAX</span>
            <span className="text-white/80">AI-powered resume optimizer</span>
          </Pill>

          <SectionHeader
            title="Perfect your resume with AI and land interviews faster."
            description="ResuMAX scores every line of your resume, suggests tailored edits, and adapts your profile to the roles you care about. Choose how you want to get started."
          />

          <div className="flex flex-wrap items-center gap-3">
            <Button href={routes.login}>Log in</Button>
            <Button href={routes.signup} variant="secondary">
              Create an account
            </Button>
          </div>
        </div>

        <section className="mt-14 grid gap-6 md:grid-cols-2">
          <Card>
            <p className="text-sm font-semibold text-emerald-300">Returning?</p>
            <h2 className="mt-2 text-2xl font-semibold">Log in to your workspace</h2>
            <p className="mt-3 text-white/75">
              Pick up where you left off with saved drafts, role-specific scoring, and recruiter-ready
              exports.
            </p>
            <Button href={routes.login} variant="secondary" size="md" className="mt-6">
              Go to login
            </Button>
          </Card>

          <Card tone="accent">
            <p className="text-sm font-semibold text-emerald-300">New here?</p>
            <h2 className="mt-2 text-2xl font-semibold">Create your free account</h2>
            <p className="mt-3 text-white/80">
              Let resuMAX rewrite bullet points, tailor summaries, and match keywords to the roles you
              actually want.
            </p>
            <ul className="mt-4 space-y-2">
              <ListItem>Instant AI scoring with actionable next steps.</ListItem>
              <ListItem>Role-aware rewrites tuned to each application.</ListItem>
              <ListItem>Version history so you can test and compare changes.</ListItem>
            </ul>
            <Button href={routes.signup} size="md" className="mt-6">
              Start with sign up
            </Button>
          </Card>
        </section>

        <Callout title="Heads up" className="mt-16">
          Log in and sign up will live under <span className="font-semibold">(auth)</span> soon. For now,
          these buttons lead the way once those routes are ready.
        </Callout>
      </Container>
    </div>
  );
}
