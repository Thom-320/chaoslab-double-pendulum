const data = window.CHAOS_DATA;
const slides = [...document.querySelectorAll(".slide")];
const counter = document.querySelector("#counter");
const progress = document.querySelector("#progress-bar");
const notesPanel = document.querySelector("#notes-panel");
const DPR = Math.min(window.devicePixelRatio || 1, 2);

let current = 0;
let notesVisible = false;
let startTime = performance.now();

function fitCanvas(canvas) {
  const rect = canvas.getBoundingClientRect();
  canvas.width = Math.floor(rect.width * DPR);
  canvas.height = Math.floor(rect.height * DPR);
  const ctx = canvas.getContext("2d");
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  return { ctx, width: rect.width, height: rect.height };
}

function showSlide(index) {
  current = (index + slides.length) % slides.length;
  slides.forEach((slide, i) => slide.classList.toggle("is-active", i === current));
  counter.value = `${current + 1} / ${slides.length}`;
  progress.style.width = `${((current + 1) / slides.length) * 100}%`;
  startTime = performance.now();
  updateNotes();
}

function updateNotes() {
  const notes = slides[current].querySelector(".notes")?.textContent || "";
  notesPanel.textContent = notes;
  notesPanel.hidden = !notesVisible;
}

document.querySelector("#prev").addEventListener("click", () => showSlide(current - 1));
document.querySelector("#next").addEventListener("click", () => showSlide(current + 1));
document.querySelector("#notes-toggle").addEventListener("click", () => {
  notesVisible = !notesVisible;
  updateNotes();
});

window.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight" || event.key === " ") showSlide(current + 1);
  if (event.key === "ArrowLeft") showSlide(current - 1);
  if (event.key.toLowerCase() === "n") {
    notesVisible = !notesVisible;
    updateNotes();
  }
});

window.addEventListener("resize", () => {
  document.querySelectorAll("canvas").forEach(fitCanvas);
});

function clear(ctx, w, h) {
  ctx.clearRect(0, 0, w, h);
}

function mapPoint(x, y, w, h, scale = 170, ox = w * 0.5, oy = h * 0.5) {
  return [ox + x * scale, oy + y * scale];
}

function drawPendulum(ctx, series, idx, w, h, options = {}) {
  const scale = options.scale || Math.min(w, h) * 0.19;
  const ox = options.ox || w * 0.55;
  const oy = options.oy || h * 0.36;
  const trail = options.trail || 130;
  const color = options.color || "oklch(82% 0.16 205)";
  const bob = options.bob || "oklch(84% 0.16 85)";
  const start = Math.max(0, idx - trail);

  ctx.lineWidth = 2;
  ctx.strokeStyle = color;
  ctx.globalAlpha = 0.85;
  ctx.beginPath();
  for (let i = start; i <= idx; i += 1) {
    const [px, py] = mapPoint(series.x2[i], series.y2[i], w, h, scale, ox, oy);
    if (i === start) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();
  ctx.globalAlpha = 1;

  const [x1, y1] = mapPoint(series.x1[idx], series.y1[idx], w, h, scale, ox, oy);
  const [x2, y2] = mapPoint(series.x2[idx], series.y2[idx], w, h, scale, ox, oy);
  ctx.strokeStyle = "oklch(94% 0.01 90)";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(ox, oy);
  ctx.lineTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();

  ctx.fillStyle = "oklch(72% 0.22 335)";
  ctx.beginPath();
  ctx.arc(x1, y1, 6, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = bob;
  ctx.beginPath();
  ctx.arc(x2, y2, 8, 0, Math.PI * 2);
  ctx.fill();
}

function drawSimple(ctx, elapsed, w, h) {
  const simple = data.simple;
  const idx = Math.floor((elapsed * 48) % simple.x.length);
  const ox = w * 0.30;
  const oy = h * 0.22;
  const scale = Math.min(w, h) * 0.24;
  const x = ox + simple.x[idx] * scale;
  const y = oy - simple.y[idx] * scale;

  ctx.strokeStyle = "oklch(94% 0.01 90)";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(ox, oy);
  ctx.lineTo(x, y);
  ctx.stroke();

  ctx.strokeStyle = "oklch(82% 0.16 205)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i <= idx; i += 1) {
    const px = ox + simple.x[i] * scale;
    const py = oy - simple.y[i] * scale;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  ctx.fillStyle = "oklch(84% 0.16 85)";
  ctx.beginPath();
  ctx.arc(x, y, 9, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = "oklch(84% 0.16 85)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(ox, oy, 52, Math.PI / 2, Math.PI / 2 + simple.theta[idx]);
  ctx.stroke();
}

function drawChart(ctx, values, labels, elapsed, w, h, mode = "linear") {
  const pad = { left: 90, right: 70, top: 150, bottom: 110 };
  const x0 = pad.left;
  const y0 = h - pad.bottom;
  const cw = w - pad.left - pad.right;
  const ch = h - pad.top - pad.bottom;
  const count = values[0].y.length;
  const end = Math.max(8, Math.floor(((elapsed % 11) / 11) * count));
  const all = values.flatMap((v) => v.y.map((n) => (mode === "log" ? Math.log10(Math.max(n, 1e-9)) : n)));
  const min = Math.min(...all);
  const max = Math.max(...all);

  ctx.strokeStyle = "oklch(31% 0.035 270)";
  ctx.lineWidth = 1;
  ctx.strokeRect(x0, pad.top, cw, ch);

  ctx.fillStyle = "oklch(73% 0.025 275)";
  ctx.font = "14px system-ui";
  ctx.fillText("t [s]", x0 + cw - 40, y0 + 44);

  values.forEach((series, si) => {
    ctx.strokeStyle = series.color;
    ctx.lineWidth = series.width || 2;
    ctx.beginPath();
    for (let i = 0; i < end; i += 1) {
      const x = x0 + (i / (count - 1)) * cw;
      const raw = series.y[i];
      const val = mode === "log" ? Math.log10(Math.max(raw, 1e-9)) : raw;
      const y = y0 - ((val - min) / (max - min || 1)) * ch;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.fillStyle = series.color;
    ctx.fillText(labels[si], x0 + 24 + si * 118, pad.top - 24);
  });
}

function renderScene(name, ctx, elapsed, w, h) {
  clear(ctx, w, h);
  const dbl = data.double;
  const idx = Math.floor((elapsed * 32) % dbl.x1.length);

  if (name === "hook") {
    drawPendulum(ctx, { x1: dbl.x1, y1: dbl.y1, x2: dbl.x2, y2: dbl.y2 }, idx, w, h, {
      ox: w * 0.52,
      oy: h * 0.36,
      color: "oklch(82% 0.16 205)",
      bob: "oklch(84% 0.16 85)",
    });
    drawPendulum(ctx, { x1: dbl.xb1, y1: dbl.yb1, x2: dbl.xb2, y2: dbl.yb2 }, idx, w, h, {
      ox: w * 0.52,
      oy: h * 0.36,
      color: "oklch(78% 0.18 145)",
      bob: "oklch(78% 0.18 145)",
      trail: 120,
    });
  }

  if (name === "simple") drawSimple(ctx, elapsed, w, h);

  if (name === "state") {
    drawPendulum(ctx, { x1: dbl.x1, y1: dbl.y1, x2: dbl.x2, y2: dbl.y2 }, idx, w, h, {
      ox: w * 0.7,
      oy: h * 0.32,
      scale: Math.min(w, h) * 0.18,
      trail: 80,
    });
    const labels = ["theta1", "omega1", "theta2", "omega2"];
    labels.forEach((label, i) => {
      const x = w * 0.56 + (i % 2) * Math.min(185, w * 0.13);
      const y = h * 0.62 + Math.floor(i / 2) * 78 + Math.sin(elapsed * 2 + i) * 5;
      ctx.strokeStyle = i % 2 ? "oklch(84% 0.16 85)" : "oklch(82% 0.16 205)";
      ctx.lineWidth = 2;
      ctx.strokeRect(x, y, 148, 58);
      ctx.fillStyle = "oklch(94% 0.01 90)";
      ctx.font = "22px ui-monospace, monospace";
      ctx.fillText(label, x + 20, y + 37);
    });
  }

  if (name === "simulation") {
    drawPendulum(ctx, { x1: dbl.x1, y1: dbl.y1, x2: dbl.x2, y2: dbl.y2 }, idx, w, h, {
      ox: w * 0.58,
      oy: h * 0.28,
      scale: Math.min(w, h) * 0.2,
      trail: 220,
    });
  }

  if (name === "energy") {
    drawChart(
      ctx,
      [
        { y: data.energy.kinetic, color: "oklch(82% 0.16 205)" },
        { y: data.energy.potential, color: "oklch(72% 0.22 335)" },
        { y: data.energy.total, color: "oklch(84% 0.16 85)", width: 3 },
      ],
      ["cinetica", "potencial", "total"],
      elapsed,
      w,
      h
    );
  }

  if (name === "divergence") {
    drawChart(
      ctx,
      [{ y: data.divergence.delta, color: "oklch(78% 0.18 145)", width: 3 }],
      ["Delta(t), escala log"],
      elapsed,
      w,
      h,
      "log"
    );
  }

  if (name === "close") {
    const cx = w * 0.5;
    const cy = h * 0.46;
    const r = Math.min(w, h) * 0.18;
    for (let i = 0; i < 4; i += 1) {
      ctx.strokeStyle = ["oklch(82% 0.16 205)", "oklch(84% 0.16 85)", "oklch(72% 0.22 335)", "oklch(78% 0.18 145)"][i];
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.ellipse(cx, cy, r * (1 + i * 0.18), r * (0.42 + i * 0.08), elapsed * 0.35 + i, 0, Math.PI * 2);
      ctx.stroke();
    }
  }
}

function animate(now) {
  const active = slides[current];
  const canvas = active.querySelector("canvas");
  if (canvas) {
    const { ctx, width, height } = fitCanvas(canvas);
    const elapsed = (now - startTime) / 1000;
    renderScene(active.dataset.scene, ctx, elapsed, width, height);
  }
  requestAnimationFrame(animate);
}

document.querySelectorAll("canvas").forEach(fitCanvas);
showSlide(0);
requestAnimationFrame(animate);
