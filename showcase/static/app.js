async function loadSummary() {
  const candidates = ["api/summary", "data/summary.json"];
  let data = null;
  let lastError = null;

  for (const url of candidates) {
    try {
      const res = await fetch(url, { cache: "no-store" });
      if (!res.ok) throw new Error(`${url} ${res.status}`);
      data = await res.json();
      break;
    } catch (err) {
      lastError = err;
    }
  }

  if (!data) throw lastError || new Error("summary data unavailable");

  const domains = data.project?.domains || [];
  const metricDomains = document.querySelector("#metric-domains");
  if (metricDomains && domains.length) metricDomains.textContent = `${domains.length}+`;

  const goal = document.querySelector("#seed-goal");
  if (goal && data.project?.goal) goal.textContent = data.project.goal;

  const deliverables = document.querySelector("#deliverables");
  if (deliverables && data.project?.deliverables?.length) {
    deliverables.innerHTML = data.project.deliverables
      .map(item => `<span class="chip">${item}</span>`)
      .join("");
  }

  const stats = document.querySelector("#sample-stats");
  if (stats && data.seed) {
    const statRows = [
      ["种子样例", data.seed.sample_count],
      ["领域覆盖", Object.keys(data.seed.domains || {}).length],
      ["题型覆盖", Object.keys(data.seed.question_types || {}).length],
      ["认知层级", Object.keys(data.seed.cognitive_levels || {}).join(" / ")]
    ];
    stats.innerHTML = statRows.map(([label, value]) => `
      <div class="stat-row"><span>${label}</span><b>${value || "-"}</b></div>
    `).join("");
  }

  const coverage = document.querySelector("#coverage");
  if (coverage && data.seed?.coverage?.length) {
    coverage.innerHTML = data.seed.coverage.map(row => `
      <tr>
        <td>${row["领域"]}</td>
        <td>${row["知识记忆C1"]}</td>
        <td>${row["理解应用C2"]}</td>
        <td>${row["分析推理C3"]}</td>
        <td>${row["动态交互C4"]}</td>
        <td>${row["目标样本量"]}</td>
      </tr>
    `).join("");
  }
}

loadSummary().catch(err => {
  console.error(err);
  const stats = document.querySelector("#sample-stats");
  if (stats) {
    stats.innerHTML = `
      <div class="stat-row"><span>种子样例</span><b>4</b></div>
      <div class="stat-row"><span>领域覆盖</span><b>4</b></div>
      <div class="stat-row"><span>题型覆盖</span><b>4</b></div>
      <div class="stat-row"><span>认知层级</span><b>C1 / C2 / C3 / C4</b></div>
    `;
  }
});
