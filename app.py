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
    page_title="YJOS Field Analytics",
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
        <h1>🛠️ YJOS Field Data Analytics Dashboard</h1>
        <p>Automated Field Operations Analysis & Frequency Tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    
    # File Upload Section
    st.sidebar.header("📁 Data Upload")
    uploaded_file = st.sidebar.file_uploader(
        "Upload YJOS Excel File",
        type=['xlsx', 'xls'],
        help="Upload your YJOS Field Tool Kit Excel file for analysis"
    )
    
    # Demo Data Toggle
    use_demo = st.sidebar.checkbox("Use Demo Data", value=True, help="Use sample data for demonstration")
    
    # Analysis Options
    st.sidebar.header("⚙️ Analysis Options")
    show_detailed_breakdown = st.sidebar.checkbox("Show Detailed Breakdown", value=True)
    show_equipment_analysis = st.sidebar.checkbox("Show Equipment Analysis", value=True)
    show_recommendations = st.sidebar.checkbox("Show Recommendations", value=True)
    
    # Initialize data
    if use_demo or uploaded_file is not None:
        if uploaded_file is not None:
            st.sidebar.info("📤 Processing uploaded file...")
            try:
                extractor = YJOSDataExtractor()
                data = extractor.process_uploaded_file(uploaded_file)
                st.sidebar.success("✅ Real file processed successfully!")
            except Exception as e:
                st.sidebar.warning(f"⚠️ File processing failed, using demo data. Error: {str(e)}")
                extractor = YJOSDataExtractor()
                data = extractor.get_demo_data()
        else:
            extractor = YJOSDataExtractor()
            data = extractor.get_demo_data()
            st.sidebar.success("✅ Demo data loaded successfully!")
        
        # Main Dashboard Content
        display_dashboard(data, show_detailed_breakdown, show_equipment_analysis, show_recommendations)
    else:
        st.info("👆 Please upload an Excel file or enable demo data to begin analysis.")
        
        # Show sample upload instructions
        st.markdown("""
        ### 📋 How to Use This Dashboard
        
        1. **Upload Your Excel File**: Use the sidebar to upload your YJOS Field Tool Kit Excel file
        2. **Automatic Processing**: The system will automatically extract and analyze your data
        3. **View Analytics**: Review operational frequency, equipment usage, and efficiency metrics
        4. **Export Results**: Download reports and charts for presentations
        
        ### 🎯 What Gets Analyzed
        - **Job Information**: Customer details, duration, location
        - **Daily Operations**: Activities, work hours, equipment usage
        - **Equipment Performance**: Tool efficiency, failure rates, maintenance needs
        - **Safety Metrics**: Incidents, compliance, observations
        - **Efficiency Trends**: Productivity patterns and recommendations
        
        ### 📊 Demo Features
        Enable "Use Demo Data" to see the dashboard with sample YJOS field data.
        """)

def display_dashboard(data, show_detailed_breakdown, show_equipment_analysis, show_recommendations):
    """Display the main dashboard with all analytics"""
    
    # Job Summary Section
    st.header("📋 Job Summary")
    job_info = data.get('job_summary', {})
    st.write("DEBUG - Extracted data:", job_info)  # Add this line temporarily
    
    # Use native Streamlit metrics for better reliability
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👤 Customer",
            value=job_info.get('customer_name', 'N/A'),
            delta=f"Ticket: {job_info.get('ticket_number', 'N/A')}"
        )

    with col2:
        st.metric(
            label="🛠️ Job Details", 
            value=job_info.get('job_type', 'N/A'),
            delta=f"{job_info.get('well_number', 'N/A')} | {job_info.get('county', 'N/A')}"
        )

    with col3:
        st.metric(
            label="⏱️ Duration",
            value=f"{job_info.get('duration_days', 0)} Days",
            delta=f"{job_info.get('date_started', 'N/A')} to {job_info.get('date_ended', 'N/A')}"
        )

    with col4:
        st.metric(
            label="✅ Status",
            value="Completed",
            delta=f"Supervisor: {job_info.get('day_supervisor', 'N/A')}"
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
            value=ops_freq.get('total_activities', 0),
            delta=f"{ops_freq.get('avg_activities_per_day', 0):.1f} per day"
        )
    
    with col2:
        st.metric(
            label="Work Hours",
            value=f"{ops_freq.get('total_work_hours', 0):.1f}",
            delta=f"{ops_freq.get('avg_hours_per_day', 0):.1f} per day"
        )
    
    with col3:
        st.metric(
            label="Efficiency Rate",
            value=f"{efficiency.get('activities_per_hour', 0):.2f}",
            delta="activities/hour"
        )
    
    with col4:
        st.metric(
            label="Equipment Success",
            value=f"{equipment_freq.get('deployment_success_rate', 0):.0f}%",
            delta="deployment success"
        )
    
    with col5:
        st.metric(
            label="Safety Score",
            value=f"{efficiency.get('safety_score', 100):.0f}",
            delta="out of 100"
        )
    
    # Operational Frequency Charts
    st.header("📈 Operational Frequency Analysis")
    
    col1, col2 = st.columns(2)
    
    daily_breakdown = data.get('daily_breakdown', [])
    if daily_breakdown:
        daily_data = pd.DataFrame(daily_breakdown)
        
        with col1:
            # Daily Activities Chart
            fig_activities = px.bar(
                daily_data,
                x='day',
                y='activities',
                title='Daily Activities Frequency',
                labels={'day': 'Day', 'activities': 'Number of Activities'},
                color='activities',
                color_continuous_scale='Blues'
            )
            fig_activities.update_layout(showlegend=False)
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
                # Equipment Usage Frequency
                eq_df = pd.DataFrame([
                    {
                        'Tool': tool,
                        'Usage Count': info.get('usage_count', 0),
                        'Success Rate': info.get('success_rate', 0),
                        'Avg Deployment Time': info.get('avg_deployment_time', 0)
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
                    hover_data=['Avg Deployment Time']
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
            
            # Equipment Details Table
            st.subheader("🔍 Equipment Details")
            
            # Create a color-coded display
            eq_display = eq_df.copy()
            
            # Add status indicators based on success rate
            def get_status_emoji(success_rate):
                if success_rate >= 90:
                    return "🟢 Excellent"
                elif success_rate >= 70:
                    return "🟡 Good"
                else:
                    return "🔴 Needs Attention"
            
            eq_display['Status'] = eq_display['Success Rate'].apply(get_status_emoji)
            eq_display['Success Rate'] = eq_display['Success Rate'].apply(lambda x: f"{x:.0f}%")
            eq_display['Avg Deployment Time'] = eq_display['Avg Deployment Time'].apply(lambda x: f"{x:.1f}h")
            
            st.dataframe(eq_display, use_container_width=True)
        else:
            st.warning("No equipment usage data available")
    
    # Detailed Daily Breakdown
    if show_detailed_breakdown and daily_breakdown:
        st.header("📅 Detailed Daily Breakdown")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "⏱️ Time Analysis", "🛠️ Equipment by Day"])
        
        with tab1:
            # Comprehensive daily table
            daily_detailed = pd.DataFrame(daily_breakdown)
            daily_detailed['Efficiency'] = (daily_detailed['activities'] / daily_detailed['work_hours']).round(2)
            daily_detailed['Equipment Count'] = daily_detailed['equipment'].apply(len)
            
            st.dataframe(
                daily_detailed[['day', 'date', 'activities', 'work_hours', 'downtime', 'Equipment Count', 'Efficiency']],
                use_container_width=True
            )
        
        with tab2:
            # Time trend analysis
            fig_trend = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Activities Trend', 'Hours Trend'),
                vertical_spacing=0.1
            )
            
            fig_trend.add_trace(
                go.Scatter(
                    x=daily_data['day'],
                    y=daily_data['activities'],
                    mode='lines+markers',
                    name='Activities',
                    line=dict(color='#2a5298', width=3)
                ),
                row=1, col=1
            )
            
            fig_trend.add_trace(
                go.Scatter(
                    x=daily_data['day'],
                    y=daily_data['work_hours'],
                    mode='lines+markers',
                    name='Work Hours',
                    line=dict(color='#28a745', width=3)
                ),
                row=2, col=1
            )
            
            fig_trend.update_layout(height=500, title_text="Operational Trends Over Time")
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with tab3:
            # Equipment usage by day
            equipment_by_day = []
            for day_data in daily_breakdown:
                for equipment in day_data.get('equipment', []):
                    equipment_by_day.append({
                        'Day': day_data['day'],
                        'Date': day_data['date'],
                        'Equipment': equipment
                    })
            
            if equipment_by_day:
                eq_day_df = pd.DataFrame(equipment_by_day)
                
                # Create heatmap-style visualization
                fig_eq_heatmap = px.density_heatmap(
                    eq_day_df,
                    x='Day',
                    y='Equipment',
                    title='Equipment Usage Pattern by Day',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_eq_heatmap, use_container_width=True)
            else:
                st.info("No equipment usage pattern data available")
    
    # Recommendations Section
    if show_recommendations:
        st.header("💡 AI-Powered Recommendations")
        
        recommendations = data.get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                if 'peak' in rec.lower() or 'optimal' in rec.lower():
                    rec_type = "success-metric"
                    icon = "✅"
                elif 'maintenance' in rec.lower() or 'review' in rec.lower():
                    rec_type = "warning-metric"
                    icon = "⚠️"
                elif 'opportunity' in rec.lower() or 'optimize' in rec.lower():
                    rec_type = "metric-card"
                    icon = "🎯"
                else:
                    rec_type = "metric-card"
                    icon = "💡"
                
                st.markdown(f"""
                <div class="metric-card {rec_type}">
                    <h4>{icon} Recommendation {i}</h4>
                    <p>{rec}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recommendations available")
    
    # Export Section
    st.header("📤 Export & Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Summary Report", use_container_width=True):
            # Generate summary report
            summary_data = {
                'Job Information': job_info,
                'Key Metrics': {
                    'Total Activities': ops_freq.get('total_activities', 0),
                    'Total Work Hours': ops_freq.get('total_work_hours', 0),
                    'Equipment Success Rate': equipment_freq.get('deployment_success_rate', 0),
                    'Safety Score': efficiency.get('safety_score', 100)
                },
                'Recommendations': recommendations
            }
            
            st.download_button(
                label="Download JSON Report",
                data=json.dumps(summary_data, indent=2),
                file_name=f"YJOS_Report_{job_info.get('ticket_number', 'DEMO')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📈 Download Data Tables", use_container_width=True):
            if daily_breakdown:
                # Prepare CSV data
                daily_csv = pd.DataFrame(daily_breakdown).to_csv(index=False)
                
                st.download_button(
                    label="Download Daily Data CSV",
                    data=daily_csv,
                    file_name=f"YJOS_Daily_Data_{job_info.get('ticket_number', 'DEMO')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No daily data available for download")
    
    with col3:
        if st.button("🎯 Schedule Follow-up", use_container_width=True):
            st.success("Follow-up scheduling feature would integrate with your CRM system!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>🛠️ YJOS Field Analytics Dashboard | Powered by Advanced Data Extraction & AI Analytics</p>
        <p>📧 Contact: analytics@yjos.com | 📞 Support: 1-800-YJOS-HELP</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
