import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
	page_title="TreatyLens | Treaty Analysis",
	page_icon="🛡️",
	layout="wide",
)

REQUIRED_COLUMNS = [
	"treaty",
	"line_of_business",
	"reinsurer",
	"premium",
	"losses",
	"limit",
	"attachment",
	"ceded_pct",
	"effective_date",
	"expiry_date",
]


def sample_data():
	"""Return a small example portfolio for first-time users."""
	return pd.DataFrame(
		[
			["Property Cat XoL", "Property", "Northstar Re", 4_800_000, 2_450_000, 25_000_000, 5_000_000, 80, "2025-01-01", "2025-12-31"],
			["Motor Quota Share", "Motor", "Apex Re", 8_200_000, 6_560_000, 15_000_000, 0, 40, "2025-01-01", "2025-12-31"],
			["Casualty Surplus", "Casualty", "Harbor Re", 3_600_000, 1_980_000, 12_000_000, 2_000_000, 60, "2025-04-01", "2026-03-31"],
			["Marine Quota Share", "Marine", "Northstar Re", 2_100_000, 1_050_000, 8_000_000, 0, 50, "2025-01-01", "2025-12-31"],
			["Property Risk XoL", "Property", "Cedar Re", 5_100_000, 3_825_000, 18_000_000, 3_000_000, 70, "2025-07-01", "2026-06-30"],
			["Health Excess Loss", "Health", "Apex Re", 2_750_000, 1_430_000, 10_000_000, 1_000_000, 65, "2025-01-01", "2025-12-31"],
			["Motor XoL", "Motor", "Harbor Re", 3_900_000, 4_680_000, 20_000_000, 4_000_000, 75, "2025-01-01", "2025-12-31"],
			["Agriculture Quota Share", "Agriculture", "Cedar Re", 1_850_000, 925_000, 6_000_000, 0, 45, "2025-10-01", "2026-09-30"],
		],
		columns=REQUIRED_COLUMNS,
	)


def normalize_data(frame):
	frame = frame.copy()
	frame.columns = [str(column).strip().lower().replace(" ", "_") for column in frame.columns]
	missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
	if missing:
		raise ValueError("Missing required columns: " + ", ".join(missing))

	for column in ["premium", "losses", "limit", "attachment", "ceded_pct"]:
		frame[column] = pd.to_numeric(frame[column], errors="coerce")
	frame["effective_date"] = pd.to_datetime(frame["effective_date"], errors="coerce")
	frame["expiry_date"] = pd.to_datetime(frame["expiry_date"], errors="coerce")
	frame = frame.dropna(subset=["premium", "losses", "limit", "attachment", "ceded_pct"])
	frame["loss_ratio"] = frame["losses"].div(frame["premium"].where(frame["premium"] != 0)).mul(100)
	frame["status"] = "Expired"
	today = pd.Timestamp.today().normalize()
	frame.loc[frame["effective_date"].gt(today), "status"] = "Upcoming"
	frame.loc[frame["effective_date"].le(today) & frame["expiry_date"].ge(today), "status"] = "Active"
	return frame


st.title("🛡️ TreatyLens")
st.caption("Analyze treaty performance, structure, and renewal exposure in one place.")

with st.sidebar:
	st.header("Treaty data")
	uploaded_file = st.file_uploader("Upload treaty data (CSV)", type=["csv"])
	st.caption("Required columns: " + ", ".join(REQUIRED_COLUMNS))

try:
	source = pd.read_csv(uploaded_file) if uploaded_file else sample_data()
	data = normalize_data(source)
except Exception as error:
	st.error(f"Could not load treaty data: {error}")
	st.stop()

if data.empty:
	st.warning("No valid treaty records were found in this file.")
	st.stop()

with st.sidebar:
	lines = sorted(data["line_of_business"].dropna().astype(str).unique())
	reinsurers = sorted(data["reinsurer"].dropna().astype(str).unique())
	selected_lines = st.multiselect("Line of business", lines, default=lines)
	selected_reinsurers = st.multiselect("Reinsurer", reinsurers, default=reinsurers)
	selected_statuses = st.multiselect(
		"Treaty status", ["Active", "Upcoming", "Expired"], default=["Active", "Upcoming", "Expired"]
	)

filtered = data[
	data["line_of_business"].astype(str).isin(selected_lines)
	& data["reinsurer"].astype(str).isin(selected_reinsurers)
	& data["status"].isin(selected_statuses)
].copy()

if filtered.empty:
	st.info("No treaties match the selected filters.")
	st.stop()

total_premium = filtered["premium"].sum()
total_losses = filtered["losses"].sum()
portfolio_loss_ratio = total_losses / total_premium * 100 if total_premium else 0

metrics = st.columns(4)
metrics[0].metric("Treaties in view", f"{len(filtered):,}")
metrics[1].metric("Gross premium", f"${total_premium:,.0f}")
metrics[2].metric("Incurred losses", f"${total_losses:,.0f}")
metrics[3].metric("Portfolio loss ratio", f"{portfolio_loss_ratio:.1f}%")

left, right = st.columns(2)
with left:
	st.subheader("Premium and losses by line")
	totals = filtered.groupby("line_of_business", as_index=False)[["premium", "losses"]].sum()
	chart_data = totals.melt(id_vars="line_of_business", var_name="measure", value_name="amount")
	chart = px.bar(
		chart_data,
		x="line_of_business",
		y="amount",
		color="measure",
		barmode="group",
		labels={"line_of_business": "Line of business", "amount": "Amount ($)", "measure": "Measure"},
		color_discrete_map={"premium": "#356AE6", "losses": "#F08A5D"},
	)
	chart.update_layout(legend_title_text="", margin=dict(t=10, b=10))
	st.plotly_chart(chart, use_container_width=True)

with right:
	st.subheader("Loss ratio by treaty")
	ratios = filtered.sort_values("loss_ratio", ascending=False)
	chart = px.bar(
		ratios,
		x="loss_ratio",
		y="treaty",
		orientation="h",
		color="loss_ratio",
		color_continuous_scale="RdYlGn_r",
		labels={"loss_ratio": "Loss ratio (%)", "treaty": "Treaty"},
		hover_data={"reinsurer": True, "premium": ":$,.0f", "losses": ":$,.0f"},
	)
	chart.add_vline(x=100, line_dash="dash", line_color="#555", annotation_text="100%")
	chart.update_layout(coloraxis_showscale=False, margin=dict(t=10, b=10))
	st.plotly_chart(chart, use_container_width=True)

left, right = st.columns(2)
with left:
	st.subheader("Treaty structure")
	structure = px.scatter(
		filtered,
		x="attachment",
		y="limit",
		size="premium",
		color="line_of_business",
		hover_name="treaty",
		hover_data={"reinsurer": True, "ceded_pct": ":.1f", "premium": ":$,.0f"},
		labels={"attachment": "Attachment ($)", "limit": "Limit ($)", "line_of_business": "Line"},
	)
	structure.update_layout(margin=dict(t=10, b=10))
	st.plotly_chart(structure, use_container_width=True)

with right:
	st.subheader("Premium by reinsurer")
	reinsurer_totals = filtered.groupby("reinsurer", as_index=False)["premium"].sum()
	chart = px.pie(reinsurer_totals, names="reinsurer", values="premium", hole=0.55)
	chart.update_layout(margin=dict(t=10, b=10), legend_title_text="")
	st.plotly_chart(chart, use_container_width=True)

st.subheader("Treaty register")
columns = [
	"treaty", "line_of_business", "reinsurer", "status", "premium", "losses", "loss_ratio",
	"limit", "attachment", "ceded_pct", "effective_date", "expiry_date",
]
register = filtered[columns].sort_values(["status", "expiry_date"])
st.dataframe(
	register,
	use_container_width=True,
	hide_index=True,
	column_config={
		"premium": st.column_config.NumberColumn("Premium", format="$%.0f"),
		"losses": st.column_config.NumberColumn("Incurred losses", format="$%.0f"),
		"limit": st.column_config.NumberColumn("Limit", format="$%.0f"),
		"attachment": st.column_config.NumberColumn("Attachment", format="$%.0f"),
		"ceded_pct": st.column_config.NumberColumn("Ceded share", format="%.1f%%"),
		"loss_ratio": st.column_config.NumberColumn("Loss ratio", format="%.1f%%"),
		"effective_date": st.column_config.DateColumn("Effective date"),
		"expiry_date": st.column_config.DateColumn("Expiry date"),
	},
)
st.download_button(
	"Download filtered treaty register",
	data=register.to_csv(index=False).encode("utf-8"),
	file_name="treaty_register.csv",
	mime="text/csv",
)
st.caption("Sample portfolio values are illustrative; validate analysis against source systems.")
