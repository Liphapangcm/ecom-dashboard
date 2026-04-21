import pandas as pd

BASE_URL = "https://raw.githubusercontent.com/nazliander/ecommerce-sales-analysis/master/data/"

def load_data():
    orders = pd.read_csv(BASE_URL + "olist_orders_dataset.csv")
    items = pd.read_csv(BASE_URL + "olist_order_items_dataset.csv")
    products = pd.read_csv(BASE_URL + "olist_products_dataset.csv")
    customers = pd.read_csv(BASE_URL + "olist_customers_dataset.csv")

    # Parse dates
    date_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])

    # Only keep delivered orders
    orders = orders[orders["order_status"] == "delivered"].copy()

    # Master dataframe — join everything together
    df = (
        orders
        .merge(items, on="order_id", how="inner")
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
        .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left")
    )

    # Add useful time columns
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M")
    df["order_week"] = df["order_purchase_timestamp"].dt.to_period("W")
    df["order_year"] = df["order_purchase_timestamp"].dt.year

    # Clean up revenue column name
    df = df.rename(columns={"price": "revenue"})

    return df

def get_revenue_over_time(df):
    """Monthly revenue trend"""
    return (
        df.groupby("order_month")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .assign(order_month=lambda x: x["order_month"].astype(str))
    )


def get_top_categories(df, n=10):
    """Top n product categories by revenue"""
    return (
        df.groupby("product_category_name")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .sort_values("total_revenue", ascending=False)
        .head(n)
    )


def get_revenue_by_state(df):
    """Revenue by Brazilian state — for the map/bar chart"""
    return (
        df.groupby("customer_state")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .sort_values("total_revenue", ascending=False)
    )


def get_weekly_summary_stats(df):
    """Last 8 weeks of data — used for AI summary"""
    last_8_weeks = df["order_week"].unique()
    last_8_weeks = sorted(last_8_weeks)[-8:]
    recent = df[df["order_week"].isin(last_8_weeks)]

    weekly = (
        recent.groupby("order_week")
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("order_id", "nunique"),
            avg_order_value=("revenue", "mean")
        )
        .reset_index()
        .assign(order_week=lambda x: x["order_week"].astype(str))
    )
    return weekly


def get_kpi_summary(df):
    """Top-level KPI numbers for the dashboard header"""
    total_revenue = df["revenue"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = df["revenue"].mean()
    top_category = (
        df.groupby("product_category_name")["revenue"]
        .sum()
        .idxmax()
    )
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "avg_order_value": round(avg_order_value, 2),
        "top_category": top_category
    }