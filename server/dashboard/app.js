/* ==========================================================================
   SENTRYX — app.js
   Shared shell behavior + FastAPI integration for all pages.

   BACKEND CONTRACT
   -----------------------------------------------------------------------
   GET /systems          -> array of endpoint/system records
   GET /resource-usage    -> array of { id, system_id, cpu_usage, memory_usage,
                                         disk_usage, timestamp }
   GET /alerts            -> array of alert records

   The exact field names returned by /systems and /alerts weren't part of
   the brief beyond the columns requested, so this file normalizes a few
   likely key spellings (snake_case / camelCase) into a canonical shape.
   If your FastAPI schema uses different names, adjust ONLY the `normalize*`
   functions below — every renderer reads from the normalized object.
   ========================================================================== */

const SENTRYX = (() => {

  /* ---------------- Config ---------------- */
  const API_BASE = window.SENTRYX_API_BASE || "http://localhost:8000";
  const POLL_INTERVAL_MS = 10000;
  const ENDPOINTS = {
    systems: `${API_BASE}/systems`,
    resourceUsage: `${API_BASE}/resource-usage`,
    alerts: `${API_BASE}/alerts`,
    processes: `${API_BASE}/processes`,
    mlStatus: `${API_BASE}/ml-status`,
  };

  /* ---------------- Generic fetch helper ---------------- */
  async function getJSON(url, { timeout = 8000 } = {}) {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), timeout);
    try {
      const res = await fetch(url, { signal: controller.signal, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setConnectionState(true);
      return Array.isArray(data) ? data : (data?.results ?? data?.data ?? []);
    } catch (err) {
      setConnectionState(false);
      throw err;
    } finally {
      clearTimeout(t);
    }
  }

  /* ---------------- Connection indicator ---------------- */
  let connectionOK = null;
  function setConnectionState(ok) {
    if (connectionOK === ok) return;
    connectionOK = ok;
    const pill = document.getElementById("connPill");
    if (!pill) return;
    const stat = pill.querySelector(".stat");
    const dot = pill.querySelector(".live-dot");
    if (ok) {
      stat.textContent = "ONLINE";
      stat.className = "stat ok";
      dot.classList.remove("danger");
    } else {
      stat.textContent = "OFFLINE";
      stat.className = "stat bad";
      dot.classList.add("danger");
    }
  }

  /* ---------------- Normalizers ---------------- */
  function pick(obj, keys, fallback = undefined) {
    for (const k of keys) {
      if (obj && obj[k] !== undefined && obj[k] !== null && obj[k] !== "") return obj[k];
    }
    return fallback;
  }

function normalizeSystem(s) {
  return {
    id: pick(s, ["id", "system_id", "uuid"], cryptoId()),
    hostname: pick(s, ["hostname", "host_name", "name"], "Unknown"),

    os: pick(s, ["os_name", "os", "operating_system", "platform"], "Unknown"),

    osVersion: pick(s, ["os_release", "os_version", "version"], ""),

    architecture: pick(s, ["architecture"], ""),

    processor: pick(s, ["processor", "cpu_model", "cpu_name"], "Unknown CPU"),

    cpuCount: pick(s, ["cpu_count", "cores"], "—"),

    pythonVersion: pick(s, ["python_version"], "—"),

    lastSeen: pick(
      s,
      ["last_seen", "updated_at", "timestamp", "created_at"],
      null
    ),

    ip: pick(s, ["ip_address", "ip"], ""),

    raw: s,
  };
}
  function normalizeAlert(a) {
    return {
      id: pick(a, ["id", "alert_id", "uuid"], cryptoId()),
      systemId: pick(a, ["system_id", "systemId", "host_id"], null),
      hostname: pick(a, ["hostname", "host_name", "system_name"], null),
      type: pick(a, ["alert_type", "type", "category"], "Unclassified Event"),
      severity: String(pick(a, ["severity", "level", "risk_level"], "low")).toLowerCase(),
      status: String(pick(a, ["status", "state"], "open")).toLowerCase(),
      message: pick(a, ["message", "description", "details"], ""),
      timestamp: pick(a, ["timestamp", "created_at", "detected_at", "time"], null),
      raw: a,
    };
  }

  function normalizeUsage(u) {
    return {
      id: pick(u, ["id"], cryptoId()),
      systemId: pick(u, ["system_id", "systemId"], null),
      hostname: pick(u, ["hostname", "host_name", "system_name"], null),
      cpu: numOrNull(pick(u, ["cpu_usage", "cpu"], null)),
      memory: numOrNull(pick(u, ["memory_usage", "memory", "mem_usage"], null)),
      disk: numOrNull(pick(u, ["disk_usage", "disk"], null)),
      timestamp: pick(u, ["timestamp", "created_at"], null),
      raw: u,
    };
  }

  function normalizeProcess(p) {
    return {
      pid:       pick(p, ["pid", "process_id"], "—"),
      name:      pick(p, ["process_name", "name", "proc_name"], "unknown"),
      exePath:   pick(p, ["exe_path", "executable_path", "exe", "path"], "—"),
      hostname: pick(p, ["hostname", "host_name"], "—"),
      cpu:       numOrNull(pick(p, ["cpu_usage", "cpu_percent", "cpu"], null)),
      memory:    numOrNull(pick(p, ["memory_usage", "mem_usage", "memory_percent", "memory"], null)),
      status:    String(pick(p, ["status", "state"], "unknown")).toLowerCase(),
      riskLevel: String(pick(p, ["risk_level", "risk", "severity"], "low")).toLowerCase(),
      raw: p,
    };
  }

    function numOrNull(v) { const n = parseFloat(v); return Number.isFinite(n) ? n : null; }
  function cryptoId() { return "tmp_" + Math.random().toString(36).slice(2, 10); }

  /* ---------------- Time helpers ---------------- */
  function timeAgo(ts) {
    if (!ts) return "—";
    const d = new Date(ts.replace ? ts.replace(" ", "T") : ts);
    if (isNaN(d)) return "—";
    const diff = Math.max(0, (Date.now() - d.getTime()) / 1000);
    if (diff < 60) return `${Math.floor(diff)}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  }
  function isRecent(ts, withinMs = 90000) {
    if (!ts) return false;
    const d = new Date(ts.replace ? ts.replace(" ", "T") : ts);
    if (isNaN(d)) return false;
    return (Date.now() - d.getTime()) <= withinMs;
  }
  function fmtClock(date) {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
  }

  /* ---------------- Icons (inline SVG, stroke-based) ---------------- */
  const ICONS = {
    shield: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l7 3v6c0 5-3.5 7.5-7 9-3.5-1.5-7-4-7-9V6l7-3z"/></svg>`,
    server: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="6" rx="1.4"/><rect x="3" y="14" width="18" height="6" rx="1.4"/><circle cx="7" cy="7" r=".6" fill="currentColor"/><circle cx="7" cy="17" r=".6" fill="currentColor"/></svg>`,
    alertTri: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 4l9 16H3z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6" fill="currentColor"/></svg>`,
    check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 13l4 4L19 7"/></svg>`,
    activity: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 12h4l2 7 4-14 2 7h6"/></svg>`,
    heart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 12h4l2 9 4-18 2 9h6"/></svg>`,
    search: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>`,
    grid: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="8" height="8" rx="1.5"/><rect x="13" y="3" width="8" height="8" rx="1.5"/><rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/></svg>`,
    monitor: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="4" width="18" height="13" rx="1.5"/><path d="M8 21h8M12 17v4"/></svg>`,
    siren: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 9a4 4 0 0 1 4 4v4H8v-4a4 4 0 0 1 4-4z"/><path d="M12 3v2M5 13H3M21 13h-2M6.3 6.3 5 5M17.7 6.3 19 5"/><rect x="6" y="17" width="12" height="3" rx="1"/></svg>`,
    brain: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-1.5 5.5A3 3 0 0 0 7 18a3 3 0 0 0 5 1.8A3 3 0 0 0 17 18a3 3 0 0 0 2.5-5.5A3 3 0 0 0 18 7a3 3 0 0 0-4-2.8A3 3 0 0 0 9 4z"/><path d="M9 4v16M15 4v16"/></svg>`,
    bolt: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg>`,
    lock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="5" y="11" width="14" height="9" rx="1.5"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>`,
    close: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6 6 18"/></svg>`,
    menu: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M4 12h16M4 17h16"/></svg>`,
    windows: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 5.5 10.5 4.4v7.1H3zM11.5 4.3 21 3v8.4H11.5zM3 12.5h7.5v7.1L3 18.5zM11.5 12.5H21V21l-9.5-1.3z"/></svg>`,
    linux: `<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" opacity=".15"/><path d="M9 9.5c0-.8.6-1.5 1.5-1.5h3c.9 0 1.5.7 1.5 1.5v2c0 .8-.6 1.5-1.5 1.5h-3C9.6 13 9 12.3 9 11.5v-2z"/></svg>`,
    apple: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.4 12.4c0-1.7 1-2.7 1-2.7s-1-1.4-2.6-1.4c-1.2 0-1.8.6-2.8.6s-1.7-.6-2.8-.6c-1.5 0-3.1 1.2-3.1 3.6 0 2.1 1.7 5.6 3.4 5.6.9 0 1.3-.6 2.4-.6s1.4.6 2.4.6c1.4 0 2.6-2.4 3-3.3-1-.4-1.9-1.2-1.9-1.8z"/></svg>`,
  };

  function osIcon(os) {
    const o = (os || "").toLowerCase();
    if (o.includes("win")) return ICONS.windows;
    if (o.includes("mac") || o.includes("darwin") || o.includes("ios")) return ICONS.apple;
    return ICONS.linux;
  }

  /* ---------------- Shell behavior (sidebar / clock / nav) ---------------- */
  function initShell() {
    const page = document.body.dataset.page;
    document.querySelectorAll(".nav-item").forEach((el) => {
      if (el.dataset.page === page) el.classList.add("active");
    });

    const toggle = document.getElementById("menuToggle");
    const sidebar = document.getElementById("sidebar");
    const scrim = document.getElementById("sidebarScrim");
    if (toggle && sidebar && scrim) {
      toggle.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        scrim.classList.toggle("show");
      });
      scrim.addEventListener("click", () => {
        sidebar.classList.remove("open");
        scrim.classList.remove("show");
      });
    }

    const clockEl = document.getElementById("clock");
    if (clockEl) {
      const tick = () => { clockEl.textContent = fmtClock(new Date()); };
      tick();
      setInterval(tick, 1000);
    }
  }

  /* ---------------- Empty / error / loading state builders ---------------- */
  function loadingRows(cols, rows = 4) {
    return Array.from({ length: rows }).map(() =>
      `<tr>${Array.from({ length: cols }).map(() => `<td><div class="skel skel-row w-60"></div></td>`).join("")}</tr>`
    ).join("");
  }

  function emptyState({ icon = ICONS.server, title, body }) {
    return `<div class="state-block">${icon}<h4>${title}</h4><p>${body}</p></div>`;
  }

  function errorState(retryFn, label = "data") {
    const id = "retry_" + Math.random().toString(36).slice(2, 8);
    setTimeout(() => {
      const btn = document.getElementById(id);
      if (btn) btn.addEventListener("click", retryFn);
    }, 0);
    return `<div class="state-block">
      ${ICONS.alertTri}
      <h4>Couldn't reach the API</h4>
      <p>SENTRYX could not load ${label}. Check that your FastAPI server is running and reachable at <span class="mono">${API_BASE}</span>.</p>
      <button id="${id}" class="btn primary">Retry now</button>
    </div>`;
  }

  return {
    API_BASE, POLL_INTERVAL_MS, ENDPOINTS, ICONS,
    getJSON, normalizeSystem, normalizeAlert, normalizeUsage, normalizeProcess,
    timeAgo, isRecent, fmtClock, osIcon,
    initShell, loadingRows, emptyState, errorState,
  };
})();


document.addEventListener("DOMContentLoaded", SENTRYX.initShell);