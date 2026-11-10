CSS = """
<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 1.4rem; padding-bottom: 3rem; max-width: 860px;}
h1, h2, h3 {letter-spacing: -0.01em;}
.hero {background: linear-gradient(135deg, #0F766E 0%, #1D4ED8 100%); color: #fff; border-radius: 22px; padding: 26px 28px; margin-bottom: 18px; box-shadow: 0 10px 30px rgba(29,78,216,.18);}
.hero h1 {color: #fff; margin: 0 0 6px 0; font-size: 1.9rem; line-height: 1.2;}
.hero p {color: rgba(255,255,255,.92); margin: 0; font-size: 1.02rem;}
.hero.compact {padding: 18px 24px;}
.hero.compact h1 {font-size: 1.4rem;}
.stepper {display: flex; gap: 10px; margin: 6px 0 18px 0;}
.step {flex: 1; display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 14px; background: #fff; border: 1px solid #E2E8F0; color: #64748B; font-weight: 600; font-size: .92rem;}
.step .dot {width: 26px; height: 26px; border-radius: 50%; background: #E2E8F0; color: #475569; display: flex; align-items: center; justify-content: center; font-size: .85rem;}
.step.on {border-color: #0F766E; color: #0F766E; box-shadow: 0 2px 10px rgba(15,118,110,.15);}
.step.on .dot {background: #0F766E; color: #fff;}
.step.done .dot {background: #16A34A; color: #fff;}
.sec-title {font-size: 1.25rem; font-weight: 700; margin: 4px 0 2px 0;}
.sec-sub {color: #64748B; margin-bottom: 14px;}
.card {background: #fff; border: 1px solid #E2E8F0; border-radius: 18px; padding: 20px 22px; margin: 12px 0 8px 0; box-shadow: 0 4px 16px rgba(15,23,42,.05);}
.card.top {border: 2px solid #0F766E;}
.card-head {display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;}
.card-title {font-size: 1.2rem; font-weight: 800; color: #0F172A;}
.rank {width: 28px; height: 28px; border-radius: 50%; background: #0F766E; color: #fff; display: inline-flex; align-items: center; justify-content: center; font-weight: 800; font-size: .9rem;}
.desc {color: #475569; margin: 2px 0 12px 0;}
.badge {display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: .76rem; font-weight: 700; white-space: nowrap;}
.b-cop {background: #FEF3C7; color: #92400E;}
.b-usd {background: #DBEAFE; color: #1E40AF;}
.b-mix {background: #E0E7FF; color: #3730A3;}
.b-co {background: #DCFCE7; color: #166534;}
.b-int {background: #EDE9FE; color: #5B21B6;}
.b-sfc {background: #CCFBF1; color: #115E59;}
.b-warn {background: #FEE2E2; color: #991B1B;}
.metrics {display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 8px 0 10px 0;}
.metric {background: #F1F5F9; border-radius: 14px; padding: 12px 14px;}
.metric .lbl {color: #64748B; font-size: .78rem; font-weight: 600;}
.metric .val {color: #0F172A; font-size: 1.25rem; font-weight: 800; margin-top: 2px;}
.metric .val.pos {color: #0F766E;}
.bar {height: 8px; border-radius: 999px; background: #E2E8F0; overflow: hidden; margin: 4px 0 2px 0;}
.bar > span {display: block; height: 100%; background: linear-gradient(90deg, #0F766E, #1D4ED8);}
.small {color: #64748B; font-size: .84rem;}
.note {background: #F0FDFA; border-left: 4px solid #0F766E; padding: 9px 12px; border-radius: 8px; color: #134E4A; font-size: .9rem; margin-top: 8px;}
.alert {padding: 11px 14px; border-radius: 12px; margin: 8px 0; font-size: .93rem;}
.alert.alto {background: #FEF2F2; border: 1px solid #FECACA; color: #7F1D1D;}
.alert.medio {background: #FFFBEB; border: 1px solid #FDE68A; color: #78350F;}
.alert.info {background: #EFF6FF; border: 1px solid #BFDBFE; color: #1E3A8A;}
.plat {background: #fff; border: 1px solid #E2E8F0; border-radius: 16px; padding: 16px 18px; margin: 8px 0;}
.plat-head {display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;}
.plat-name {font-size: 1.05rem; font-weight: 800;}
.plat-grid {display: grid; grid-template-columns: 1fr 1fr; gap: 10px 18px; font-size: .88rem; color: #334155;}
.plat-grid b {color: #0F172A;}
.btn-link {display: inline-block; margin-top: 10px; padding: 7px 14px; border-radius: 10px; background: #0F766E; color: #fff !important; text-decoration: none !important; font-weight: 700; font-size: .85rem;}
.btn-link:hover {background: #115E59;}
.gauge {position: relative; height: 12px; border-radius: 999px; background: linear-gradient(90deg, #22C55E 0%, #FACC15 50%, #EF4444 100%); margin: 16px 0 16px 0;}
.gauge .pin {position: absolute; top: -5px; width: 22px; height: 22px; border-radius: 50%; background: #fff; border: 4px solid #0F172A; transform: translateX(-50%);}
.gauge-lbl {display: flex; justify-content: space-between; color: #64748B; font-size: .78rem; font-weight: 600;}
.chips {display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px;}
.chip {background: rgba(255,255,255,.18); border-radius: 999px; padding: 4px 12px; font-size: .85rem; font-weight: 600;}
.disclaimer {color: #64748B; font-size: .8rem; text-align: center; margin-top: 26px;}
.stButton button, div[data-testid="stFormSubmitButton"] button {border-radius: 12px; font-weight: 700; padding: .55rem 1.3rem;}
@media (max-width: 640px) {
  .metrics {grid-template-columns: 1fr;}
  .plat-grid {grid-template-columns: 1fr;}
  .step span.t {display: none;}
  .hero h1 {font-size: 1.5rem;}
}
</style>
"""
