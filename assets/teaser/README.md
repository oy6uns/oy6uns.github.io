# Publication teaser figures

One figure per publication, in the order they appear on `/publications/`.

| File | Publication | Venue |
| --- | --- | --- |
| `hwang2026maritime.png` | Redefining Maritime Anomaly Detection via Equation-Grounded Synthetic Anomalies | KDD 2026 |
| `bae2026toolfailures.png` | Beyond Tool Selection: Diagnosing Downstream Failures in MCP Tool-Using LLM Agents | ICML Workshop on FAGEN 2026 |
| `bae2026aisflow.png` | AISFlow: Boundary-Informed Flow Matching for Long-Term AIS Trajectory Imputation | ICML Workshop on AI for Science 2026 |
| `kim2025stgbenchmark.png` | Spatio-Temporal Graphs Beyond Grids: Benchmark for Maritime Anomaly Detection | NeurIPS Workshop on AI for Science 2025 |
| `kim2025stgvad.png` | STGVAD: Spatio-Temporal Graph-Based Vessel Behavior Anomaly Detection | IEEE Access 2025 |
| `bae2024smartmeter.png` | Socio-demographic Information Estimation via Smart Meter Data Analysis and Feature Selection | ICTC 2024 |
| `bae2024palmoil.png` | Deep Learning-Based Short-Term Time Series Forecasting Modeling for Palm Oil Price Prediction | Information Systems Review 2024 |

## Adding a new one

Downscale to 960 px wide, then reference it from the publication entry:

```html
<a class="pub-thumb" href="LINK_TO_PAPER" target="_blank" rel="noreferrer">
  <img src="assets/teaser/yourfile.png" alt="One line describing the figure" loading="lazy" />
</a>
```

From `publications/index.html` the path is `../assets/teaser/...`.

The thumbnail box takes its height from the image, so any aspect ratio works and
nothing gets cropped. In dark mode the figures are dimmed slightly by CSS so the
white backgrounds don't glare.
