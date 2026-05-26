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
  return [ox + x * scale, oy - y * scale];
}

function drawDashedVertical(ctx, x, y, length, color = "oklch(73% 0.025 275)") {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.globalAlpha = 0.52;
  ctx.lineWidth = 1.4;
  ctx.setLineDash([7, 8]);
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x, y + length);
  ctx.stroke();
  ctx.restore();
}

function drawAngleArc(ctx, cx, cy, ex, ey, radius, label, color) {
  const down = Math.PI / 2;
  const bar = Math.atan2(ey - cy, ex - cx);
  const start = Math.min(down, bar);
  const end = Math.max(down, bar);
  const mid = (start + end) / 2;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, radius, start, end);
  ctx.stroke();
  ctx.font = "17px ui-monospace, monospace";
  ctx.fillText(label, cx + Math.cos(mid) * (radius + 14) - 10, cy + Math.sin(mid) * (radius + 14) + 6);
  ctx.restore();
}

function drawLabel(ctx, text, x, y, color = "oklch(94% 0.01 90)", align = "center") {
  ctx.save();
  ctx.fillStyle = color;
  ctx.font = "18px ui-monospace, monospace";
  ctx.textAlign = align;
  ctx.fillText(text, x, y);
  ctx.restore();
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
  if (options.angles) {
    drawDashedVertical(ctx, ox, oy, scale * 0.72);
    drawDashedVertical(ctx, x1, y1, scale * 0.58);
    drawAngleArc(ctx, ox, oy, x1, y1, Math.min(58, scale * 0.3), "\u03b8\u2081", "oklch(82% 0.16 205)");
    drawAngleArc(ctx, x1, y1, x2, y2, Math.min(48, scale * 0.25), "\u03b8\u2082", "oklch(84% 0.16 85)");
  }
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

function drawGeometry(ctx, elapsed, w, h) {
  const cx = w * 0.68;
  const cy = h * 0.23;
  const L1 = Math.min(w, h) * 0.23;
  const L2 = Math.min(w, h) * 0.20;
  const theta1 = 0.78 + 0.08 * Math.sin(elapsed * 0.8);
  const theta2 = -0.56 + 0.07 * Math.cos(elapsed * 0.9);
  const x1 = L1 * Math.sin(theta1);
  const y1 = L1 * Math.cos(theta1);
  const x2 = x1 + L2 * Math.sin(theta2);
  const y2 = y1 + L2 * Math.cos(theta2);
  const p1x = cx + x1;
  const p1y = cy + y1;
  const p2x = cx + x2;
  const p2y = cy + y2;
  const phase = Math.min(1, (elapsed % 6) / 4.8);

  ctx.save();
  ctx.lineCap = "round";
  drawDashedVertical(ctx, cx, cy, L1 * 1.1);
  drawDashedVertical(ctx, p1x, p1y, L2 * 1.0);
  drawAngleArc(ctx, cx, cy, p1x, p1y, 64, "\u03b8\u2081", "oklch(82% 0.16 205)");
  drawAngleArc(ctx, p1x, p1y, p2x, p2y, 48, "\u03b8\u2082", "oklch(84% 0.16 85)");

  ctx.strokeStyle = "oklch(94% 0.01 90)";
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(cx, cy);
  ctx.lineTo(p1x, p1y);
  ctx.lineTo(p2x, p2y);
  ctx.stroke();

  ctx.fillStyle = "oklch(72% 0.22 335)";
  ctx.beginPath();
  ctx.arc(p1x, p1y, 8, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "oklch(84% 0.16 85)";
  ctx.beginPath();
  ctx.arc(p2x, p2y, 10, 0, Math.PI * 2);
  ctx.fill();

  ctx.setLineDash([8, 8]);
  ctx.lineWidth = 2;
  ctx.globalAlpha = 0.82;
  if (phase > 0.12) {
    ctx.strokeStyle = "oklch(82% 0.16 205)";
    ctx.beginPath();
    ctx.moveTo(cx, p1y);
    ctx.lineTo(p1x, p1y);
    ctx.stroke();
    drawLabel(ctx, "x\u2081", (cx + p1x) / 2, p1y + 27, "oklch(82% 0.16 205)");
  }
  if (phase > 0.28) {
    ctx.strokeStyle = "oklch(72% 0.22 335)";
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx, p1y);
    ctx.stroke();
    drawLabel(ctx, "y\u2081", cx - 28, (cy + p1y) / 2, "oklch(72% 0.22 335)", "right");
  }
  if (phase > 0.48) {
    ctx.strokeStyle = "oklch(84% 0.16 85)";
    ctx.beginPath();
    ctx.moveTo(p1x, p2y);
    ctx.lineTo(p2x, p2y);
    ctx.stroke();
    drawLabel(ctx, "L\u2082 sin(\u03b8\u2082)", (p1x + p2x) / 2, p2y + 27, "oklch(84% 0.16 85)");
  }
  if (phase > 0.64) {
    ctx.strokeStyle = "oklch(78% 0.18 145)";
    ctx.beginPath();
    ctx.moveTo(p1x, p1y);
    ctx.lineTo(p1x, p2y);
    ctx.stroke();
    drawLabel(ctx, "-L\u2082 cos(\u03b8\u2082)", p1x - 25, (p1y + p2y) / 2, "oklch(78% 0.18 145)", "right");
  }
  if (phase > 0.78) {
    ctx.setLineDash([]);
    ctx.strokeStyle = "oklch(78% 0.18 145)";
    ctx.lineWidth = 2.4;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(p2x, p2y);
    ctx.stroke();
    drawLabel(ctx, "(x\u2082, y\u2082)", p2x + 16, p2y - 18, "oklch(94% 0.01 90)", "left");
  }
  ctx.restore();
}

function drawSimple(ctx, elapsed, w, h) {
  const simple = data.simple;
  const idx = Math.floor((elapsed * 48) % simple.x.length);
  const ox = w * 0.30;
  const oy = h * 0.22;
  const scale = Math.min(w, h) * 0.24;
  const x = ox + simple.x[idx] * scale;
  const y = oy - simple.y[idx] * scale;

  drawDashedVertical(ctx, ox, oy, scale * 0.72);

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
  drawAngleArc(ctx, ox, oy, x, y, 52, "\u03b8", "oklch(84% 0.16 85)");
}

function drawChart(ctx, values, labels, elapsed, w, h, mode = "linear", placement = "full", cursor = false) {
  const pad =
    placement === "right"
      ? { left: w * 0.46, right: 70, top: 150, bottom: 110 }
      : placement === "left"
        ? { left: 90, right: w * 0.43, top: 150, bottom: 110 }
        : { left: 90, right: 70, top: 150, bottom: 110 };
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

  if (cursor) {
    const x = x0 + ((end - 1) / (count - 1)) * cw;
    ctx.save();
    ctx.strokeStyle = "oklch(84% 0.16 85)";
    ctx.globalAlpha = 0.75;
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 7]);
    ctx.beginPath();
    ctx.moveTo(x, pad.top);
    ctx.lineTo(x, y0);
    ctx.stroke();
    ctx.restore();
  }
}


function drawAngleSpace(ctx, elapsed, w, h) {
  const dbl = data.double;
  const n = dbl.x1.length;
  const count = Math.max(2, Math.min(n, Math.floor(((elapsed % 8.0) / 7.4) * n)));
  const left = w * 0.08;
  const top = h * 0.14;
  const size = Math.min(w * 0.54, h * 0.70);
  const x0 = left;
  const y0 = top + size;

  function theta1(i) {
    return Math.atan2(dbl.x1[i], -dbl.y1[i]);
  }
  function theta2(i) {
    return Math.atan2(dbl.x2[i] - dbl.x1[i], -(dbl.y2[i] - dbl.y1[i]));
  }
  function map(th1, th2) {
    return [x0 + ((th1 + Math.PI) / (2 * Math.PI)) * size, y0 - ((th2 + Math.PI) / (2 * Math.PI)) * size];
  }

  ctx.save();
  ctx.fillStyle = "rgba(2, 4, 13, 0.52)";
  ctx.fillRect(x0, y0 - size, size, size);
  ctx.strokeStyle = "oklch(31% 0.035 270)";
  ctx.lineWidth = 1;
  ctx.strokeRect(x0, y0 - size, size, size);

  ctx.strokeStyle = "rgba(255,255,255,0.08)";
  for (let i = 1; i < 4; i += 1) {
    const gx = x0 + (i / 4) * size;
    const gy = y0 - (i / 4) * size;
    ctx.beginPath();
    ctx.moveTo(gx, y0 - size);
    ctx.lineTo(gx, y0);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x0, gy);
    ctx.lineTo(x0 + size, gy);
    ctx.stroke();
  }

  ctx.strokeStyle = "rgba(255,255,255,0.22)";
  ctx.setLineDash([5, 7]);
  ctx.beginPath();
  ctx.moveTo(x0 + size / 2, y0 - size);
  ctx.lineTo(x0 + size / 2, y0);
  ctx.moveTo(x0, y0 - size / 2);
  ctx.lineTo(x0 + size, y0 - size / 2);
  ctx.stroke();
  ctx.setLineDash([]);

  const grad = ctx.createLinearGradient(x0, y0, x0 + size, y0 - size);
  grad.addColorStop(0, "oklch(82% 0.16 205)");
  grad.addColorStop(0.55, "oklch(84% 0.16 85)");
  grad.addColorStop(1, "oklch(72% 0.22 335)");
  ctx.strokeStyle = grad;
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  for (let i = 0; i < count; i += 1) {
    const [px, py] = map(theta1(i), theta2(i));
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();

  const [px, py] = map(theta1(count - 1), theta2(count - 1));
  ctx.fillStyle = "oklch(84% 0.16 85)";
  ctx.beginPath();
  ctx.arc(px, py, 6, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "oklch(73% 0.025 275)";
  ctx.font = "15px ui-monospace, monospace";
  ctx.textAlign = "center";
  ctx.fillText("θ₁(t)", x0 + size / 2, y0 + 34);
  ctx.save();
  ctx.translate(x0 - 34, y0 - size / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("θ₂(t)", 0, 0);
  ctx.restore();

  ctx.textAlign = "left";
  ctx.fillStyle = "oklch(94% 0.01 90)";
  ctx.font = "17px ui-monospace, monospace";
  ctx.fillText("un experimento individual", x0, y0 - size - 24);
  ctx.fillStyle = "oklch(84% 0.16 85)";
  ctx.fillText(`muestras: ${count.toLocaleString("es-CO")}`, x0 + size - 160, y0 - size - 24);

  const miniScale = Math.min(w, h) * 0.11;
  const idx = Math.min(n - 1, count - 1);
  drawPendulum(ctx, { x1: dbl.x1, y1: dbl.y1, x2: dbl.x2, y2: dbl.y2 }, idx, w, h, {
    ox: w * 0.78,
    oy: h * 0.23,
    scale: miniScale,
    trail: 60,
    color: "oklch(82% 0.16 205)",
    bob: "oklch(84% 0.16 85)",
    angles: true,
  });

  ctx.fillStyle = "oklch(73% 0.025 275)";
  ctx.font = "16px system-ui, sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("La animación física y la curva angular son el mismo movimiento visto desde dos coordenadas.", w * 0.62, h * 0.54);
  ctx.restore();
}

function drawEomOverlay(ctx, elapsed, w, h) {
  const x = w * 0.64;
  const y = h * 0.58;
  const pulse = 0.55 + 0.45 * Math.sin(elapsed * 2.1) ** 2;
  ctx.save();
  ctx.font = "20px ui-monospace, monospace";
  ctx.fillStyle = "oklch(94% 0.01 90)";
  ctx.fillText("ecuaciones acopladas", x, y);
  ctx.font = "18px ui-monospace, monospace";
  ctx.fillStyle = "oklch(82% 0.16 205)";
  ctx.fillText("\u03b8\u0308\u2081 = f(\u03b8\u2081, \u03b8\u2082, \u03c9\u2081, \u03c9\u2082)", x, y + 44);
  ctx.fillStyle = "oklch(84% 0.16 85)";
  ctx.fillText("\u03b8\u0308\u2082 = g(\u03b8\u2081, \u03b8\u2082, \u03c9\u2081, \u03c9\u2082)", x, y + 82);
  ctx.globalAlpha = pulse;
  ctx.fillStyle = "oklch(72% 0.22 335)";
  ctx.fillText("términos cruzados + senos/cosenos", x, y + 126);
  ctx.restore();
}


function flipColor(value, tMax) {
  if (!Number.isFinite(value)) return "rgba(5, 7, 18, 0.92)";
  const v = Math.max(0, Math.min(1, value / Math.max(tMax, 1e-9)));
  if (v >= 0.995) return "rgba(2, 4, 13, 0.95)";
  if (v < 0.18) return "rgba(50, 105, 232, 0.94)";
  if (v < 0.36) return "rgba(38, 199, 229, 0.94)";
  if (v < 0.56) return "rgba(80, 236, 142, 0.94)";
  if (v < 0.74) return "rgba(236, 221, 72, 0.94)";
  if (v < 0.90) return "rgba(250, 125, 38, 0.94)";
  return "rgba(196, 29, 29, 0.94)";
}

function renderMap(ctx, elapsed, w, h) {
  const payload = data.map || {};
  ctx.save();
  ctx.fillStyle = "rgba(2, 4, 13, 0.95)";
  ctx.fillRect(0, 0, w, h);

  const size = Math.min(w * 0.78, h * 0.78);
  const x0 = (w - size) / 2;
  const y0 = (h - size) / 2;
  const rows = payload.flipTimes?.length || 0;
  const cols = rows ? payload.flipTimes[0].length : 0;
  const tMax = payload.tMax || 18;

  ctx.strokeStyle = "oklch(31% 0.035 270)";
  ctx.lineWidth = 1;
  ctx.strokeRect(x0, y0, size, size);

  if (!rows || !cols) {
    ctx.fillStyle = "oklch(94% 0.01 90)";
    ctx.font = "18px ui-monospace, monospace";
    ctx.textAlign = "center";
    ctx.fillText("mapa no cargado: ejecuta scripts/export_presentation_data.py", w / 2, h / 2);
    ctx.restore();
    return;
  }

  const cellW = size / cols;
  const cellH = size / rows;
  const progress = Math.min(1, elapsed / 4.4);
  const revealCols = Math.max(1, Math.floor(cols * progress));

  for (let r = 0; r < rows; r += 1) {
    for (let c = 0; c < revealCols; c += 1) {
      const value = payload.flipTimes[r][c];
      ctx.fillStyle = flipColor(value, tMax);
      ctx.fillRect(x0 + c * cellW, y0 + (rows - 1 - r) * cellH, Math.ceil(cellW) + 0.5, Math.ceil(cellH) + 0.5);
    }
  }

  const scanX = x0 + revealCols * cellW;
  ctx.save();
  ctx.strokeStyle = "oklch(84% 0.16 85)";
  ctx.globalAlpha = 0.8;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(scanX, y0);
  ctx.lineTo(scanX, y0 + size);
  ctx.stroke();
  ctx.restore();

  function mapTheta(theta1, theta2) {
    return [x0 + ((theta1 + Math.PI) / (2 * Math.PI)) * size, y0 + size - ((theta2 + Math.PI) / (2 * Math.PI)) * size];
  }

  if (elapsed > 2.6) {
    ctx.save();
    ctx.strokeStyle = "rgba(255, 255, 255, 0.78)";
    ctx.lineWidth = 1.8;
    ctx.setLineDash([7, 6]);
    [1, -1].forEach((branch) => {
      ctx.beginPath();
      let first = true;
      for (let i = 0; i <= 220; i += 1) {
        const th1 = -Math.PI + (2 * Math.PI * i) / 220;
        const rhs = 2 - 3 * Math.cos(th1);
        if (rhs < -1 || rhs > 1) {
          first = true;
          continue;
        }
        const th2 = branch * Math.acos(rhs);
        const [px, py] = mapTheta(th1, th2);
        if (first) {
          ctx.moveTo(px, py);
          first = false;
        } else {
          ctx.lineTo(px, py);
        }
      }
      ctx.stroke();
    });
    ctx.setLineDash([]);
    ctx.fillStyle = "rgba(255, 255, 255, 0.82)";
    ctx.font = "13px ui-monospace, monospace";
    ctx.textAlign = "left";
    ctx.fillText("frontera energética", x0 + 16, y0 + 24);
    ctx.restore();
  }

  ctx.fillStyle = "oklch(73% 0.025 275)";
  ctx.font = "14px ui-monospace, monospace";
  ctx.textAlign = "center";
  ctx.fillText("θ₁(0) [rad]", x0 + size / 2, y0 + size + 34);
  ctx.save();
  ctx.translate(x0 - 34, y0 + size / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.fillText("θ₂(0) [rad]", 0, 0);
  ctx.restore();

  const resolved = revealCols * rows;
  ctx.textAlign = "right";
  ctx.fillStyle = "oklch(94% 0.01 90)";
  ctx.font = "15px ui-monospace, monospace";
  ctx.fillText(`${resolved.toLocaleString("es-CO")} condiciones iniciales resueltas`, x0 + size, y0 - 18);
  ctx.textAlign = "left";
  ctx.fillStyle = "oklch(84% 0.16 85)";
  ctx.fillText("un pixel = una integración", x0, y0 - 18);
  ctx.restore();
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
      angles: true,
    });
    const labels = ["\u03b8\u2081", "\u03c9\u2081", "\u03b8\u2082", "\u03c9\u2082"];
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

  if (name === "geometry") {
    drawGeometry(ctx, elapsed, w, h);
  }

  if (name === "simulation") {
    drawPendulum(ctx, { x1: dbl.x1, y1: dbl.y1, x2: dbl.x2, y2: dbl.y2 }, idx, w, h, {
      ox: w * 0.58,
      oy: h * 0.28,
      scale: Math.min(w, h) * 0.2,
      trail: 220,
      angles: true,
    });
    drawEomOverlay(ctx, elapsed, w, h);
  }

  if (name === "angle-space") {
    drawAngleSpace(ctx, elapsed, w, h);
  }

  if (name === "energy") {
    drawChart(
      ctx,
      [
        { y: data.energy.kinetic, color: "oklch(82% 0.16 205)" },
        { y: data.energy.potential, color: "oklch(72% 0.22 335)" },
        { y: data.energy.total, color: "oklch(84% 0.16 85)", width: 3 },
      ],
      ["cinética", "potencial", "total"],
      elapsed,
      w,
      h,
      "linear",
      "right"
    );
  }

  if (name === "divergence") {
    drawPendulum(ctx, { x1: dbl.x1, y1: dbl.y1, x2: dbl.x2, y2: dbl.y2 }, idx, w, h, {
      ox: w * 0.78,
      oy: h * 0.28,
      scale: Math.min(w, h) * 0.12,
      trail: 70,
      color: "oklch(82% 0.16 205)",
      bob: "oklch(84% 0.16 85)",
    });
    drawPendulum(ctx, { x1: dbl.xb1, y1: dbl.yb1, x2: dbl.xb2, y2: dbl.yb2 }, idx, w, h, {
      ox: w * 0.78,
      oy: h * 0.28,
      scale: Math.min(w, h) * 0.12,
      trail: 70,
      color: "oklch(78% 0.18 145)",
      bob: "oklch(78% 0.18 145)",
    });
    drawChart(
      ctx,
      [{ y: data.divergence.delta, color: "oklch(78% 0.18 145)", width: 3 }],
      ["Δ(t), escala log"],
      elapsed,
      w,
      h,
      "log",
      "left",
      true
    );
  }

  if (name === "map") {
    renderMap(ctx, elapsed, w, h);
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
