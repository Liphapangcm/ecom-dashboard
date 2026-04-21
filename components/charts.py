import plotly.express as px
import plotly.graph_objects as go

COLOR_PRIMARY = "#1E4D8C"
COLOR_ACCENT = "#2E86DE"
COLOR_SEQ = px.colors.sequential.Blues[3:]


def chart_revenue_over_time(revenue_df):
    """Line chart — monthly revenue trend"""
    fig = px.line(
        revenue_df,
        x="order_month",
        y="total_revenue",
        title="Monthly Revenue Trend",
        labels={"order_month": "Month", "total_revenue": "Revenue (R$)"},
        color_discrete_sequence=[COLOR_ACCENT]
    )
    fig.update_traces(line_width=2.5, mode="lines+markers")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(tickangle=45),
        yaxis=dict(tickformat=",.0f")
    )
    return fig


def chart_top_categories(categories_df):
    """Horizontal bar chart — top categories by revenue"""
    # Reverse so highest is at top
    df = categories_df.sort_values("total_revenue", ascending=True)
    fig = px.bar(
        df,
        x="total_revenue",
        y="product_category_name",
        orientation="h",
        title="Top 10 Categories by Revenue",
        labels={"total_revenue": "Revenue (R$)", "product_category_name": "Category"},
        color="total_revenue",
        color_continuous_scale=COLOR_SEQ
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False,
        yaxis_title=None,
        xaxis=dict(tickformat=",.0f")
    )
    return fig


def chart_revenue_by_state(state_df):
    """Bar chart — revenue by customer state"""
    fig = px.bar(
        state_df,
        x="customer_state",
        y="total_revenue",
        title="Revenue by Customer State",
        labels={"customer_state": "State", "total_revenue": "Revenue (R$)"},
        color="total_revenue",
        color_continuous_scale=COLOR_SEQ
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        coloraxis_showscale=False,
        xaxis_title=None,
        yaxis=dict(tickformat=",.0f")
    )
    return fig


def chart_weekly_trend(weekly_df):
    """Dual-axis chart — weekly orders and revenue together"""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=weekly_df["order_week"],
        y=weekly_df["total_orders"],
        name="Orders",
        marker_color=COLOR_PRIMARY,
        opacity=0.7,
        yaxis="y"
    ))

    fig.add_trace(go.Scatter(
        x=weekly_df["order_week"],
        y=weekly_df["total_revenue"],
        name="Revenue (R$)",
        mode="lines+markers",
        line=dict(color=COLOR_ACCENT, width=2.5),
        yaxis="y2"
    ))

    fig.update_layout(
        title="Last 8 Weeks — Orders vs Revenue",
        plot_bgcolor="white",
        paper_bgcolor="white",
        hovermode="x unified",
        xaxis=dict(tickangle=45),
        yaxis=dict(title="Orders", showgrid=False),
        yaxis2=dict(
            title="Revenue (R$)",
            overlaying="y",
            side="right",
            tickformat=",.0f"
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    return fig