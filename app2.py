import streamlit as st
from modules.data_loader import get_data
from modules import visualizer as viz

st.set_page_config(page_title="Delivery Strategy Analytics", layout="wide")

def main():
    st.title("Delivery Operations Dashboard")
    
    #Data
    try:
        df_raw = get_data('data/BC_A&A_with_ATD.csv')
    except FileNotFoundError:
        st.error("Data file not found in data folder")
        return
    #Filters
    st.sidebar.header("Filter Configuration")
    
    min_d = df_raw['order_final_state_timestamp_local'].min().date()
    max_d = df_raw['order_final_state_timestamp_local'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range Selection", 
        value=(min_d, max_d), 
        min_value=min_d, 
        max_value=max_d
    )
    territories = st.sidebar.multiselect(
        "Territory Segment", 
        options=df_raw['territory'].unique(), 
        default=df_raw['territory'].unique()
    )
    ATD_Segments = st.sidebar.multiselect(
        "ATD Segment", 
        options=df_raw['atd_segment'].unique(), 
        default=df_raw['atd_segment'].unique()
    )

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
        df_date_only = df_raw[
            (df_raw['order_final_state_timestamp_local'].dt.date >= start_d) & 
            (df_raw['order_final_state_timestamp_local'].dt.date <= end_d)
        ]
        df_territory_dates= df_date_only[df_date_only['territory'].isin(territories)]
        df_final=df_territory_dates[df_territory_dates['atd_segment'].isin(ATD_Segments)]
    else:
        df_date_only, df_final = df_raw, df_raw

    #KPI
    c1, c2, c3 = st.columns(3)
    c1.metric("Selected Orders", f"{len(df_final):,}")
    c2.metric("Avg ATD", f"{df_final['ATD'].mean():.2f} min")
    c3.metric("Avg Distance", f"{df_final['total_distance'].mean():.2f} km")
    st.divider()

    #Visuals
    st.plotly_chart(viz.plot_regional_stacked_bar(df_date_only), width='stretch' , key='regionalstacked' )
    st.plotly_chart(viz.plot_orders_and_atd_over_time(df_final), width='stretch', key='ordersvsatdvisual')
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.plot_merchant_pie(df_final), width='stretch', key='type_pie')
    with col2:
        st.plotly_chart(viz.plot_atd_by_archetype(df_final), width='stretch', key='atd_arch')
    st.subheader("Territory Performance Breakdown")
    st.plotly_chart(viz.plot_atd_stacked_bar(df_final), width='stretch', key='atdstackedbar')
    
    st.divider()
    st.subheader("Time-Based Operational Analysis")
    st.plotly_chart(viz.plot_delivery_heatmap(df_final), width='stretch', key='delvheat,map')

    
if __name__ == "__main__":
    main()