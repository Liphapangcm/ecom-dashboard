from utils.data_loader import load_data, get_revenue_over_time, get_top_categories
from components.charts import chart_revenue_over_time, chart_top_categories

df = load_data()
fig1 = chart_revenue_over_time(get_revenue_over_time(df))
fig2 = chart_top_categories(get_top_categories(df))

fig1.show()
fig2.show()