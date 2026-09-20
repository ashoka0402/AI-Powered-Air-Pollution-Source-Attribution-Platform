"""
Tiny pipeline progress visualizer for Person 2 AI layer.

Usage:
    from src.common.pipeline_progress import PipelineProgress

    progress = PipelineProgress()
    progress.start()
    progress.step("baseline", "Building pollution baseline…")
    # … do work …
    progress.done("baseline", detail="24 cells")
    progress.step("events", "Detecting pollution events…")
    progress.done("events", detail="9 events found")
    progress.finish()
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# Ordered stages of the Person 2 pipeline
STAGES = [
    ("ingest", "Load data"),
    ("baseline", "Build baseline"),
    ("events", "Detect events"),
    ("candidates", "Candidate sources"),
    ("features", "Build features"),
    ("ml", "ML probabilities"),
    ("fusion", "Evidence fusion"),
    ("attribution", "Attribution result"),
    ("forecast", "Forecast"),
]


@dataclass
class StageState:
    name: str
    label: str
    status: str = "pending"  # pending | running | done | skipped | failed
    detail: str = ""
    started_at: Optional[float] = None
    finished_at: Optional[float] = None

    @property
    def duration_s(self) -> Optional[float]:
        if self.started_at is None:
            return None
        end = self.finished_at if self.finished_at is not None else time.time()
        return end - self.started_at


class PipelineProgress:
    """
    Pretty terminal progress for the source-attribution pipeline.

    Call:
        progress.start()
        progress.step("baseline", "Building pollution baseline…")
        progress.done("baseline", detail="24 cells")
        …
        progress.finish()
    """

    def __init__(self, stream=None, width: int = 56):
        self.stream = stream or sys.stdout
        self.width = width
        self.stages: Dict[str, StageState] = {
            key: StageState(name=key, label=label) for key, label in STAGES
        }
        self._order = [key for key, _ in STAGES]
        self._started = False
        self._t0: Optional[float] = None

    # ── public API ──────────────────────────────────────────────

    def start(self, title: str = "Person 2 · AI Pipeline") -> None:
        self._started = True
        self._t0 = time.time()
        self._clear_and_draw(header=title)

    def step(self, stage: str, message: str = "") -> None:
        """Mark stage as running."""
        st = self._get(stage)
        st.status = "running"
        st.detail = message
        st.started_at = time.time()
        st.finished_at = None
        self._clear_and_draw()

    def done(self, stage: str, detail: str = "") -> None:
        st = self._get(stage)
        st.status = "done"
        if detail:
            st.detail = detail
        st.finished_at = time.time()
        self._clear_and_draw()

    def skip(self, stage: str, detail: str = "skipped") -> None:
        st = self._get(stage)
        st.status = "skipped"
        st.detail = detail
        st.finished_at = time.time()
        self._clear_and_draw()

    def fail(self, stage: str, detail: str = "failed") -> None:
        st = self._get(stage)
        st.status = "failed"
        st.detail = detail
        st.finished_at = time.time()
        self._clear_and_draw()

    def finish(self, title: str = "Pipeline complete") -> None:
        elapsed = time.time() - self._t0 if self._t0 else 0.0
        self._clear_and_draw(header=f"{title}  ({elapsed:.1f}s)")
        self.stream.write("\n")
        self.stream.flush()

    # ── internals ───────────────────────────────────────────────

    def _get(self, stage: str) -> StageState:
        if stage not in self.stages:
            # allow ad-hoc stages
            self.stages[stage] = StageState(name=stage, label=stage)
            self._order.append(stage)
        return self.stages[stage]

    def _icon(self, status: str) -> str:
        return {
            "pending": "○",
            "running": "◉",
            "done": "●",
            "skipped": "◌",
            "failed": "✗",
        }.get(status, "?")

    def _color(self, status: str, text: str) -> str:
        # ANSI colors (safe for most terminals)
        codes = {
            "pending": "\033[90m",   # grey
            "running": "\033[96m",   # cyan
            "done": "\033[92m",      # green
            "skipped": "\033[90m",
            "failed": "\033[91m",    # red
        }
        reset = "\033[0m"
        return f"{codes.get(status, '')}{text}{reset}"

    def _bar(self) -> str:
        total = len(self._order)
        done = sum(1 for k in self._order if self.stages[k].status in ("done", "skipped"))
        running = any(self.stages[k].status == "running" for k in self._order)
        width = 20
        filled = int(width * done / max(total, 1))
        if running and filled < width:
            bar = "█" * filled + "▓" + "░" * (width - filled - 1)
        else:
            bar = "█" * filled + "░" * (width - filled)
        pct = int(100 * done / max(total, 1))
        return f"[{bar}] {pct:3d}%"

    def _clear_and_draw(self, header: Optional[str] = None) -> None:
        # Move cursor up to redraw in place (n lines = stages + header + bar + blank)
        n_lines = len(self._order) + 4
        if self._started:
            self.stream.write(f"\033[{n_lines}A")  # cursor up

        lines: List[str] = []
        lines.append("")
        lines.append(header or "Person 2 · AI Pipeline")
        lines.append(self._bar())
        lines.append("─" * self.width)

        for key in self._order:
            st = self.stages[key]
            icon = self._icon(st.status)
            label = f"{st.label:<22}"
            detail = st.detail
            if st.status == "done" and st.duration_s is not None and not detail:
                detail = f"{st.duration_s:.2f}s"
            elif st.status == "done" and st.duration_s is not None:
                detail = f"{detail}  ({st.duration_s:.2f}s)"

            row = f"  {icon}  {label}  {detail}"
            lines.append(self._color(st.status, row))

        # pad so we always overwrite the same number of lines
        while len(lines) < n_lines:
            lines.append("")

        for line in lines:
            self.stream.write(line[: self.width + 30].ljust(self.width + 10) + "\n")
        self.stream.flush()


# ── convenience one-liner for quick scripts ─────────────────────

def demo_progress(sleep: float = 0.4) -> None:
    """Run a fake pipeline so you can see the visualizer."""
    p = PipelineProgress()
    p.start()
    steps = [
        ("ingest", "Loaded 240 records", 0.3),
        ("baseline", "24 cells", 0.5),
        ("events", "9 events", 0.4),
        ("candidates", "4 candidates", 0.3),
        ("features", "22 features", 0.2),
        ("ml", "uniform prior (no model)", 0.3),
        ("fusion", "fused 5 channels", 0.4),
        ("attribution", "construction 61%", 0.3),
        ("forecast", "24 h horizon", 0.4),
    ]
    for key, detail, delay in steps:
        p.step(key, f"…")
        time.sleep(delay)
        p.done(key, detail)
    p.finish()


if __name__ == "__main__":
    demo_progress()
