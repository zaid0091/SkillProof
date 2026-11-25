"""One-off scaffold helper: creates the Django domain app skeletons.

Run from the backend directory:
    python ../scripts/_scaffold_apps.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "backend" / "apps"

APPS = {
    "accounts": ("Accounts", "Identity, roles, and sessions.", "Phase 2", "SP-005 to SP-009"),
    "organizations": (
        "Organizations",
        "Employer and university organisations with membership.",
        "Phase 3",
        "SP-027, SP-031",
    ),
    "profiles": (
        "Profiles",
        "Student, employer, and university profile records.",
        "Phase 3",
        "SP-010, SP-012",
    ),
    "skills": (
        "Skills",
        "Skill catalogue, verification records, and passport assembly.",
        "Phase 6",
        "SP-023 to SP-026",
    ),
    "assessments": (
        "Assessments",
        "Assessment definitions, tasks, and private test configurations.",
        "Phase 4",
        "SP-013 to SP-016",
    ),
    "submissions": (
        "Submissions",
        "Student submissions, validation, and execution status.",
        "Phase 5",
        "SP-017, SP-018",
    ),
    "evaluations": (
        "Evaluations",
        "Execution results and code-quality findings.",
        "Phase 5",
        "SP-019 to SP-022",
    ),
    "evidence": (
        "Evidence",
        "Evidence records, confidence inputs, and revocation.",
        "Phase 6",
        "SP-023 to SP-025",
    ),
    "github_integration": (
        "GitHub Integration",
        "Consent-based repository evidence (supplementary only).",
        "Phase 8",
        "SP-034, SP-035",
    ),
    "hiring": (
        "Hiring",
        "Candidate search, shortlists, internships, and applications.",
        "Phase 7",
        "SP-028 to SP-030",
    ),
    "analytics": (
        "Analytics",
        "Aggregate institutional and platform reporting.",
        "Phase 9",
        "SP-032, SP-033",
    ),
    "notifications": (
        "Notifications",
        "In-app and email notifications.",
        "Phase 9",
        "SP-036, SP-037",
    ),
    "audit": (
        "Audit",
        "Immutable security and administrative event log.",
        "Phase 9",
        "SP-039",
    ),
}

APPS_PY = '''"""{verbose} domain module."""

from __future__ import annotations

from django.apps import AppConfig


class {cls}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.{package}"
    label = "{package}"
    verbose_name = "{verbose}"
'''

MODELS_PY = '''"""{verbose}: {description}

Models for this module arrive in {phase} ({tickets}). The app boundary is
created in Phase 1 so that later migrations land in the module that owns the
data; see docs/tad.md section 5.2 for module responsibilities.
"""

from __future__ import annotations

# Models are intentionally absent until {phase}. Do not create schemas here for
# other modules to satisfy an early demo: ownership must stay with the module.
'''


def main() -> None:
    for package, (verbose, description, phase, tickets) in APPS.items():
        app_dir = ROOT / package
        (app_dir / "migrations").mkdir(parents=True, exist_ok=True)

        init = app_dir / "__init__.py"
        if not init.exists():
            init.write_text(f'"""The {verbose.lower()} domain module."""\n', encoding="utf-8")

        migrations_init = app_dir / "migrations" / "__init__.py"
        if not migrations_init.exists():
            migrations_init.write_text("", encoding="utf-8")

        apps_py = app_dir / "apps.py"
        if not apps_py.exists():
            cls = "".join(part.capitalize() for part in package.split("_"))
            apps_py.write_text(
                APPS_PY.format(verbose=verbose, cls=cls, package=package),
                encoding="utf-8",
            )

        models_py = app_dir / "models.py"
        if not models_py.exists():
            models_py.write_text(
                MODELS_PY.format(
                    verbose=verbose,
                    description=description,
                    phase=phase,
                    tickets=tickets,
                ),
                encoding="utf-8",
            )

        print(f"scaffolded apps/{package}")


if __name__ == "__main__":
    main()
