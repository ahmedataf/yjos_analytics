import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import numpy as np
from yjos_extractor import YJOSDataExtractor

# Streamlit App Configuration
st.set_page_config(
    page_title="YJOS Drillout Analytics",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.metric-card {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #2a5298;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.success-metric { 
    border-left-color: #28a745;
    background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
}
.warning-metric { 
    border-left-color: #ffc107;
    background: linear-gradient(135deg, #fffef8 0%, #fff3cd 100%);
}
.danger-metric { 
    border-left-color: #dc3545;
    background: linear-gradient(135deg, #fff8f8 0%, #f8d7da 100%);
}
.drill-metric {
    border-left-color: #17a2b8;
    background: linear-gradient(135deg, #f8fdff 0%, #e2f3f5 100%);
}
.stMetric {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛠️ YJOS Drillout Analytics Dashboard</h1>
        <p>Advanced Drilling Operations Analysis & Performance Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    
    # File Upload Section
    st.sidebar.header("📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload YJOS Drillout Excel File",
        type=['xlsx', 'xls'],
        help="Upload your YJOS Drillout Field Tool Kit Excel file for analysis"
    )
    
    # Demo Data Toggle
    use_demo = st.sidebar.checkbox("Use Demo Data", value=True, help="Use sample drillout data for demonstration")
    
    # Analysis Options
    st.sidebar.header("⚙️ Analysis Options")
    show_drilling_performance = st.sidebar.checkbox("Show Drilling Performance", value=True)
    show_detailed_breakdown = st.sidebar.checkbox("Show Daily Breakdown", value=True)
    show_equipment_analysis = st.sidebar.checkbox("Show Equipment Analysis", value=True)
    show_recommendations = st.sidebar.checkbox("Show Recommendations", value=True)
    
    # Initialize data
    if use_demo or uploaded_file is not None:
        if uploaded_file is not None:
            st.sidebar.info("📤 Processing uploaded drillout file...")
            try:
                extractor = YJOSDataExtractor()
                data = extractor.process_uploaded_file(uploaded_file)
                st.sidebar.success("✅ Drillout file processed successfully!")
            except Exception as e:
                st.sidebar.warning(f"⚠️ File processing failed, using demo data. Error: {str(e)}")
                extractor = YJOSDataExtractor()
                data = extractor.get_demo_data()
        else:
            extractor = YJOSDataExtractor()
            data = extractor.get_demo_data()
            st.sidebar.success("✅ Demo drillout data loaded successfully!")
        
        # Main Dashboard Content
        display_dashboard(data, show_drilling_performance, show_detailed_breakdown, show_equipment_analysis, show_recommendations)
    else:
        st.info("👆 Please upload a YJOS Drillout Excel file or enable demo data to begin analysis.")
        
        # Show sample upload instructions
        st.markdown("""
        ### 📋 YJOS Drillout Analytics
        
        **Specialized for Drilling Operations:**
        - **Mill Data Analysis**: Plug drilling performance and timing
        - **CT Operations**: Coiled tubing milling efficiency  
        - **Equipment Tracking**: Tool usage and maintenance scheduling
        - **Operational Frequency**: Daily activity patterns and productivity
        - **Performance Metrics**: Drilling efficiency and success rates
        
        ### 🎯 Key Features
        - **Real-time Processing**: Upload Excel files for instant analysis
        - **Drilling Insights**: Mill performance, CT operations, depth tracking
        - **Equipment Analytics**: Usage patterns, maintenance alerts, efficiency ratings
        - **Trend Analysis**: Multi-day operational patterns and optimization opportunities
        - **Export Capabilities**: Download reports and data for management review
        
        ### 📊 Demo Data Available
        Enable "Use Demo Data" to explore the dashboard with realistic drillout operation data.
        """)

def display_dashboard(data, show_drilling_performance, show_detailed_breakdown, show_equipment_analysis, show_recommendations):
    """Display the main dashboard with drillout-specific analytics"""
    
    # Job Summary Section
    st.header("📋 Job Summary")
    job_info = data.get('job_summary', {})
    
    # Use native Streamlit metrics for better reliability
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👤 Customer",
            value=job_info.get('customer_name', 'Mughees Khan'),
            delta=f"Ticket: {job_info.get('ticket_number', 'AE867384')}"
        )

    with col2:
        st.metric(
            label="🛠️ Operation Type", 
            value=job_info.get('job_type', 'Drillout Operation'),
            delta=f"{job_info.get('well_number', 'Well #DSO-1')} | {job_info.get('county', 'Dubai')}"
        )

    with col3:
        st.metric(
            label="⏱️ Duration",
            value=f"{job_info.get('duration_days', 7)} Days",
            delta=f"{job_info.get('date_started', '2025-06-11')} to {job_info.get('date_ended', '2025-06-18')}"
        )

    with col4:
        st.metric(
            label="✅ Status",
            value="Completed",
            delta=f"Supervisor: {job_info.get('day_supervisor', 'Saif Khan')}"
        )
    
    # Key Performance Indicators
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    ops_freq = data.get('operational_frequency', {})
    efficiency = data.get('efficiency_metrics', {})
    equipment_freq = data.get('equipment_frequency', {})
    
    with col1:
        st.metric(
            label="Total Activities",
            value=ops_freq.get('total_activities', 78),
            delta=f"{ops_freq.get('avg_activities_per_day', 11.1):.1f} per day"
        )
    
    with col2:
        st.metric(
            label="Work Hours",
            value=f"{ops_freq.get('total_work_hours', 68.5):.1f}",
            delta=f"{ops_freq.get('avg_hours_per_day', 9.8):.1f} per day"
        )
    
    with col3:
        st.metric(
            label="Drilling Efficiency",
            value=f"{efficiency.get('drilling_efficiency', 88):.0f}%",
            delta="performance rating"
        )
    
    with col4:
        st.metric(
            label="Equipment Success",
            value=f"{equipment_freq.get('deployment_success_rate', 83.3):.0f}%",
            delta="deployment success"
        )
    
    with col5:
        st.metric(
            label="Safety Score",
            value=f"{efficiency.get('safety_score', 98):.0f}",
            delta="out of 100"
        )
    
    # Drilling Performance Section
    if show_drilling_performance:
        st.header("🚀 Drilling Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        # Mill Performance Metrics
        mill_perf = data.get('mill_performance', {})
        ct_perf = data.get('ct_performance', {})
        
        with col1:
            st.subheader("⚙️ Mill Operations")
            
            mill_col1, mill_col2 = st.columns(2)
            with mill_col1:
                st.metric(
                    label="Plugs Drilled",
                    value=mill_perf.get('total_plugs_drilled', 10),
                    delta=f"{mill_perf.get('total_footage', 30)} ft total"
                )
            with mill_col2:
                st.metric(
                    label="Avg Drill Time",
                    value=f"{mill_perf.get('avg_drill_time_mins', 42.3):.1f} min",
                    delta=mill_perf.get('efficiency_rating', 'High')
                )
        
        with col2:
            st.subheader("🔄 CT Operations")
            
            ct_col1, ct_col2 = st.columns(2)
            with ct_col1:
                st.metric(
                    label="CT Operations",
                    value=ct_perf.get('total_ct_operations', 5),
                    delta=f"{ct_perf.get('depth_accuracy', 95.5):.1f}% accuracy"
                )
            with ct_col2:
                st.metric(
                    label="Avg CT Time",
                    value=f"{ct_perf.get('avg_ct_drill_time', 36.8):.1f} min",
                    delta=ct_perf.get('efficiency_rating', 'Excellent')
                )
        
        # Drilling Performance Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Create sample drill time data for visualization
            drill_times = [42.3 - i*1.2 + np.random.normal(0, 2) for i in range(10)]
            plug_numbers = list(range(1, 11))
            
            fig_drill_times = px.line(
                x=plug_numbers,
                y=drill_times,
                title='Drill Time Progression by Plug',
                labels={'x': 'Plug Number', 'y': 'Drill Time (minutes)'},
                markers=True
            )
            fig_drill_times.update_traces(line_color='#2a5298', marker_size=8)
            fig_drill_times.add_hline(y=np.mean(drill_times), line_dash="dash", 
                                    annotation_text=f"Average: {np.mean(drill_times):.1f} min")
            st.plotly_chart(fig_drill_times, use_container_width=True)
        
        with col2:
            # Drilling efficiency comparison
            efficiency_data = {
                'Operation Type': ['Mill Operations', 'CT Operations', 'Industry Standard'],
                'Efficiency Score': [mill_perf.get('success_rate', 100), 
                                   ct_perf.get('depth_accuracy', 95.5), 85],
                'Color': ['Mill', 'CT', 'Standard']
            }
            
            fig_efficiency = px.bar(
                efficiency_data,
                x='Operation Type',
                y='Efficiency Score',
                title='Operation Efficiency Comparison',
                color='Color',
                color_discrete_map={'Mill': '#2a5298', 'CT': '#28a745', 'Standard': '#6c757d'}
            )
            fig_efficiency.update_layout(showlegend=False)
            st.plotly_chart(fig_efficiency, use_container_width=True)
    
    # Operational Frequency Charts
    st.header("📈 Operational Frequency Analysis")
    
    col1, col2 = st.columns(2)
    
    daily_breakdown = data.get('daily_breakdown', [])
    if daily_breakdown:
        daily_data = pd.DataFrame(daily_breakdown)
        
        with col1:
            # Daily Activities Chart with drilling operations overlay
            fig_activities = go.Figure()
            
            fig_activities.add_trace(go.Bar(
                name='Total Activities',
                x=daily_data['day'],
                y=daily_data['activities'],
                marker_color='#2a5298',
                opacity=0.7
            ))
            
            fig_activities.add_trace(go.Scatter(
                name='Mill Operations',
                x=daily_data['day'],
                y=daily_data['mill_operations'],
                mode='lines+markers',
                line=dict(color='#dc3545', width=3),
                marker=dict(size=8)
            ))
            
            fig_activities.add_trace(go.Scatter(
                name='CT Operations',
                x=daily_data['day'],
                y=daily_data['ct_operations'],
                mode='lines+markers',
                line=dict(color='#28a745', width=3),
                marker=dict(size=8)
            ))
            
            fig_activities.update_layout(
                title='Daily Activities & Drilling Operations',
                xaxis_title='Day',
                yaxis_title='Count',
                legend=dict(x=0, y=1)
            )
            st.plotly_chart(fig_activities, use_container_width=True)
        
        with col2:
            # Work Hours vs Downtime
            fig_hours = go.Figure()
            
            fig_hours.add_trace(go.Bar(
                name='Work Hours',
                x=daily_data['day'],
                y=daily_data['work_hours'],
                marker_color='#2a5298'
            ))
            
            fig_hours.add_trace(go.Bar(
                name='Downtime',
                x=daily_data['day'],
                y=daily_data['downtime'],
                marker_color='#dc3545'
            ))
            
            fig_hours.update_layout(
                title='Daily Work Hours vs Downtime',
                xaxis_title='Day',
                yaxis_title='Hours',
                barmode='stack'
            )
            
            st.plotly_chart(fig_hours, use_container_width=True)
    else:
        st.warning("No daily breakdown data available")
    
    # Equipment Analysis Section
    if show_equipment_analysis:
        st.header("🔧 Equipment Utilization Analysis")
        
        equipment_usage = data.get('equipment_usage', {})
        
        if equipment_usage:
            col1, col2 = st.columns(2)
            
            with col1:
                # Equipment Usage Frequency with tool types
                eq_df = pd.DataFrame([
                    {
                        'Tool': tool,
                        'Tool Type': info.get('tool_type', 'Unknown'),
                        'Usage Count': info.get('usage_count', 0),
                        'Success Rate': info.get('success_rate', 0),
                        'Avg Deployment Time': info.get('avg_deployment_time', 0),
                        'Maintenance Due': info.get('maintenance_due', False)
                    }
                    for tool, info in equipment_usage.items()
                ])
                
                fig_eq_usage = px.bar(
                    eq_df,
                    x='Tool',
                    y='Usage Count',
                    title='Equipment Usage Frequency',
                    color='Success Rate',
                    color_continuous_scale='RdYlGn',
                    hover_data=['Tool Type', 'Avg Deployment Time']
                )
                st.plotly_chart(fig_eq_usage, use_container_width=True)
            
            with col2:
                # Equipment Performance Distribution
                performance_dist = equipment_freq.get('performance_distribution', {})
                
                if performance_dist:
                    fig_performance = px.pie(
                        values=list(performance_dist.values()),
                        names=list(performance_dist.keys()),
                        title='Equipment Performance Distribution',
                        color_discrete_map={
                            'excellent': '#28a745',
                            'good': '#17a2b8',
                            'poor': '#dc3545'
                        }
                    )
                    st.plotly_chart(fig_performance, use_container_width=True)
                else:
                    st.info("Performance distribution data not available")
            
            # Equipment Details Table with maintenance alerts
            st.subheader("🔍 Equipment Details & Maintenance Status")
            
            # Create a color-coded display
            eq_display = eq_df.copy()
            
            # Add status indicators
            def get_status_emoji(row):
                if row['Maintenance Due']:
                    return "🔴 Maintenance Required"
                elif row['Success Rate'] >= 95:
                    return "🟢 Excellent"
                elif row['Success Rate'] >= 85:
                    return "🟡 Good"
                else:
                    return "🟠 Needs Attention"
            
            eq_display['Status'] = eq_display.apply(get_status_emoji, axis=1)
            eq_display['Success Rate'] = eq_display['Success Rate'].apply(lambda x: f"{x:.0f}%")
            eq_display['Avg Deployment Time'] = eq_display['Avg Deployment Time'].apply(lambda x: f"{x:.1f}h")
            
            # Highlight maintenance due items
            maintenance_due = eq_display[eq_display['Status'].str.contains('Maintenance Required')]
            if not maintenance_due.empty:
                st.warning(f"⚠️ {len(maintenance_due)} tools require maintenance: {', '.join(maintenance_due['Tool'].values)}")
            
            st.dataframe(eq_display[['Tool', 'Tool Type', 'Usage Count', 'Success Rate', 'Avg Deployment Time', 'Status']], 
                        use_container_width=True)
        else:
            st.warning("No equipment usage data available")
    
    # Detailed Daily Breakdown
    if show_detailed_breakdown and daily_breakdown:
        st.header("📅 Detailed Daily Operations")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "⏱️ Drilling Timeline", "🛠️ Equipment Schedule"])
        
        with tab1:
            # Comprehensive daily table with drilling operations
            daily_detailed = pd.DataFrame(daily_breakdown)
            daily_detailed['Efficiency'] = (daily_detailed['activities'] / daily_detailed['work_hours']).round(2)
            daily_detailed['Equipment Count'] = daily_detailed['equipment'].apply(len)
            daily_detailed['Total Drilling Ops'] = daily_detailed['mill_operations'] + daily_detailed['ct_operations']
            
            st.dataframe(
                daily_detailed[['day', 'date', 'activities', 'work_hours', 'downtime', 'mill_operations', 'ct_operations', 'Total Drilling Ops', 'Equipment Count', 'Efficiency']],
                use_container_width=True
            )
        
        with tab2:
            # Drilling operations timeline
            fig_drilling_timeline = go.Figure()
            
            # Mill operations
            fig_drilling_timeline.add_trace(go.Bar(
                name='Mill Operations',
                x=daily_data['day'],
                y=daily_data['mill_operations'],
                marker_color='#dc3545',
                width=0.4,
                offset=-0.2
            ))
            
            # CT operations
            fig_drilling_timeline.add_trace(go.Bar(
                name='CT Operations',
                x=daily_data['day'],
                y=daily_data['ct_operations'],
                marker_color='#28a745',
                width=0.4,
                offset=0.2
            ))
            
            fig_drilling_timeline.update_layout(
                title='Drilling Operations Timeline',
                xaxis_title='Day',
                yaxis_title='Number of Operations',
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig_drilling_timeline, use_container_width=True)
        
        with tab3:
            # Equipment usage schedule
            equipment_schedule = []
            for day_data in daily_breakdown:
                for equipment in day_data.get('equipment', []):
                    equipment_schedule.append({
                        'Day': day_data['day'],
                        'Date': day_data['date'],
                        'Equipment': equipment,
                        'Work Hours': day_data['work_hours']
                    })
            
            if equipment_schedule:
                eq_schedule_df = pd.DataFrame(equipment_schedule)
                
                # Create schedule heatmap
                fig_eq_schedule = px.density_heatmap(
                    eq_schedule_df,
                    x='Day',
                    y='Equipment',
                    title='Equipment Usage Schedule',
                    color_continuous_scale='Blues',
                    aspect='auto'
                )
                st.plotly_chart(fig_eq_schedule, use_container_width=True)
                
                # Equipment utilization summary
                eq_utilization = eq_schedule_df.groupby('Equipment').agg({
                    'Day': 'count',
                    'Work Hours': 'sum'
                }).rename(columns={'Day': 'Days Used', 'Work Hours': 'Total Hours'})
                
                st.subheader("Equipment Utilization Summary")
                st.dataframe(eq_utilization, use_container_width=True)
            else:
                st.info("No equipment schedule data available")
    
    # Recommendations Section
    if show_recommendations:
        st.header("💡 AI-Powered Recommendations")
        
        recommendations = data.get('recommendations', [
            "✅ Excellent drilling performance with 42.3 min average - maintain current operational parameters",
            "🔧 2 tools (FT3, FT6) require maintenance review before next deployment", 
            "🎯 High drilling efficiency achieved (88%) - consider sharing best practices with other crews",
            "💡 CT operations showing excellent efficiency (36.8 min avg) - optimize for future jobs",
            "🛡️ Maintain excellent safety record with continued JSA compliance and observation protocols"
        ])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                if 'excellent' in rec.lower() or 'maintain' in rec.lower():
                    rec_type = "success-metric"
                    icon = "✅"
                elif 'maintenance' in rec.lower() or 'require' in rec.lower():
                    rec_type = "warning-metric"  
                    icon = "⚠️"
                elif 'efficiency' in rec.lower() or 'optimize' in rec.lower():
                    rec_type = "drill-metric"
                    icon = "🎯"
                elif 'safety' in rec.lower():
                    rec_type = "success-metric"
                    icon = "🛡️"
                else:
                    rec_type = "metric-card"
                    icon = "💡"
                
                st.markdown(f"""
                <div class="metric-card {rec_type}" style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #2a5298; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: #333;">{icon} Recommendation {i}</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #666;">{rec}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recommendations available")
    
    # Advanced Analytics Section
    st.header("📊 Advanced Drilling Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Drilling efficiency trends
        st.subheader("⚡ Drilling Efficiency Trends")
        
        # Create efficiency trend data
        days = list(range(1, 8))
        efficiency_trend = [85 + i*0.5 + np.random.normal(0, 1.5) for i in days]
        
        fig_efficiency_trend = go.Figure()
        fig_efficiency_trend.add_trace(go.Scatter(
            x=days,
            y=efficiency_trend,
            mode='lines+markers',
            name='Efficiency %',
            line=dict(color='#2a5298', width=3),
            marker=dict(size=8)
        ))
        
        fig_efficiency_trend.add_hline(
            y=np.mean(efficiency_trend), 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Average: {np.mean(efficiency_trend):.1f}%"
        )
        
        fig_efficiency_trend.update_layout(
            title='Daily Drilling Efficiency',
            xaxis_title='Day',
            yaxis_title='Efficiency %',
            yaxis_range=[80, 95]
        )
        
        st.plotly_chart(fig_efficiency_trend, use_container_width=True)
    
    with col2:
        # Cost efficiency analysis
        st.subheader("💰 Cost Efficiency Analysis")
        
        # Sample cost data
        cost_data = {
            'Category': ['Equipment', 'Labor', 'Materials', 'Overhead'],
            'Budgeted': [15000, 25000, 8000, 12000],
            'Actual': [14200, 23800, 7600, 11400],
            'Variance': [800, 1200, 400, 600]
        }
        
        cost_df = pd.DataFrame(cost_data)
        
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            name='Budgeted',
            x=cost_df['Category'],
            y=cost_df['Budgeted'],
            marker_color='lightblue'
        ))
        fig_cost.add_trace(go.Bar(
            name='Actual',
            x=cost_df['Category'],
            y=cost_df['Actual'],
            marker_color='darkblue'
        ))
        
        fig_cost.update_layout(
            title='Budget vs Actual Costs',
            xaxis_title='Cost Category',
            yaxis_title='Amount (USD)',
            barmode='group'
        )
        
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Cost savings summary
        total_savings = cost_df['Variance'].sum()
        st.metric(
            label="Total Cost Savings",
            value=f"${total_savings:,}",
            delta=f"{(total_savings/cost_df['Budgeted'].sum()*100):.1f}% under budget"
        )
    
    # Export Section
    st.header("📤 Export & Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Drilling Report", use_container_width=True):
            # Generate comprehensive drilling report
            drilling_report = {
                'Job Information': job_info,
                'Drilling Performance': {
                    'Mill Operations': mill_perf,
                    'CT Operations': ct_perf,
                    'Overall Efficiency': efficiency.get('drilling_efficiency', 88)
                },
                'Key Metrics': {
                    'Total Activities': ops_freq.get('total_activities', 78),
                    'Total Work Hours': ops_freq.get('total_work_hours', 68.5),
                    'Equipment Success Rate': equipment_freq.get('deployment_success_rate', 83.3),
                    'Safety Score': efficiency.get('safety_score', 98)
                },
                'Equipment Status': equipment_usage,
                'Recommendations': recommendations
            }
            
            st.download_button(
                label="Download Drilling Report (JSON)",
                data=json.dumps(drilling_report, indent=2),
                file_name=f"YJOS_Drilling_Report_{job_info.get('ticket_number', 'DEMO')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📈 Download Data Tables", use_container_width=True):
            if daily_breakdown:
                # Prepare comprehensive CSV data
                daily_csv = pd.DataFrame(daily_breakdown)
                equipment_csv = pd.DataFrame([
                    {'Tool': tool, **info} for tool, info in equipment_usage.items()
                ])
                
                # Combine data
                combined_data = {
                    'Daily Operations': daily_csv.to_csv(index=False),
                    'Equipment Data': equipment_csv.to_csv(index=False)
                }
                
                st.download_button(
                    label="Download Daily Operations CSV",
                    data=daily_csv.to_csv(index=False),
                    file_name=f"YJOS_Daily_Operations_{job_info.get('ticket_number', 'DEMO')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data available for download")
    
    with col3:
        if st.button("🎯 Schedule Maintenance", use_container_width=True):
            # Show maintenance scheduling interface
            maintenance_tools = [tool for tool, info in equipment_usage.items() 
                               if info.get('maintenance_due', False)]
            
            if maintenance_tools:
                st.success(f"Maintenance scheduled for: {', '.join(maintenance_tools)}")
                st.info("Maintenance scheduling would integrate with your maintenance management system!")
            else:
                st.info("No tools currently require maintenance scheduling.")
    
    # Footer with drilling-specific info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🛠️ YJOS Drillout Analytics Dashboard | Advanced Drilling Operations Intelligence</p>
        <p>📧 Contact: drilling-analytics@yjos.com | 📞 Support: 1-800-YJOS-DRILL</p>
        <p>Specialized for Mill Operations, CT Drilling, and Equipment Optimization</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
