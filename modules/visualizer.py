# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 16:03:32 2026

@author: vic_p
"""
import plotly.express as px
import plotly.graph_objects as go

def plot_unfiltered_region_bar(df):
    df_region = df.groupby('territory').size().reset_index(name='count')
    df_region = df_region.sort_values(by='count', ascending=False)
    
    fig = px.bar(
        df_region, x='territory', y='count',
        title="Territory Context: Total Orders per Region",
        labels={'count': 'Total Orders', 'region': 'Region'},
        color_discrete_sequence=['#AB63FA']
    )
    fig.update_xaxes(categoryorder='total descending')
    return fig

def plot_orders_and_atd_over_time(df):
    df_daily = df.groupby(df['order_final_state_timestamp_local'].dt.date).agg(
        total_orders=('workflow_uuid', 'count'),
        avg_atd=('ATD', 'mean')
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_daily['order_final_state_timestamp_local'],
        y=df_daily['total_orders'],
        name="Order Count",
        marker_color='#636EFA',
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=df_daily['order_final_state_timestamp_local'],
        y=df_daily['avg_atd'],
        name="Avg ATD (Min)",
        line=dict(color='#EF553B', width=3),
        yaxis='y2'
    ))

    fig.update_layout(
        title="Temporal Evolution: Orders vs. Avg ATD",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Order Volume", side="left"),
        yaxis2=dict(title="Avg ATD (Min)", side="right", overlaying="y", showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )
    return fig

def plot_merchant_pie(df):
    fig = px.pie(
        df, names='merchant_surface', 
        title="Orders by Merchant Surface",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig

def plot_atd_by_archetype(df):
    df_avg = df.groupby('geo_archetype')['ATD'].mean().reset_index()
    df_avg = df_avg.sort_values(by='ATD', ascending=False)
    
    fig = px.bar(
        df_avg, x='geo_archetype', y='ATD',
        title="Average ATD by Geo Archetype",
        labels={'ATD': 'Avg (Min)', 'geo_archetype': 'Archetype'},
        color='ATD',
        color_continuous_scale='Reds'
    )
    return fig

def plot_distance_vs_atd_segmented(df):
    fig = px.scatter(
        df, x="total_distance", y="ATD",
        color="atd_segment",
        title="Dispersion Analysis: Total Distance vs ATD",
        labels={'total_distance': 'Distance (KM)', 'ATD': 'Time (Min)', 'atd_segment': 'ATD Range'},
        category_orders={"atd_segment": ['0-10 min', '11-20 min', '21-40 min', '40-60 min', '60+ min']},
        render_mode='webgl'
    )
    return fig

def plot_distance_vs_atd_bubble(df):
    df_grouped = df.copy()
    df_grouped['dist_bin'] = df_grouped['total_distance'].round(1)
    df_grouped['territory '] = df_grouped['territory']
    df_plot = df_grouped.groupby(['dist_bin', 'territory ', 'atd_segment']).agg(
        order_count=('workflow_uuid', 'count')
    ).reset_index().dropna()

    fig = px.scatter(
        df_plot, 
        x="dist_bin", 
        y="territory ",
        size="order_count", 
        color="atd_segment",
        title="Operational Deep Dive: Distance vs. ATD (Bubble Size = Order Count)",
        labels={
            'dist_bin': 'Distance (KM)', 
            'territory ': 'Territory', 
            'atd_segment': 'ATD Range',
            'order_count': 'Orders'
        },
        category_orders={
            "atd_segment": ['0-10 min', '11-20 min', '21-40 min', '40-60 min', '60+ min']
        },
        size_max=40,
        template="plotly_white"
    )
    
    fig.update_layout(legend_title_text='ATD Range')
    return fig

def plot_atd_stacked_bar(df):
    df_grouped = df.groupby(['geo_archetype', 'atd_segment']).size().reset_index(name='order_count')
    territory_order = df.groupby('geo_archetype').size().sort_values(ascending=False).index
    
    fig = px.bar(
        df_grouped, 
        x='geo_archetype', 
        y='order_count', 
        color='atd_segment',
        title="Order Volume & ATD Performance by Archetype",
        labels={
            'geo_archetype': 'Archetype', 
            'order_count': 'Total Orders', 
            'atd_segment': 'ATD Range'
        },
        category_orders={
            "atd_segment": ['0-10 min', '11-20 min', '21-40 min', '40-60 min', '60+ min'],
            "Archetype": list(territory_order)
        },
        color_discrete_sequence=px.colors.sequential.RdBu_r, # Red for slow, Blue for fast
        template="plotly_white"
    )

    fig.update_layout(
        barmode='stack',
        xaxis={'categoryorder': 'total descending'},
        legend_title_text='ATD Range'
    )
    return fig

def plot_delivery_heatmap(df):
    """
    Heatmap: Day of Week vs. Hour of Day.
    Color intensity represents Order Volume.
    """
    # 1. Define day order for the axis
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # 2. Aggregate data
    df_heat = df.groupby(['day_of_week', 'hour_of_day']).size().reset_index(name='order_count')
    
    # 3. Create Heatmap
    fig = px.density_heatmap(
        df_heat, 
        x="hour_of_day", 
        y="day_of_week", 
        z="order_count",
        title="Operational Heatmap: Delivery Volume by Day & Hour",
        labels={'hour_of_day': 'Hour of Day (24h)', 'day_of_week': 'Day of Week', 'order_count': 'Orders'},
        category_orders={"day_of_week": day_order},
        color_continuous_scale='Viridis',
        template="plotly_white"
    )
    
    fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    return fig

def plot_regional_stacked_bar(df):
    df_region = df.groupby(['territory', 'atd_segment']).size().reset_index(name='count')
   
    region_order = df.groupby('territory').size().sort_values(ascending=False).index

    fig = px.bar(
        df_region, 
        x='territory', 
        y='count', 
        color='atd_segment',
        title="Territorial Context: Order Volume by ATD Segment",
        labels={'count': 'Total Orders', 'territory': 'territory', 'atd_segment': 'ATD Range'},
        category_orders={
            "atd_segment": ['0-10 min', '11-20 min', '21-40 min', '40-60 min', '60+ min'],
            "territory": list(region_order)
        },
        color_discrete_sequence=px.colors.sequential.RdBu_r,
        template="plotly_white"
    )
    
    fig.update_layout(barmode='stack')
    return fig