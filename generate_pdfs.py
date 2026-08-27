import os
import re
import subprocess
from pathlib import Path
from markdown_it import MarkdownIt

md = MarkdownIt().enable("table")

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(CHROME_PATH):
    CHROME_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CLAY_BLACK_WHITE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

@page {
    size: A4 portrait;
    margin: 14mm 12mm 14mm 12mm;
    background-color: #000000;
}

*, *::before, *::after {
    box-sizing: border-box;
}

html, body {
    background-color: #000000;
    color: #e2e8f0;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 12.5px;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

/* Header & Brand Banner */
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0d0d11;
    padding: 9px 16px;
    margin-bottom: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.6),
                -2px -2px 6px rgba(255, 255, 255, 0.04),
                inset 1px 1px 2px rgba(255, 255, 255, 0.15),
                inset -1px -1px 2px rgba(0, 0, 0, 0.5);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
}

.brand-tag {
    color: #ffffff;
    font-weight: 800;
    display: flex;
    align-items: center;
    gap: 8px;
}

.brand-pill {
    background: #ffffff;
    color: #000000;
    padding: 2px 8px;
    border-radius: 9999px;
    font-weight: 800;
    font-size: 9px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.5), inset 1px 1px 1px rgba(255,255,255,0.9), inset -1px -1px 2px rgba(0,0,0,0.3);
}

.doc-tag {
    color: #94a3b8;
    font-weight: 600;
}

.footer-bar {
    margin-top: 30px;
    padding: 10px 16px;
    background: #0d0d11;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.6),
                -2px -2px 6px rgba(255, 255, 255, 0.03),
                inset 1px 1px 2px rgba(255, 255, 255, 0.1),
                inset -1px -1px 2px rgba(0, 0, 0, 0.4);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: #94a3b8;
    page-break-inside: avoid;
}

.footer-bar .author-credit {
    color: #ffffff;
    font-weight: 800;
    border-bottom: 1.5px solid #ffffff;
    padding-bottom: 1px;
}

/* Headings */
h1 {
    color: #ffffff;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-top: 0;
    margin-bottom: 14px;
    padding: 12px 16px;
    background: #111116;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.16);
    box-shadow: 6px 6px 14px rgba(0, 0, 0, 0.7),
                -3px -3px 8px rgba(255, 255, 255, 0.05),
                inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.2),
                inset -1.5px -1.5px 3px rgba(0, 0, 0, 0.6);
}

h2 {
    color: #ffffff;
    font-size: 15.5px;
    font-weight: 700;
    letter-spacing: -0.3px;
    margin-top: 22px;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1.5px solid rgba(255, 255, 255, 0.2);
    page-break-after: avoid;
    display: flex;
    align-items: center;
    gap: 8px;
}

h2::before {
    content: "■";
    font-size: 9px;
    color: #ffffff;
}

h3 {
    color: #f1f5f9;
    font-size: 13.5px;
    font-weight: 700;
    margin-top: 16px;
    margin-bottom: 6px;
    page-break-after: avoid;
}

h4 {
    color: #e2e8f0;
    font-size: 12.5px;
    font-weight: 600;
    margin-top: 12px;
    margin-bottom: 4px;
    page-break-after: avoid;
}

p {
    margin-top: 0;
    margin-bottom: 10px;
    color: #cbd5e1;
}

strong {
    color: #ffffff;
    font-weight: 700;
}

em {
    color: #ffffff;
    font-style: italic;
}

/* ======================================================== */
/* CLAYMORPHIC GRAPHS, COMPARISON CARDS & METRIC WIDGETS   */
/* ======================================================== */

/* 1. VPN Provider Comparison Cards */
.comparison-grid {
    display: flex;
    gap: 14px;
    margin: 18px 0;
    page-break-inside: avoid;
}

.comp-card {
    flex: 1;
    background: #0f0f14;
    border-radius: 14px;
    padding: 16px 16px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6),
                -3px -3px 8px rgba(255, 255, 255, 0.04),
                inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.15),
                inset -1.5px -1.5px 3px rgba(0, 0, 0, 0.6);
}

.comp-header {
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 12px;
    margin-bottom: 12px;
}

.comp-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.badge-warning {
    background: #23232b;
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: inset 1px 1px 2px rgba(255,255,255,0.2);
}

.badge-success {
    background: #ffffff;
    color: #000000;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.5), inset 1px 1px 2px rgba(255,255,255,0.9), inset -1px -1px 2px rgba(0,0,0,0.3);
}

.comp-score-box {
    margin-top: 6px;
}

.score-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: #94a3b8;
    margin-bottom: 4px;
}

.score-bar-bg {
    height: 7px;
    background: #181822;
    border-radius: 9999px;
    overflow: hidden;
    margin: 4px 0;
    box-shadow: inset 1px 1px 3px rgba(0,0,0,0.8);
    border: 1px solid rgba(255,255,255,0.06);
}

.score-bar-fill {
    height: 100%;
    border-radius: 9999px;
}

.fill-low {
    background: #94a3b8;
    box-shadow: 0 0 6px rgba(255,255,255,0.2);
}

.fill-high {
    background: #ffffff;
    box-shadow: 0 0 8px rgba(255,255,255,0.6);
}

.score-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: #ffffff;
}

.comp-row {
    margin-bottom: 10px;
    font-size: 11.5px;
}

.comp-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 2px;
}

.comp-val {
    color: #cbd5e1;
    font-weight: 500;
}

.val-negative {
    color: #cbd5e1;
}

.val-positive {
    color: #ffffff;
    font-weight: 700;
}

.val-neutral {
    color: #94a3b8;
}

/* 2. Network Flow Graph */
.network-flow-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    background: #0d0d12;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6), inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.15);
    margin: 16px 0;
    page-break-inside: avoid;
}

.flow-step {
    flex: 1;
    background: #14141a;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: inset 1px 1px 2px rgba(255,255,255,0.1), 3px 3px 8px rgba(0,0,0,0.5);
}

.highlight-step {
    border: 1.5px solid #ffffff;
}

.flow-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: #94a3b8;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

.flow-title {
    color: #ffffff;
    font-weight: 700;
    font-size: 12px;
    margin-bottom: 6px;
}

.flow-pill {
    display: inline-block;
    background: #1e1e28;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 9999px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 4px;
}

.public-pill {
    background: #ffffff;
    color: #000000;
}

.flow-desc {
    font-size: 10px;
    color: #94a3b8;
}

.flow-arrow {
    text-align: center;
    color: #ffffff;
    font-weight: 800;
}

.arrow-symbol {
    font-size: 16px;
}

.arrow-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    color: #94a3b8;
    max-width: 60px;
    line-height: 1.1;
}

/* 3. DNS Resolution Graph */
.dns-tree-container {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #0d0d12;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6), inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.15);
    margin: 16px 0;
    page-break-inside: avoid;
}

.dns-node {
    flex: 1;
    background: #14141a;
    padding: 10px 12px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.dns-pill {
    display: inline-block;
    background: #ffffff;
    color: #000000;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 9999px;
    margin-bottom: 4px;
}

.dns-title {
    color: #ffffff;
    font-weight: 700;
    font-size: 11.5px;
}

.dns-desc {
    color: #94a3b8;
    font-size: 10px;
}

.dns-arrow {
    color: #ffffff;
    font-weight: 800;
    font-size: 14px;
}

.dns-tier-group {
    flex: 1.2;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.dns-subnode {
    background: #181822;
    padding: 5px 10px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.highlight-subnode {
    border: 1px solid #ffffff;
    color: #ffffff;
    font-weight: 700;
}

/* 4. MAC Byte Split Graph */
.mac-breakdown-card {
    background: #0d0d12;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6), inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.15);
    margin: 16px 0;
    page-break-inside: avoid;
}

.mac-hex-display {
    display: flex;
    gap: 12px;
}

.mac-block {
    flex: 1;
    background: #14141a;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    text-align: center;
}

.mac-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: #94a3b8;
    letter-spacing: 1px;
    margin-bottom: 6px;
}

.mac-hex {
    font-family: 'JetBrains Mono', monospace;
    font-size: 18px;
    font-weight: 800;
    color: #ffffff;
    background: #1c1c26;
    padding: 6px 12px;
    border-radius: 8px;
    display: inline-block;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 8px;
}

.mac-label {
    color: #ffffff;
    font-weight: 700;
    font-size: 11.5px;
}

.mac-sub {
    color: #94a3b8;
    font-size: 10px;
}

/* 5. Layer 2 Hop-by-Hop Stripping */
.layer2-flow-container {
    background: #0d0d12;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    margin: 16px 0;
    page-break-inside: avoid;
}

.layer2-card {
    background: #14141a;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.l2-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 800;
    color: #ffffff;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 4px;
    margin-bottom: 6px;
}

.l2-body {
    display: flex;
    flex-direction: column;
    gap: 3px;
    font-size: 11px;
}

.l2-key {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: #94a3b8;
}

.l2-val {
    color: #e2e8f0;
    font-weight: 600;
}

.val-client {
    color: #ffffff;
    font-weight: 800;
}

.l2-badge {
    display: inline-block;
    padding: 1px 8px;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 700;
}

.layer2-divider {
    display: flex;
    align-items: center;
    margin: 10px 0;
}

.divider-line {
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.15);
}

.divider-badge {
    padding: 3px 12px;
    background: #ffffff;
    color: #000000;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 800;
    border-radius: 9999px;
    margin: 0 10px;
}

/* 6. GeoIP Inspector & Meters */
.geoip-inspector {
    background: #0d0d12;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6), inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.15);
    margin: 16px 0;
    page-break-inside: avoid;
}

.geoip-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 10px;
    margin-bottom: 12px;
}

.geoip-pill {
    background: #ffffff;
    color: #000000;
    padding: 3px 10px;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 800;
}

.geoip-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    color: #94a3b8;
}

.geoip-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-bottom: 14px;
}

.geoip-stat {
    background: #14141a;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 11px;
}

.stat-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #94a3b8;
}

.stat-val {
    color: #ffffff;
    font-weight: 700;
    margin-left: 4px;
}

.stat-danger {
    color: #ffffff;
    text-decoration: underline;
}

.geoip-meters {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.meter-row {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 11px;
}

.meter-lbl {
    width: 170px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #cbd5e1;
}

.meter-bar {
    flex: 1;
    height: 7px;
    background: #181822;
    border-radius: 9999px;
    overflow: hidden;
    box-shadow: inset 1px 1px 3px rgba(0,0,0,0.8);
    border: 1px solid rgba(255,255,255,0.06);
}

.meter-fill {
    height: 100%;
    background: #ffffff;
    border-radius: 9999px;
}

.fill-zero {
    background: transparent;
}

.meter-pct {
    width: 140px;
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: #ffffff;
}

/* 7. 4-Card Vector Grid */
.vector-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 16px 0;
    page-break-inside: avoid;
}

.vector-card {
    background: #0f0f14;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5), inset 1px 1px 2px rgba(255, 255, 255, 0.12);
}

.vector-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 800;
    margin-bottom: 8px;
}

.badge-critical {
    background: #ffffff;
    color: #000000;
}

.badge-high {
    background: #24242e;
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.2);
}

.badge-med {
    background: #181820;
    color: #94a3b8;
    border: 1px solid rgba(255,255,255,0.1);
}

.vector-title {
    color: #ffffff;
    font-size: 12.5px;
    font-weight: 700;
    margin-bottom: 4px;
}

.vector-desc {
    color: #94a3b8;
    font-size: 10.5px;
    line-height: 1.4;
    margin-bottom: 8px;
}

.vector-stat {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #cbd5e1;
}

/* 8. VPN Tunnel Comparison */
.vpn-tunnel-comparison {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 16px 0;
    page-break-inside: avoid;
}

.tunnel-card {
    background: #0d0d12;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
}

.tunnel-unprotected {
    border-left: 4px solid #64748b;
}

.tunnel-protected {
    border-left: 4px solid #ffffff;
}

.tunnel-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
    letter-spacing: 1px;
}

.tunnel-flow {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
}

.t-node {
    background: #181822;
    padding: 4px 8px;
    border-radius: 6px;
    color: #ffffff;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.08);
}

.t-arrow-red {
    color: #94a3b8;
    font-size: 9px;
}

.t-arrow-green {
    color: #ffffff;
    font-weight: 700;
    font-size: 9px;
}

/* 9. Defense Stack */
.defense-stack-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin: 16px 0;
    page-break-inside: avoid;
}

.stack-layer {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #0f0f14;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.5), inset 1px 1px 2px rgba(255, 255, 255, 0.1);
}

.layer-pill {
    background: #ffffff;
    color: #000000;
    padding: 2px 8px;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 800;
    width: 65px;
    text-align: center;
}

.layer-title {
    color: #ffffff;
    font-weight: 700;
    font-size: 11.5px;
    width: 200px;
}

.layer-desc {
    color: #94a3b8;
    font-size: 10.5px;
    flex: 1;
}

/* Code & Pre Blocks */
code {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 11px;
    background-color: #141419;
    color: #ffffff;
    padding: 2px 5px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

pre {
    background-color: #09090c;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 12px 16px;
    overflow-x: hidden;
    margin: 12px 0;
    page-break-inside: avoid;
    box-shadow: inset 3px 3px 8px rgba(0, 0, 0, 0.9),
                inset -2px -2px 6px rgba(255, 255, 255, 0.05),
                0 6px 16px rgba(0, 0, 0, 0.6);
}

pre code {
    background: transparent;
    border: none;
    padding: 0;
    color: #f8fafc;
    font-size: 10.5px;
    line-height: 1.4;
    display: block;
    white-space: pre;
    box-shadow: none;
}

/* Tables */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 16px 0;
    font-size: 11.5px;
    background: #0d0d12;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.14);
    page-break-inside: avoid;
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6), inset 1px 1px 2px rgba(255, 255, 255, 0.15);
}

th {
    background-color: #18181f;
    color: #ffffff;
    text-align: left;
    padding: 9px 12px;
    font-weight: 700;
    border-bottom: 2px solid #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

td {
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    color: #cbd5e1;
}

tr:last-child td {
    border-bottom: none;
}

tr:nth-child(even) td {
    background-color: #121217;
}

/* Lists */
ul, ol {
    margin: 6px 0 12px 18px;
    padding: 0;
    color: #cbd5e1;
}

li {
    margin-bottom: 4px;
}

li::marker {
    color: #ffffff;
}

hr {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    margin: 20px 0;
}

/* Cover Page */
.cover-page {
    min-height: 85vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    page-break-after: always;
    padding: 40px 24px;
    background: #0e0e13;
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 20px;
    box-shadow: 12px 12px 30px rgba(0, 0, 0, 0.85),
                -6px -6px 18px rgba(255, 255, 255, 0.05),
                inset 2px 2px 5px rgba(255, 255, 255, 0.2),
                inset -2px -2px 5px rgba(0, 0, 0, 0.7);
    margin-bottom: 24px;
}

.cover-pill {
    background: #ffffff;
    color: #000000;
    padding: 5px 18px;
    border-radius: 9999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 24px;
    box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5),
                inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.9),
                inset -2px -2px 3px rgba(0, 0, 0, 0.3);
}

.cover-title {
    font-size: 32px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1.2px;
    line-height: 1.25;
    margin-bottom: 14px;
}

.cover-title span {
    color: #ffffff;
    border-bottom: 3px solid #ffffff;
    padding-bottom: 2px;
}

.cover-subtitle {
    font-size: 14px;
    color: #94a3b8;
    max-width: 540px;
    margin-bottom: 38px;
    line-height: 1.6;
}

.cover-meta {
    background: #14141a;
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 14px;
    padding: 16px 28px;
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    box-shadow: 6px 6px 16px rgba(0, 0, 0, 0.6),
                -3px -3px 8px rgba(255, 255, 255, 0.04),
                inset 1.5px 1.5px 3px rgba(255, 255, 255, 0.18),
                inset -1.5px -1.5px 3px rgba(0, 0, 0, 0.5);
}

.cover-meta .author-line {
    color: #ffffff;
    font-size: 13.5px;
    font-weight: 800;
    margin-bottom: 4px;
    letter-spacing: 1px;
}

.cover-meta .sub-line {
    color: #94a3b8;
    font-size: 10.5px;
}

.page-break {
    page-break-before: always;
}
"""

def markdown_to_html_doc(md_content, title="Cybersecurity Reference", is_compilation=False):
    rendered_body = md.render(md_content)
    
    cover_html = ""
    if is_compilation:
        cover_html = """
        <div class="cover-page">
            <div class="cover-pill">SYSTEMS SECURITY & OPSEC SERIES</div>
            <div class="cover-title">CYBERSECURITY & OPSEC<br><span>THEORY & PRACTICAL FIELD GUIDE</span></div>
            <div class="cover-subtitle">Low-Level Network Architecture, Hardware Identifiers, Geolocation Realities, and Threat-Model Driven VPN Analysis</div>
            <div class="cover-meta">
                <div class="author-line">PUBLISHED AND MADE BY DRAXO.DEV</div>
                <div class="sub-line">SYSTEMS RESEARCH // COMPLETE CURRICULUM EDITION</div>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
{CLAY_BLACK_WHITE_CSS}
</style>
</head>
<body>
{cover_html}
<div class="header-bar">
    <div class="brand-tag"><span class="brand-pill">DRAXO.DEV</span> CYBERSECURITY & OPSEC</div>
    <div class="doc-tag">{title}</div>
</div>

{rendered_body}

<div class="footer-bar">
    <div>Published and made by <span class="author-credit">draxo.dev</span></div>
    <div>DRAXO.DEV RESEARCH &copy; 2026 // ALL RIGHTS RESERVED</div>
</div>
</body>
</html>"""
    return html

def convert_html_to_pdf(html_path, pdf_path):
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        str(html_path.resolve())
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error converting {html_path}: {res.stderr}")
    else:
        print(f"Generated: {pdf_path.name}")

def main():
    base_dir = Path(r"c:\Users\draxo\Downloads\Docs On cyber security")
    output_dir = base_dir / "PDFs"
    output_dir.mkdir(exist_ok=True)
    
    files = [
        ("01_Networking_IPs_Subnets_DNS.md", "01_Networking_IPs_Subnets_DNS.pdf", "Module 01: Networking, IPs, Subnets & DNS"),
        ("02_Hardware_Identifiers_MAC_Addresses.md", "02_Hardware_Identifiers_MAC_Addresses.pdf", "Module 02: Hardware Identifiers & MAC"),
        ("03_IP_Tracking_Geolocation_Realities.md", "03_IP_Tracking_Geolocation_Realities.pdf", "Module 03: IP Tracking & Geolocation Realities"),
        ("04_VPN_Mechanics_OPSEC_Provider_Breakdown.md", "04_VPN_Mechanics_OPSEC_Provider_Breakdown.pdf", "Module 04: VPN Mechanics & OPSEC Provider Breakdown"),
    ]
    
    full_compiled_md = ""
    
    for md_file, pdf_file, title in files:
        md_path = base_dir / md_file
        if md_path.exists():
            content = md_path.read_text(encoding="utf-8")
            
            if full_compiled_md:
                full_compiled_md += "\n\n<div class=\"page-break\"></div>\n\n"
            full_compiled_md += content
            
            html_content = markdown_to_html_doc(content, title=title)
            temp_html_path = output_dir / f"{md_file}.html"
            temp_html_path.write_text(html_content, encoding="utf-8")
            
            pdf_path = output_dir / pdf_file
            convert_html_to_pdf(temp_html_path, pdf_path)
    
    # Master Compilation Book PDF
    master_html = markdown_to_html_doc(
        full_compiled_md, 
        title="Complete Cybersecurity & OPSEC Guide — draxo.dev", 
        is_compilation=True
    )
    master_html_path = output_dir / "Cybersecurity_Complete_Guide_draxo_dev.html"
    master_html_path.write_text(master_html, encoding="utf-8")
    
    master_pdf_path = output_dir / "Cybersecurity_Complete_Guide_draxo_dev.pdf"
    convert_html_to_pdf(master_html_path, master_pdf_path)
    
    print("\nALL GRAPHS & REDESIGNED CLAYMORPHISM PDFS GENERATED!")

if __name__ == "__main__":
    main()
