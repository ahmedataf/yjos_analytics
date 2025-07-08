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
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
}
.metric-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #2a5298;
    margin-bottom: 1rem;
}
.success-metric { border-left-color: #28a745; }
.warning-metric { border-left-color: #ffc107; }
.danger-metric { border-left-color: #dc3545; }
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
            extractor = YJOSDataExtractor()
            data = extractor.process_uploaded_file(uploaded_file)
            st.sidebar.success("✅ File processed successfully!")
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
        """)

def display_dashboard(data, show_detailed_breakdown, show_equipment_analysis, show_recommendations):
    """Display the main dashboard with all analytics"""
    
    # Job Summary Section
    st.header("📋 Job Summary")
    job_info = data['job_summary']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Customer</h4>
            <h3>{job_info['customer_name']}</h3>
            <p>Ticket: {job_info['ticket_number']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Job Details</h4>
            <h3>{job_info['job_type']}</h3>
            <p>{job_info['well_number']} | {job_info['county']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Duration</h4>
            <h3>{job_info['duration_days']} Days</h3>
            <p>{job_info['date_started']} to {job_info['date_ended']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card success-metric">
            <h4>Status</h4>
            <h3>Completed</h3>
            <p>Supervisor: {job_info['day_supervisor']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Performance Indicators
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    ops_freq = data['operational_frequency']
    efficiency = data['efficiency_metrics']
    
    with col1:
        st.metric(
            label="Total Activities",
            value=ops_freq['total_activities'],
            delta=f"{ops_freq['avg_activities_per_day']:.1f} per day"
        )
    
    with col2:
        st.metric(
            label="Work Hours",
            value=f"{ops_freq['total_work_hours']:.1f}",
            delta=f"{ops_freq['avg_hours_per_day']:.1f} per day"
        )
    
    with col3:
        st.metric(
            label="Efficiency Rate",
            value=f"{efficiency['activities_per_hour']:.2f}",
            delta="activities/hour"
        )
    
    with col4:
        st.metric(
            label="Equipment Success",
            value=f"{data['equipment_frequency']['deployment_success_rate']:.0f}%",
            delta="deployment success"
        )
    
    with col5:
        st.metric(
            label="Safety Score",
            value=f"{efficiency['safety_score']:.0f}",
            delta="out of 100"
        )
    
    # Operational Frequency Charts
    st.header("📈 Operational Frequency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily Activities Chart
        daily_data = pd.DataFrame(data['daily_breakdown'])
        
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
    
    # Equipment Analysis Section
    if show_equipment_analysis:
        st.header("🔧 Equipment Utilization Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Equipment Usage Frequency
            equipment_data = data['equipment_usage']
            eq_df = pd.DataFrame([
                {
                    'Tool': tool,
                    'Usage Count': info['usage_count'],
                    'Success Rate': info['success_rate'],
                    'Avg Deployment Time': info['avg_deployment_time']
                }
                for tool, info in equipment_data.items()
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
            performance_dist = data['equipment_frequency']['performance_distribution']
            
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
        
        # Equipment Details Table
        st.subheader("🔍 Equipment Details")
        
        # Style the dataframe
        eq_styled = eq_df.style.format({
            'Success Rate': '{:.0f}%',
            'Avg Deployment Time': '{:.1f}h'
        }).background_gradient(
            subset=['Success Rate'], 
            cmap='RdYlGn', 
            vmin=0, 
            vmax=100
        )
        
        st.dataframe(eq_styled, use_container_width=True)
    
    # Detailed Daily Breakdown
    if show_detailed_breakdown:
        st.header("📅 Detailed Daily Breakdown")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "⏱️ Time Analysis", "🛠️ Equipment by Day"])
        
        with tab1:
            # Comprehensive daily table
            daily_detailed = pd.DataFrame(data['daily_breakdown'])
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
            for day_data in data['daily_breakdown']:
                for equipment in day_data['equipment']:
                    equipment_by_day.append({
                        'Day': day_data['day'],
                        'Date': day_data['date'],
                        'Equipment': equipment
                    })
            
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
    
    # Recommendations Section
    if show_recommendations:
        st.header("💡 AI-Powered Recommendations")
        
        recommendations = data['recommendations']
        
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
    
    # Export Section
    st.header("📤 Export & Reports")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Summary Report", use_container_width=True):
            # Generate summary report
            summary_data = {
                'Job Information': job_info,
                'Key Metrics': {
                    'Total Activities': ops_freq['total_activities'],
                    'Total Work Hours': ops_freq['total_work_hours'],
                    'Equipment Success Rate': data['equipment_frequency']['deployment_success_rate'],
                    'Safety Score': efficiency['safety_score']
                },
                'Recommendations': recommendations
            }
            
            st.download_button(
                label="Download JSON Report",
                data=json.dumps(summary_data, indent=2),
                file_name=f"YJOS_Report_{job_info['ticket_number']}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📈 Download Data Tables", use_container_width=True):
            # Prepare CSV data
            daily_csv = pd.DataFrame(data['daily_breakdown']).to_csv(index=False)
            
            st.download_button(
                label="Download Daily Data CSV",
                data=daily_csv,
                file_name=f"YJOS_Daily_Data_{job_info['ticket_number']}.csv",
                mime="text/csv"
            )
    
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