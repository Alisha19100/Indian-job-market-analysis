import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import pickle
import os

# ════════════════════════════════════════════════════════════════════
#  CUSTOM CSS STYLING - DARK THEME JOB MARKET ANALYSIS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Global background and text colors */
    :root {
        --primary-dark: #0f1419;
        --secondary-dark: #1a1f2e;
        --accent-blue: #2563eb;
        --accent-orange: #f97316;
        --accent-green: #10b981;
        --accent-purple: #8b5cf6;
    }
    
    /* Main container background */
    .main {
        background-color: #0f1419 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0f1419 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a1f2e !important;
        border-right: 2px solid #2563eb !important;
    }
    
    /* Text colors */
    body, p, span, h1, h2, h3, h4, h5, h6 {
        color: #e5e7eb !important;
    }
    
    /* Header texts */
    h1, h2, h3 {
        color: #f3f4f6 !important;
        font-weight: 700 !important;
    }
    
    /* Dashboard title styling */
    .main-title {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1e3c72 100%);
        border-radius: 15px;
        color: #f0f9ff;
        margin-bottom: 2rem;
        border: 2px solid #2563eb;
        box-shadow: 0 8px 16px rgba(37, 99, 235, 0.3);
    }
    
    .main-title h1 {
        margin: 0;
        font-size: 2.5rem;
        color: #fff !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    .main-title p {
        margin: 0.5rem 0 0 0;
        color: #bfdbfe !important;
        font-size: 1.1rem;
    }
    
    /* Label styling */
    label {
        color: #e5e7eb !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stWidgetLabel"] label {
        color: #e5e7eb !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Input fields - no !important on svg or complex selectors */
    input {
        background-color: #1a1f2e !important;
        color: #e5e7eb !important;
        border: 1px solid #2563eb !important;
    }
    
    input::placeholder {
        color: #6b7280 !important;
    }
    
    select {
        background-color: #1a1f2e !important;
        color: #e5e7eb !important;
        border: 1px solid #2563eb !important;
    }
    
    textarea {
        background-color: #1a1f2e !important;
        color: #e5e7eb !important;
        border: 1px solid #2563eb !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%) !important;
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 2px solid #2563eb;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-weight: 600;
        color: #9ca3af !important;
        border-radius: 8px 8px 0 0;
        background-color: transparent;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #f97316 !important;
        border-bottom: 3px solid #f97316 !important;
    }
    
    /* Dropdown styling */
    [data-baseweb="select"] {
        background-color: #1a1f2e !important;
    }
    
    [data-baseweb="select"] input {
        background-color: #1a1f2e !important;
        color: #e5e7eb !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #1a1f2e !important;
    }
    
    [data-baseweb="menu"] li {
        background-color: #1a1f2e !important;
        color: #e5e7eb !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background-color: rgba(37, 99, 235, 0.3) !important;
        color: #fff !important;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #1a1f2e !important;
        border-left: 4px solid #f97316 !important;
        border-radius: 8px !important;
        color: #e5e7eb !important;
    }
    
    /* Data frame styling */
    [data-testid="stDataFrame"] {
        background-color: #1a1f2e !important;
        color: #e5e7eb !important;
    }
    
    /* Metric container */
    [data-testid="metric-container"] {
        background-color: rgba(37, 99, 235, 0.1);
        border: 1px solid #2563eb;
        border-radius: 12px;
        padding: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="India Job Market Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    df_tech     = pd.read_csv('data/df_tech_clean.csv')
    df_salary   = pd.read_csv('data/df_salary.csv')
    df_tech_sal = pd.read_csv('data/df_tech_salary.csv')
    df_rated    = pd.read_csv('data/df_rated.csv')

    for df in [df_tech, df_salary, df_tech_sal, df_rated]:
        if 'avgSalary_LPA' not in df.columns and 'avgSalary' in df.columns:
            df['avgSalary_LPA'] = df['avgSalary'] / 100000

    for df in [df_tech, df_salary, df_tech_sal]:
        if 'avgExperience' not in df.columns:
            df['avgExperience'] = (
                df['minimumExperience'] + df['maximumExperience']
            ) / 2

    city_mapping = {
        'Hybrid - Hyderabad': 'Hyderabad',
        'Hybrid - Bengaluru': 'Bangalore',
        'Hybrid - Pune':      'Pune',
        'Hybrid - Chennai':   'Chennai',
        'Hybrid - Noida':     'Noida',
        'Hybrid - Gurugram':  'Gurgaon',
        'Bengaluru':          'Bangalore',
        'Bangalore Rural':    'Bangalore',
        'Gurugram':           'Gurgaon',
        'Gurgaon/Gurugram':   'Gurgaon',
        'Navi Mumbai':        'Mumbai',
        'Mumbai Suburban':    'Mumbai',
        'Thane':              'Mumbai',
        'Pune(Chakan)':       'Pune',
        'Pimpri-Chinchwad':   'Pune',
        'Ghaziabad':          'Delhi NCR',
        'Faridabad':          'Delhi NCR',
        'Greater Noida':      'Noida',
        'Delhi':              'Delhi NCR',
        'Noida':              'Delhi NCR',
        'Gurgaon':            'Delhi NCR',
    }
    region_mapping = {
        'Bangalore':  'South', 'Hyderabad': 'South', 'Chennai':    'South',
        'Kochi':      'South', 'Coimbatore':'South', 'Mysuru':     'South',
        'Mumbai':     'West',  'Pune':      'West',  'Ahmedabad':  'West',
        'Surat':      'West',  'Vadodara':  'West',  'Nashik':     'West',
        'Delhi NCR':  'North', 'Chandigarh':'North', 'Jaipur':    'North',
        'Lucknow':    'North', 'Ludhiana':  'North', 'Mohali':     'North',
        'Kolkata':    'East',  'Guwahati':  'East',
        'Remote':     'Remote'
    }

    for df in [df_salary, df_tech_sal, df_rated]:
        if 'city' not in df.columns:
            df['city'] = df['location'].str.split(',').str[0].str.strip()
            df['city'] = df['city'].replace(city_mapping)
        if 'city_clean' not in df.columns:
            top_cities = df_tech['city'].value_counts().head(20).index
            df['city_clean'] = df['city'].apply(
                lambda x: x if x in top_cities else 'Other'
            )
        if 'region' not in df.columns:
            df['region'] = df['city'].map(region_mapping).fillna('Other')
        if 'expCategory' not in df.columns and 'avgExperience' in df.columns:
            def exp_category(exp):
                if exp <= 1:   return 'Fresher (0-1 yrs)'
                elif exp <= 3: return 'Junior (1-3 yrs)'
                elif exp <= 6: return 'Mid (3-6 yrs)'
                elif exp <= 10:return 'Senior (6-10 yrs)'
                else:          return 'Expert (10+ yrs)'
            df['expCategory'] = df['avgExperience'].apply(exp_category)

    return df_tech, df_salary, df_tech_sal, df_rated

# ════════════════════════════════════════════════════════════════════
# DATA VALIDATION FUNCTION
# ════════════════════════════════════════════════════════════════════
def validate_data(df, required_columns=None):
    """
    Validate DataFrame integrity.
    
    EXPLANATION:
    - Checks if DataFrame exists and is not empty
    - Verifies required columns are present
    - Helps prevent errors in data processing
    
    ARGS:
        df: DataFrame to validate
        required_columns: List of column names to check
        
    RETURN:
        bool: True if valid, False otherwise
    """
    if df is None or len(df) == 0:
        return False
    
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            st.warning(f" Missing columns: {', '.join(missing)}")
            return False
    
    return True

df_tech, df_salary, df_tech_sal, df_rated = load_data()

# ── HEADER ────────────────────────────────────────────
st.markdown("""
<div class="main-title">
    <h1>India Job Market Dashboard</h1>
    <p> Analyzing 97,000+ job postings across India</p>
</div>
""", unsafe_allow_html=True)

# ── TOP METRICS ───────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Job Postings", f"{len(df_tech):,}")
with col2:
    st.metric("Unique Companies", f"{df_tech['companyName'].nunique():,}")
with col3:
    st.metric("Unique Cities", f"{df_tech['city'].nunique():,}")
with col4:
    st.metric("Avg Salary (LPA)", f"₹{df_tech_sal['avgSalary_LPA'].mean():.1f}")

st.markdown("---")

# ── SIDEBAR FILTERS ───────────────────────────────────
st.sidebar.title(" Filters")
st.sidebar.markdown("Use filters to explore specific segments")

all_cities   = ['All'] + sorted(df_tech['city'].value_counts().head(15).index.tolist())
selected_city = st.sidebar.selectbox("Select City", all_cities)

all_exp      = ['All'] + df_tech['expCategory'].unique().tolist()
selected_exp  = st.sidebar.selectbox("Select Experience Level", all_exp)

df_filtered = df_tech.copy()
if selected_city != 'All':
    df_filtered = df_filtered[df_filtered['city'] == selected_city]
if selected_exp != 'All':
    df_filtered = df_filtered[df_filtered['expCategory'] == selected_exp]

st.sidebar.markdown(f"**Showing: {len(df_filtered):,} jobs**")

# ── INVALID CITIES (used throughout) ──────────────────
invalid_cities = ['Hybrid', 'Remote', 'Work From Home',
                  'Onsite', 'Work From Office', 'Wfo', 'Wfh']

# ── ROW 1 — SKILLS CHARTS ─────────────────────────────
st.subheader(" Most In-Demand Skills")
col1, col2 = st.columns(2)

with col1:
    all_skills = []
    for skills in df_salary['tagsAndSkills'].dropna():
        all_skills.extend([s.strip() for s in skills.split(',')])
    skill_df = pd.DataFrame(
        Counter(all_skills).most_common(20),
        columns=['skill', 'count']
    )
    fig1 = px.bar(skill_df, x='count', y='skill', orientation='h',
                  title='Top 20 Skills — All Industries',
                  color='count', color_continuous_scale='Blues',
                  labels={'count': 'Job Postings', 'skill': 'Skill'})
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'},
                       height=500, showlegend=False)
    st.plotly_chart(fig1, width='stretch')

with col2:
    tech_skills = []
    for skills in df_filtered['tagsAndSkills'].dropna():
        tech_skills.extend([s.strip() for s in skills.split(',')])
    tech_skill_df = pd.DataFrame(
        Counter(tech_skills).most_common(20),
        columns=['skill', 'count']
    )
    fig2 = px.bar(tech_skill_df, x='count', y='skill', orientation='h',
                  title='Top 20 Skills — Tech Jobs Only',
                  color='count', color_continuous_scale='Greens',
                  labels={'count': 'Job Postings', 'skill': 'Skill'})
    fig2.update_layout(yaxis={'categoryorder': 'total ascending'},
                       height=500, showlegend=False)
    st.plotly_chart(fig2, width='stretch')

st.markdown("---")

# ── ROW 2 — JOB ROLES + CITIES ────────────────────────
st.subheader(" Job Roles & Cities")
col1, col2 = st.columns(2)

with col1:
    title_counts = df_filtered['title'].value_counts().head(15).reset_index()
    title_counts.columns = ['title', 'count']
    fig3 = px.bar(title_counts, x='count', y='title', orientation='h',
                  title='Top 15 Most In-Demand Job Roles',
                  color='count', color_continuous_scale='Purples',
                  labels={'count': 'Job Postings', 'title': 'Job Role'})
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'},
                       height=500, showlegend=False)
    st.plotly_chart(fig3, width='stretch')

with col2:
    df_city = df_filtered[~df_filtered['city'].str.contains(
        '|'.join(invalid_cities), case=False, na=False)]
    city_counts = df_city['city'].value_counts().head(15).reset_index()
    city_counts.columns = ['city', 'count']
    fig4 = px.bar(city_counts, x='city', y='count',
                  title='Top 15 Cities by Job Postings',
                  color='count', color_continuous_scale='Oranges',
                  labels={'count': 'Job Postings', 'city': 'City'})
    fig4.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
    st.plotly_chart(fig4, width='stretch')

st.markdown("---")

# ── ROW 3 — SALARY CHARTS ─────────────────────────────
st.subheader(" Salary Analysis")
col1, col2 = st.columns(2)

with col1:
    city_salary = df_tech_sal.groupby('city_clean')['avgSalary_LPA'].mean().reset_index()
    city_salary = city_salary[~city_salary['city_clean'].str.contains(
        '|'.join(invalid_cities), case=False, na=False)]
    city_salary = city_salary[city_salary['city_clean'] != 'Other']
    city_salary = city_salary.sort_values('avgSalary_LPA', ascending=False)
    fig5 = px.bar(city_salary, x='city_clean', y='avgSalary_LPA',
                  title='Average Salary by City (LPA)',
                  color='avgSalary_LPA', color_continuous_scale='Reds',
                  labels={'avgSalary_LPA': 'Avg Salary (LPA)', 'city_clean': 'City'})
    fig5.update_layout(xaxis_tickangle=-45, height=500, showlegend=False)
    st.plotly_chart(fig5, width='stretch')

with col2:
    exp_salary = df_tech_sal.groupby('expCategory')['avgSalary_LPA'].mean().reset_index()
    exp_salary = exp_salary.sort_values('avgSalary_LPA', ascending=False)
    fig6 = px.bar(exp_salary, x='expCategory', y='avgSalary_LPA',
                  title='Average Salary by Experience Level (LPA)',
                  color='avgSalary_LPA', color_continuous_scale='Viridis',
                  labels={'avgSalary_LPA': 'Avg Salary (LPA)', 'expCategory': 'Experience Level'})
    fig6.update_layout(xaxis_tickangle=-15, height=500, showlegend=False)
    st.plotly_chart(fig6, width='stretch')

st.markdown("---")

# ── ROW 4 — COMPANIES + RATING ────────────────────────
st.subheader(" Company Analysis")
col1, col2 = st.columns(2)

with col1:
    company_counts = df_filtered['companyName'].value_counts().head(15).reset_index()
    company_counts.columns = ['company', 'count']
    fig7 = px.bar(company_counts, x='count', y='company', orientation='h',
                  title='Top 15 Hiring Companies',
                  color='count', color_continuous_scale='Teal',
                  labels={'count': 'Job Postings', 'company': 'Company'})
    fig7.update_layout(yaxis={'categoryorder': 'total ascending'},
                       height=500, showlegend=False)
    st.plotly_chart(fig7, width='stretch')

with col2:
    fig8 = px.scatter(df_rated, x='AggregateRating', y='avgSalary_LPA',
                      title='Company Rating vs Salary',
                      color='avgSalary_LPA', color_continuous_scale='Sunset',
                      labels={'AggregateRating': 'Company Rating',
                              'avgSalary_LPA': 'Avg Salary (LPA)'},
                      opacity=0.6)
    fig8.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig8, width='stretch')

st.markdown("---")

# ── EXPERIENCE DISTRIBUTION ───────────────────────────
st.subheader(" Experience Distribution")
col1, col2 = st.columns(2)

with col1:
    exp_counts = df_filtered['expCategory'].value_counts().reset_index()
    exp_counts.columns = ['expCategory', 'count']
    fig9 = px.pie(exp_counts, values='count', names='expCategory',
                  title='Job Distribution by Experience Level',
                  color_discrete_sequence=px.colors.sequential.RdBu)
    fig9.update_traces(textposition='inside', textinfo='percent+label')
    fig9.update_layout(height=450)
    st.plotly_chart(fig9, width='stretch')

with col2:
    st.markdown("###  Key Insights")
    st.success(" **Bengaluru** leads in both job count and average salary")
    st.info(" **Python & SQL** are the most in-demand tech skills")
    st.warning(" **Junior & Mid level** roles make up 65% of all openings")
    st.error(" **Accenture & Wipro** dominate tech hiring in India")
    st.success(" Higher rated companies tend to offer **better salaries**")
    st.info(" **Data Engineer** is the top pure-data role in demand")

st.markdown("---")

# ── JOB RECOMMENDER ───────────────────────────────────
st.subheader(" Job Recommender — Find Jobs by Your Skills")

user_input = st.text_input(
    "Enter your skills (comma separated)",
    placeholder="e.g. python, sql, machine learning"
)
min_match = st.slider("Minimum skills to match", min_value=1,
                      max_value=5, value=2,
                      help="Higher = more relevant results")

if user_input:
    user_skills = [s.strip().lower() for s in user_input.split(',')]

    def match_score(row_skills, user_skills):
        if pd.isna(row_skills):
            return 0, 0
        row_skill_list = [s.strip().lower() for s in str(row_skills).split(',')]
        matches   = sum(1 for skill in user_skills if skill in row_skill_list)
        match_pct = matches / len(user_skills) * 100
        return matches, round(match_pct, 1)

    df_tech[['matchCount', 'matchPct']] = df_tech['tagsAndSkills'].apply(
        lambda x: pd.Series(match_score(x, user_skills))
    )

    generic_titles = ['application developer', 'software developer',
                      'it consultant', 'technical consultant',
                      'associate consultant', 'consultant']

    df_matched = df_tech[df_tech['matchCount'] >= min_match].copy()
    df_matched = df_matched.sort_values(['matchCount', 'matchPct'], ascending=False)
    df_matched = df_matched[~df_matched['title'].str.lower().str.contains(
        '|'.join(generic_titles), na=False)]

    if len(df_matched) == 0:
        st.warning(f"No jobs found matching {min_match}+ skills. Try lowering the minimum match slider!")
    else:
        st.success(f"Found **{len(df_matched):,}** relevant jobs for: `{', '.join(user_skills)}`")

        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Matching Jobs",     f"{len(df_matched):,}")
        with col2: st.metric("Companies Hiring",  f"{df_matched['companyName'].nunique():,}")
        with col3: st.metric("Cities",            f"{df_matched['city'].nunique():,}")
        with col4: st.metric("Avg Skill Match",   f"{df_matched['matchPct'].mean():.0f}%")

        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            top_roles = df_matched['title'].value_counts().head(10).reset_index()
            top_roles.columns = ['role', 'count']
            fig_roles = px.bar(top_roles, x='count', y='role', orientation='h',
                               title='Top 10 Relevant Job Roles',
                               color='count', color_continuous_scale='Blues',
                               labels={'count': 'Openings', 'role': 'Job Role'})
            fig_roles.update_layout(yaxis={'categoryorder': 'total ascending'},
                                    height=400, showlegend=False)
            st.plotly_chart(fig_roles, width='stretch')

        with col2:
            top_companies = df_matched['companyName'].value_counts().head(10).reset_index()
            top_companies.columns = ['company', 'count']
            fig_comp = px.bar(top_companies, x='count', y='company', orientation='h',
                              title='Top 10 Companies Hiring',
                              color='count', color_continuous_scale='Greens',
                              labels={'count': 'Openings', 'company': 'Company'})
            fig_comp.update_layout(yaxis={'categoryorder': 'total ascending'},
                                   height=400, showlegend=False)
            st.plotly_chart(fig_comp, width='stretch')

        col1, col2 = st.columns(2)

        with col1:
            df_matched_city = df_matched[~df_matched['city'].str.contains(
                '|'.join(invalid_cities), case=False, na=False)]
            top_cities = df_matched_city['city'].value_counts().head(10).reset_index()
            top_cities.columns = ['city', 'count']
            fig_city = px.bar(top_cities, x='count', y='city', orientation='h',
                              title='Top Cities Hiring for Your Skills',
                              color='count', color_continuous_scale='Oranges',
                              labels={'count': 'Openings', 'city': 'City'})
            fig_city.update_layout(yaxis={'categoryorder': 'total ascending'},
                                   height=400, showlegend=False)
            st.plotly_chart(fig_city, width='stretch')

        with col2:
            df_matched_sal = df_matched[df_matched['avgSalary'] >= 100000].copy()
            df_matched_sal['avgSalary_LPA'] = df_matched_sal['avgSalary'] / 100000
            if len(df_matched_sal) > 0:
                st.markdown("###  Expected Salary Range")
                st.info(f" Entry Level: ₹{df_matched_sal['avgSalary_LPA'].quantile(0.25):.1f} LPA")
                st.success(f" Average: ₹{df_matched_sal['avgSalary_LPA'].mean():.1f} LPA")
                st.warning(f" Senior Level: ₹{df_matched_sal['avgSalary_LPA'].quantile(0.75):.1f} LPA")
                fig_sal = px.histogram(df_matched_sal, x='avgSalary_LPA',
                                       title='Salary Distribution',
                                       color_discrete_sequence=['#636EFA'],
                                       labels={'avgSalary_LPA': 'Salary (LPA)'})
                fig_sal.update_layout(height=300)
                st.plotly_chart(fig_sal, width='stretch')
            else:
                st.info("Not enough salary data for these skills")

        st.markdown("---")
        st.markdown("###  Best Matching Job Postings")
        display_cols = ['title', 'companyName', 'city', 'expCategory', 'matchCount', 'matchPct']
        st.dataframe(
            df_matched[display_cols].head(20).reset_index(drop=True),
            width='stretch',
            column_config={
                "matchPct": st.column_config.ProgressColumn(
                    "Match %", min_value=0, max_value=100)
            }
        )

        st.markdown("---")
        st.markdown("###  Skills Also Required in These Jobs")
        st.markdown("*Other skills that appear alongside yours — consider learning these!*")

        related_skills = []
        for skills in df_matched['tagsAndSkills'].dropna():
            skill_list = [s.strip().lower() for s in skills.split(',')]
            related_skills.extend([s for s in skill_list if s not in user_skills])

        related_df = pd.DataFrame(
            Counter(related_skills).most_common(15),
            columns=['skill', 'count']
        )
        fig_related = px.bar(related_df, x='count', y='skill', orientation='h',
                             title='Skills to Learn Next ',
                             color='count', color_continuous_scale='Purples',
                             labels={'count': 'Frequency', 'skill': 'Skill'})
        fig_related.update_layout(yaxis={'categoryorder': 'total ascending'},
                                  height=500, showlegend=False)
        st.plotly_chart(fig_related, width='stretch')

st.markdown("---")

# ── RESUME SKILL GAP ANALYZER ─────────────────────────
st.subheader(" Resume Skill Gap Analyzer")
st.markdown("*Paste a job description and enter your skills — see exactly what you're missing!*")

col1, col2 = st.columns(2)
with col1:
    jd_input = st.text_area(" Paste Job Description Here", height=250,
                             placeholder="Paste the full job description here...")
with col2:
    resume_skills_input = st.text_input(
        " Enter Your Skills (comma separated)",
        placeholder="e.g. python, sql, machine learning, tableau"
    )

if jd_input and resume_skills_input:
    user_skills  = [s.strip().lower() for s in resume_skills_input.split(',')]
    master_skills = [
        'python', 'r', 'java', 'scala', 'c++', 'c#', 'javascript',
        'typescript', 'go', 'rust', 'kotlin', 'swift', 'php', 'ruby',
        'sql', 'mysql', 'postgresql', 'mongodb', 'cassandra', 'redis',
        'oracle', 'sqlite', 'nosql', 'hadoop', 'spark', 'hive', 'kafka',
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'xgboost',
        'neural networks', 'reinforcement learning', 'llm', 'transformers',
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
        'excel', 'tableau', 'power bi', 'looker', 'data studio',
        'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
        'terraform', 'jenkins', 'ci/cd', 'git', 'github', 'linux',
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'django',
        'flask', 'fastapi', 'rest api', 'graphql',
        'project management', 'agile', 'scrum', 'jira', 'confluence',
        'communication', 'leadership', 'problem solving',
        'airflow', 'dbt', 'etl', 'data pipeline', 'data warehouse',
        'snowflake', 'bigquery', 'redshift', 'databricks',
        'statistics', 'probability', 'hypothesis testing', 'regression',
        'time series', 'forecasting', 'a/b testing', 'causal inference'
    ]

    jd_lower  = jd_input.lower()
    jd_skills = list(set([skill for skill in master_skills if skill in jd_lower]))

    if len(jd_skills) == 0:
        st.warning("No recognizable skills found in job description. Try pasting a more detailed JD.")
    else:
        matched_skills = [s for s in jd_skills if s in user_skills]
        missing_skills = [s for s in jd_skills if s not in user_skills]
        extra_skills   = [s for s in user_skills if s not in jd_skills]
        match_score    = len(matched_skills) / len(jd_skills) * 100

        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("JD Skills Found",  len(jd_skills))
        with col2: st.metric("Your Matches",      len(matched_skills))
        with col3: st.metric("Skills Missing",    len(missing_skills))
        with col4: st.metric("Match Score",       f"{match_score:.0f}%")

        st.markdown("###  Your Match Score")
        if match_score >= 80:
            st.success(f" {match_score:.0f}% Match — Excellent! You're a strong candidate. Apply immediately!")
        elif match_score >= 60:
            st.info(f" {match_score:.0f}% Match — Good fit! Learn the missing skills and apply.")
        elif match_score >= 40:
            st.warning(f" {match_score:.0f}% Match — Partial fit. Work on missing skills before applying.")
        else:
            st.error(f" {match_score:.0f}% Match — Low fit. This role needs significant skill building.")

        st.progress(int(match_score))
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("###  Skills You Have")
            for skill in sorted(matched_skills):
                st.success(f" {skill.title()}")
            if not matched_skills:
                st.info("No matching skills found")
        with col2:
            st.markdown("###  Skills You're Missing")
            for skill in sorted(missing_skills):
                st.error(f" {skill.title()}")
            if not missing_skills:
                st.success("You have all required skills!")
        with col3:
            st.markdown("### Your Bonus Skills")
            st.markdown("*Skills you have beyond JD requirements*")
            for skill in sorted(extra_skills):
                st.info(f"+ {skill.title()}")
            if not extra_skills:
                st.info("No extra skills detected")

        st.markdown("---")
        skill_status = (
            [{'skill': s, 'status': ' You Have This',         'value': 1} for s in matched_skills] +
            [{'skill': s, 'status': ' You Are Missing This',  'value': 1} for s in missing_skills]
        )
        if skill_status:
            skill_gap_df = pd.DataFrame(skill_status)
            fig_gap = px.bar(skill_gap_df, x='value', y='skill',
                             color='status', orientation='h',
                             title='Skill Gap Analysis — Required vs Your Skills',
                             color_discrete_map={
                                 ' You Have This':        '#00CC96',
                                 ' You Are Missing This': '#EF553B'
                             },
                             labels={'value': '', 'skill': 'Skill'})
            fig_gap.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                height=max(400, len(skill_status) * 30),
                showlegend=True, xaxis_visible=False
            )
            st.plotly_chart(fig_gap, width='stretch')

        if missing_skills:
            st.markdown("---")
            st.markdown("###  Learning Roadmap for Missing Skills")
            resources = {
                'python':           'https://kaggle.com/learn/python',
                'sql':              'https://sqlzoo.net',
                'machine learning': 'https://kaggle.com/learn/machine-learning',
                'deep learning':    'https://fast.ai',
                'tableau':          'https://www.tableau.com/learn/training',
                'power bi':         'https://learn.microsoft.com/en-us/power-bi',
                'aws':              'https://aws.amazon.com/training',
                'docker':           'https://docs.docker.com/get-started',
                'spark':            'https://spark.apache.org/docs/latest',
                'tensorflow':       'https://www.tensorflow.org/tutorials',
                'pytorch':          'https://pytorch.org/tutorials',
                'excel':            'https://support.microsoft.com/en-us/excel',
                'git':              'https://learngitbranching.js.org',
                'statistics':       'https://www.khanacademy.org/math/statistics-probability',
            }
            for i, skill in enumerate(missing_skills[:8], 1):
                link = resources.get(skill, f'https://google.com/search?q=learn+{skill.replace(" ", "+")}')
                st.markdown(f"**{i}. {skill.title()}** → [Start Learning]({link})")

        if matched_skills:
            st.markdown("---")
            st.markdown("###  Similar Jobs in Our Dataset Matching Your Profile")

            def calc_match(row_skills, user_skills):
                if pd.isna(row_skills): return 0
                row_list = [s.strip().lower() for s in str(row_skills).split(',')]
                return sum(1 for s in user_skills if s in row_list)

            df_tech['resumeMatch'] = df_tech['tagsAndSkills'].apply(
                lambda x: calc_match(x, matched_skills))
            df_resume_matched = df_tech[
                df_tech['resumeMatch'] >= max(1, len(matched_skills) // 2)
            ].sort_values('resumeMatch', ascending=False)

            if len(df_resume_matched) > 0:
                st.success(f"Found **{len(df_resume_matched):,}** similar jobs in dataset!")
                st.dataframe(
                    df_resume_matched[['title', 'companyName', 'city',
                                       'expCategory', 'resumeMatch']].head(15).reset_index(drop=True),
                    width='stretch'
                )
            else:
                st.info("No exact matches found in dataset for your current skills.")

st.markdown("---")

# ── SALARY PREDICTOR ──────────────────────────────────
st.subheader(" Salary Predictor")
st.markdown("*Enter your role, city and experience — get expected salary range!*")

@st.cache_resource
def load_model():
    try:
        with open('model/salary_model.pkl', 'rb') as f:
            model    = pickle.load(f)
        with open('model/le_title.pkl', 'rb') as f:
            le_title = pickle.load(f)
        with open('model/le_city.pkl', 'rb') as f:
            le_city  = pickle.load(f)
        job_titles = pd.read_csv('data/job_titles.csv', header=None)[0].tolist()
        cities     = pd.read_csv('data/cities.csv',     header=None)[0].tolist()
        return model, le_title, le_city, job_titles, cities, True
    except Exception as e:
        return None, None, None, [], [], False

model, le_title, le_city, job_titles, cities, model_loaded = load_model()

if not model_loaded:
    st.warning(" Salary model files not found. Please run the model training notebook first and place the files in the `model/` folder.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_title = st.selectbox(
            " Job Role", options=sorted(job_titles),
            index=sorted(job_titles).index('data analyst')
                  if 'data analyst' in job_titles else 0
        )
    with col2:
        selected_city_pred = st.selectbox(
            " City", options=sorted(cities),
            index=sorted(cities).index('bangalore')
                  if 'bangalore' in cities else 0
        )
    with col3:
        experience = st.slider("⏳ Years of Experience",
                               min_value=0, max_value=20, value=2, step=1)

    if st.button(" Predict My Salary", width='stretch'):
        try:
            title_encoded = le_title.transform([selected_title])[0]
            city_encoded  = le_city.transform([selected_city_pred])[0]
            predicted_sal = model.predict([[title_encoded, city_encoded, experience]])[0]

            mae   = 2.68
            lower = max(1.0, predicted_sal - mae)
            upper = predicted_sal + mae

            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1: st.metric(" Minimum Expected", f"₹{lower:.1f} LPA")
            with col2: st.metric(" Predicted Salary",  f"₹{predicted_sal:.1f} LPA")
            with col3: st.metric(" Maximum Expected",  f"₹{upper:.1f} LPA")

            st.markdown("###  Salary Verdict")
            if predicted_sal >= 15:
                st.success(f" Excellent! **{selected_title.title()}** in **{selected_city_pred.title()}** "
                           f"with {experience} years exp is a high paying role!")
            elif predicted_sal >= 8:
                st.info(f" Good salary! **{selected_title.title()}** in **{selected_city_pred.title()}** "
                        f"offers a competitive package.")
            elif predicted_sal >= 4:
                st.warning(" Average salary range. Consider upskilling to move to higher paying roles.")
            else:
                st.error(" This is an entry level salary. Focus on gaining experience to grow quickly.")

            st.markdown("###  Salary Growth Projection")
            exp_range = list(range(0, 21))
            projected = [round(model.predict([[title_encoded, city_encoded, e]])[0], 2)
                         for e in exp_range]
            growth_df = pd.DataFrame({
                'Experience (Years)': exp_range,
                'Projected Salary (LPA)': projected
            })
            fig_growth = px.line(growth_df, x='Experience (Years)',
                                 y='Projected Salary (LPA)',
                                 title=f'Salary Growth — {selected_title.title()} in {selected_city_pred.title()}',
                                 markers=True, color_discrete_sequence=['#636EFA'])
            fig_growth.add_scatter(x=[experience], y=[predicted_sal],
                                   mode='markers',
                                   marker=dict(size=15, color='red', symbol='star'),
                                   name='You Are Here')
            fig_growth.update_layout(height=400)
            st.plotly_chart(fig_growth, width='stretch')

            st.markdown("###  Same Role Salary Across Cities")
            city_comparison = []
            for city in sorted(cities):
                try:
                    c_enc = le_city.transform([city])[0]
                    c_sal = model.predict([[title_encoded, c_enc, experience]])[0]
                    city_comparison.append({'City': city.title(),
                                            'Expected Salary (LPA)': round(c_sal, 2)})
                except:
                    pass
            city_comp_df = pd.DataFrame(city_comparison).sort_values(
                'Expected Salary (LPA)', ascending=False).reset_index(drop=True)

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(city_comp_df, width='stretch')
            with col2:
                fig_city_comp = px.bar(
                    city_comp_df.head(10), x='Expected Salary (LPA)', y='City',
                    orientation='h',
                    title=f'Top 10 Cities by Salary — {selected_title.title()}',
                    color='Expected Salary (LPA)', color_continuous_scale='Greens')
                fig_city_comp.update_layout(yaxis={'categoryorder': 'total ascending'},
                                            height=400, showlegend=False)
                st.plotly_chart(fig_city_comp, width='stretch')

        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.info("This job title or city may not have enough data to predict accurately.")

st.markdown("---")

# ── SKILLS DEMAND TREND ANALYSIS ──────────────────────
st.subheader(" Skills Demand Trend Analysis")
st.markdown("*Which skills are most in demand and how they compare across job categories*")

all_skills_list = []
for skills in df_tech['tagsAndSkills'].dropna():
    all_skills_list.extend([s.strip().lower() for s in skills.split(',')])
skill_freq = pd.DataFrame(Counter(all_skills_list).most_common(30),
                          columns=['skill', 'total_count'])

data_keywords = ['data analyst', 'data scientist', 'data engineer',
                 'machine learning', 'ml engineer', 'ai engineer',
                 'business analyst', 'bi analyst']
df_data_roles     = df_tech[df_tech['title'].str.contains(
    '|'.join(data_keywords), case=False, na=False)]
data_skills_list  = []
for skills in df_data_roles['tagsAndSkills'].dropna():
    data_skills_list.extend([s.strip().lower() for s in skills.split(',')])
data_skill_freq   = pd.DataFrame(Counter(data_skills_list).most_common(30),
                                  columns=['skill', 'data_count'])

dev_keywords  = ['developer', 'software engineer', 'backend',
                 'frontend', 'fullstack', 'full stack']
df_dev_roles  = df_tech[df_tech['title'].str.contains(
    '|'.join(dev_keywords), case=False, na=False)]
dev_skills_list = []
for skills in df_dev_roles['tagsAndSkills'].dropna():
    dev_skills_list.extend([s.strip().lower() for s in skills.split(',')])
dev_skill_freq = pd.DataFrame(Counter(dev_skills_list).most_common(30),
                               columns=['skill', 'dev_count'])

trend_df = skill_freq.merge(data_skill_freq, on='skill', how='left')
trend_df = trend_df.merge(dev_skill_freq, on='skill', how='left').fillna(0)
trend_df['demand_score'] = (
    trend_df['total_count'] * 0.5 +
    trend_df['data_count']  * 0.3 +
    trend_df['dev_count']   * 0.2
).round(0).astype(int)

def demand_category(score):
    if score >= trend_df['demand_score'].quantile(0.75): return ' Very High Demand'
    elif score >= trend_df['demand_score'].quantile(0.50): return ' High Demand'
    elif score >= trend_df['demand_score'].quantile(0.25): return ' Medium Demand'
    else: return ' Lower Demand'

trend_df['demand_level'] = trend_df['demand_score'].apply(demand_category)
trend_df = trend_df.sort_values('demand_score', ascending=False).head(25)

tab1, tab2, tab3 = st.tabs([" Overall Demand",
                             " Data Roles vs Dev Roles",
                             " Skills Demand Table"])
with tab1:
    fig_trend = px.bar(trend_df, x='demand_score', y='skill', orientation='h',
                       color='demand_level',
                       title='Top 25 Skills by Demand Score',
                       color_discrete_map={
                           ' Very High Demand': '#FF4B4B',
                           ' High Demand':      '#FF8C00',
                           ' Medium Demand':    '#1F77B4',
                           ' Lower Demand':     '#7F7F7F'
                       },
                       labels={'demand_score': 'Demand Score', 'skill': 'Skill'})
    fig_trend.update_layout(yaxis={'categoryorder': 'total ascending'},
                            height=650, legend_title='Demand Level')
    st.plotly_chart(fig_trend, width='stretch')
    top_3 = trend_df.head(3)['skill'].tolist()
    st.info(f" **Top 3 Most In-Demand Skills:** {', '.join([s.title() for s in top_3])}")

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        fig_data = px.bar(data_skill_freq.head(15), x='data_count', y='skill',
                          orientation='h', title='Top Skills in Data/ML Roles',
                          color='data_count', color_continuous_scale='Blues',
                          labels={'data_count': 'Frequency', 'skill': 'Skill'})
        fig_data.update_layout(yaxis={'categoryorder': 'total ascending'},
                               height=500, showlegend=False)
        st.plotly_chart(fig_data, width='stretch')
    with col2:
        fig_dev = px.bar(dev_skill_freq.head(15), x='dev_count', y='skill',
                         orientation='h', title='Top Skills in Dev/Engineering Roles',
                         color='dev_count', color_continuous_scale='Greens',
                         labels={'dev_count': 'Frequency', 'skill': 'Skill'})
        fig_dev.update_layout(yaxis={'categoryorder': 'total ascending'},
                              height=500, showlegend=False)
        st.plotly_chart(fig_dev, width='stretch')

    st.markdown("###  Skills That Appear in BOTH Data + Dev Roles")
    overlap = set(data_skill_freq['skill'].head(20)) & set(dev_skill_freq['skill'].head(20))
    if overlap:
        cols = st.columns(4)
        for i, skill in enumerate(sorted(list(overlap))):
            cols[i % 4].success(f" {skill.title()}")
    st.markdown("*These overlap skills are the most versatile — learning them opens doors in both data and dev careers!*")

with tab3:
    display_trend = trend_df[['skill', 'total_count', 'data_count',
                               'dev_count', 'demand_score', 'demand_level']].copy()
    display_trend.columns = ['Skill', 'Total Jobs', 'Data Role Jobs',
                              'Dev Role Jobs', 'Demand Score', 'Demand Level']
    display_trend['Skill'] = display_trend['Skill'].str.title()
    st.dataframe(
        display_trend.reset_index(drop=True), width='stretch',
        column_config={
            "Demand Score": st.column_config.ProgressColumn(
                "Demand Score", min_value=0,
                max_value=int(display_trend['Demand Score'].max()))
        }
    )
    csv = display_trend.to_csv(index=False)
    st.download_button(label=" Download Skills Report", data=csv,
                       file_name="india_skills_demand_report.csv", mime="text/csv")

st.markdown("---")

# ── FRESHER JOBS FINDER ───────────────────────────────
st.subheader(" Fresher Jobs Finder")
st.markdown("*Jobs specifically for 0-2 years experience — filtered and sorted for you*")

col1, col2, col3 = st.columns(3)
with col1:
    fresher_city = st.selectbox(
        " Preferred City",
        ['All'] + sorted(df_tech[~df_tech['city'].str.contains(
            'Hybrid|Remote|Work From Home|Onsite|Wfo|Wfh',
            case=False, na=False)]['city'].value_counts().head(15).index.tolist()),
        key='fresher_city'
    )
with col2:
    fresher_skill = st.text_input(" Filter by Skill (optional)",
                                   placeholder="e.g. python, sql",
                                   key='fresher_skill')
with col3:
    min_rating = st.slider("Minimum Company Rating",
                            min_value=0.0, max_value=5.0,
                            value=0.0, step=0.5, key='fresher_rating')

job_type = st.radio(" Job Type",
                    ['All Jobs', ' Tech Only', ' Non-Tech Only'],
                    horizontal=True, key='fresher_job_type')

tech_keywords_fresher = [
    'developer', 'engineer', 'analyst', 'scientist',
    'architect', 'devops', 'data ', 'software', 'python',
    'java ', 'sql', 'cloud', 'backend', 'frontend',
    'fullstack', 'full stack', 'machine learning',
    'deep learning', 'nlp', 'aws', 'azure', 'testing',
    'automation', 'sap', 'salesforce', 'database',
    'network', 'security', 'cyber', 'blockchain',
    'android', 'ios', 'react', 'angular', 'tableau'
]
tech_pattern = '|'.join(tech_keywords_fresher)

df_fresher = df_tech[df_tech['avgExperience'] <= 2].copy()

if job_type == ' Tech Only':
    df_fresher = df_fresher[df_fresher['title'].str.contains(
        tech_pattern, case=False, na=False)]
elif job_type == ' Non-Tech Only':
    df_fresher = df_fresher[~df_fresher['title'].str.contains(
        tech_pattern, case=False, na=False)]

if fresher_city != 'All':
    df_fresher = df_fresher[df_fresher['city'] == fresher_city]
if fresher_skill:
    pattern = '|'.join([s.strip().lower() for s in fresher_skill.split(',')])
    df_fresher = df_fresher[df_fresher['tagsAndSkills'].str.contains(
        pattern, case=False, na=False)]
if min_rating > 0:
    df_fresher = df_fresher[df_fresher['AggregateRating'] >= min_rating]

st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric(" Fresher Jobs Found",  f"{len(df_fresher):,}")
with col2: st.metric(" Companies Hiring",    f"{df_fresher['companyName'].nunique():,}")
with col3: st.metric(" Cities",              f"{df_fresher['city'].nunique():,}")
with col4:
    df_f_sal = df_fresher[df_fresher['avgSalary'] >= 100000]
    if len(df_f_sal) > 0:
        st.metric(" Avg Salary", f"₹{df_f_sal['avgSalary'].mean()/100000:.1f} LPA")
    else:
        st.metric(" Avg Salary", "N/A")

if len(df_fresher) == 0:
    st.warning("No fresher jobs found with these filters. Try relaxing the filters!")
else:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        fresher_roles = df_fresher['title'].value_counts().head(10).reset_index()
        fresher_roles.columns = ['role', 'count']
        fig_fr = px.bar(fresher_roles, x='count', y='role', orientation='h',
                        title='Top 10 Roles Open for Freshers',
                        color='count', color_continuous_scale='Blues',
                        labels={'count': 'Openings', 'role': 'Job Role'})
        fig_fr.update_layout(yaxis={'categoryorder': 'total ascending'},
                             height=400, showlegend=False)
        st.plotly_chart(fig_fr, width='stretch')

    with col2:
        fresher_skills = []
        for skills in df_fresher['tagsAndSkills'].dropna():
            fresher_skills.extend([s.strip().lower() for s in skills.split(',')])
        fresher_skill_df = pd.DataFrame(Counter(fresher_skills).most_common(10),
                                        columns=['skill', 'count'])
        fig_fs = px.bar(fresher_skill_df, x='count', y='skill', orientation='h',
                        title='Top 10 Skills Freshers Need',
                        color='count', color_continuous_scale='Greens',
                        labels={'count': 'Frequency', 'skill': 'Skill'})
        fig_fs.update_layout(yaxis={'categoryorder': 'total ascending'},
                             height=400, showlegend=False)
        st.plotly_chart(fig_fs, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        fresher_companies = df_fresher['companyName'].value_counts().head(10).reset_index()
        fresher_companies.columns = ['company', 'count']
        fig_fc = px.bar(fresher_companies, x='count', y='company', orientation='h',
                        title='Top 10 Companies Hiring Freshers',
                        color='count', color_continuous_scale='Oranges',
                        labels={'count': 'Openings', 'company': 'Company'})
        fig_fc.update_layout(yaxis={'categoryorder': 'total ascending'},
                             height=400, showlegend=False)
        st.plotly_chart(fig_fc, width='stretch')

    with col2:
        df_fresher_sal = df_fresher[df_fresher['avgSalary'] >= 100000].copy()
        df_fresher_sal['avgSalary_LPA'] = df_fresher_sal['avgSalary'] / 100000
        if len(df_fresher_sal) > 0:
            fig_fsal = px.histogram(df_fresher_sal, x='avgSalary_LPA',
                                    title='Fresher Salary Distribution (LPA)',
                                    color_discrete_sequence=['#00CC96'],
                                    labels={'avgSalary_LPA': 'Salary (LPA)'},
                                    nbins=20)
            fig_fsal.update_layout(height=400)
            st.plotly_chart(fig_fsal, width='stretch')
        else:
            st.info("Not enough salary data for current filters")

    st.markdown("---")
    st.markdown("###  All Fresher Job Openings")
    sort_by = st.selectbox("Sort by",
                           ['Most Openings First', 'Highest Salary First',
                            'Best Company Rating First'],
                           key='fresher_sort')
    df_display = df_fresher.copy()
    if sort_by == 'Highest Salary First':
        df_display = df_display.sort_values('avgSalary', ascending=False)
    elif sort_by == 'Best Company Rating First':
        df_display = df_display.sort_values('AggregateRating', ascending=False)

    df_display_final = df_display[['title', 'companyName', 'city',
                                    'avgExperience', 'AggregateRating']].copy()
    df_display_final.columns = ['Job Title', 'Company', 'City',
                                 'Exp Required (Yrs)', 'Company Rating']
    df_display_final['Job Title']          = df_display_final['Job Title'].str.title()
    df_display_final['Company']            = df_display_final['Company'].str.title()
    df_display_final['Exp Required (Yrs)'] = df_display_final['Exp Required (Yrs)'].round(1)
    df_display_final['Company Rating']     = df_display_final['Company Rating'].round(1)
    st.dataframe(df_display_final.reset_index(drop=True), width='stretch',
                 column_config={
                     "Company Rating": st.column_config.ProgressColumn(
                         "Company Rating", min_value=0, max_value=5)
                 })

    st.markdown("---")
    top_fresher_role    = df_fresher['title'].value_counts().index[0].title()
    top_fresher_skill   = fresher_skill_df['skill'].iloc[0].title()
    top_fresher_company = fresher_companies['company'].iloc[0]
    st.success(f" **Fresher Insight:** Most openings are for **{top_fresher_role}** roles. "
               f"**{top_fresher_skill}** is the most required skill. "
               f"**{top_fresher_company}** is the top hiring company for freshers!")

st.markdown("---")

# ── JOB ROLE COMPARISON TOOL ──────────────────────────
st.subheader(" Job Role Comparison Tool")
st.markdown("*Compare two job roles side by side — salary, skills, cities and more*")

all_roles = sorted(df_tech['title'].value_counts().head(100).index.tolist())
col1, col2 = st.columns(2)
with col1:
    role1 = st.selectbox("Select Role 1", all_roles,
                          index=all_roles.index('data analyst')
                                if 'data analyst' in all_roles else 0,
                          key='role1')
with col2:
    role2 = st.selectbox("Select Role 2", all_roles,
                          index=all_roles.index('data engineer')
                                if 'data engineer' in all_roles else 1,
                          key='role2')

if role1 == role2:
    st.warning("Please select two different roles!")
else:
    df_role1     = df_tech[df_tech['title'].str.lower() == role1.lower()].copy()
    df_role2     = df_tech[df_tech['title'].str.lower() == role2.lower()].copy()
    df_role1_sal = df_role1[df_role1['avgSalary'] >= 100000].copy()
    df_role1_sal['avgSalary_LPA'] = df_role1_sal['avgSalary'] / 100000
    df_role2_sal = df_role2[df_role2['avgSalary'] >= 100000].copy()
    df_role2_sal['avgSalary_LPA'] = df_role2_sal['avgSalary'] / 100000

    avg1 = df_role1_sal['avgSalary_LPA'].mean() if len(df_role1_sal) > 0 else None
    avg2 = df_role2_sal['avgSalary_LPA'].mean() if len(df_role2_sal) > 0 else None

    st.markdown("---")
    st.markdown("###  Quick Comparison")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("**Metric**")
        for label in ["Total Openings", "Avg Salary", "Min Experience",
                      "Companies Hiring", "Top City"]:
            st.markdown(label)
    with col2:
        st.markdown(f"**{role1.title()}**")
        st.markdown(f" {len(df_role1):,}")
        st.markdown(f" ₹{avg1:.1f} LPA" if avg1 else " Not Disclosed")
        st.markdown(f" {df_role1['avgExperience'].min():.1f} yrs")
        st.markdown(f" {df_role1['companyName'].nunique():,}")
        st.markdown(f" {df_role1['city'].value_counts().index[0] if len(df_role1) > 0 else 'N/A'}")
    with col3:
        st.markdown("**vs**")
        for _ in range(5): st.markdown("vs")
    with col4:
        st.markdown(f"**{role2.title()}**")
        st.markdown(f" {len(df_role2):,}")
        st.markdown(f" ₹{avg2:.1f} LPA" if avg2 else " Not Disclosed")
        st.markdown(f" {df_role2['avgExperience'].min():.1f} yrs")
        st.markdown(f" {df_role2['companyName'].nunique():,}")
        st.markdown(f" {df_role2['city'].value_counts().index[0] if len(df_role2) > 0 else 'N/A'}")
    with col5:
        st.markdown("**Winner**")
        st.markdown(" " + (role1.title() if len(df_role1) > len(df_role2) else role2.title()))
        if avg1 and avg2:
            st.markdown(" " + (role1.title() if avg1 > avg2 else role2.title()))
        elif avg1:
            st.markdown(f" {role1.title()}")
        elif avg2:
            st.markdown(f" {role2.title()}")
        else:
            st.markdown(" No data")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        sal_compare = pd.DataFrame({
            'Role': [role1.title(), role2.title()],
            'Avg Salary (LPA)': [round(avg1, 2) if avg1 else 0,
                                  round(avg2, 2) if avg2 else 0]
        })
        fig_sal = px.bar(sal_compare, x='Role', y='Avg Salary (LPA)',
                         title='Average Salary Comparison',
                         color='Role',
                         color_discrete_sequence=['#636EFA', '#EF553B'],
                         text='Avg Salary (LPA)')
        fig_sal.update_traces(texttemplate='₹%{text:.1f} LPA', textposition='outside')
        fig_sal.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_sal, width='stretch')
    with col2:
        open_compare = pd.DataFrame({
            'Role': [role1.title(), role2.title()],
            'Job Openings': [len(df_role1), len(df_role2)]
        })
        fig_open = px.bar(open_compare, x='Role', y='Job Openings',
                          title='Total Job Openings', color='Role',
                          color_discrete_sequence=['#00CC96', '#FF6692'],
                          text='Job Openings')
        fig_open.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig_open.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_open, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        skills1 = []
        for skills in df_role1['tagsAndSkills'].dropna():
            skills1.extend([s.strip().lower() for s in skills.split(',')])
        skill1_df = pd.DataFrame(Counter(skills1).most_common(10),
                                  columns=['skill', 'count'])
        fig_sk1 = px.bar(skill1_df, x='count', y='skill', orientation='h',
                         title=f'Top Skills — {role1.title()}',
                         color='count', color_continuous_scale='Blues',
                         labels={'count': 'Frequency', 'skill': 'Skill'})
        fig_sk1.update_layout(yaxis={'categoryorder': 'total ascending'},
                              height=400, showlegend=False)
        st.plotly_chart(fig_sk1, width='stretch')
    with col2:
        skills2 = []
        for skills in df_role2['tagsAndSkills'].dropna():
            skills2.extend([s.strip().lower() for s in skills.split(',')])
        skill2_df = pd.DataFrame(Counter(skills2).most_common(10),
                                  columns=['skill', 'count'])
        fig_sk2 = px.bar(skill2_df, x='count', y='skill', orientation='h',
                         title=f'Top Skills — {role2.title()}',
                         color='count', color_continuous_scale='Reds',
                         labels={'count': 'Frequency', 'skill': 'Skill'})
        fig_sk2.update_layout(yaxis={'categoryorder': 'total ascending'},
                              height=400, showlegend=False)
        st.plotly_chart(fig_sk2, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        exp_compare = pd.DataFrame({
            'Experience': list(df_role1['avgExperience']) + list(df_role2['avgExperience']),
            'Role': [role1.title()] * len(df_role1) + [role2.title()] * len(df_role2)
        })
        fig_exp = px.box(exp_compare, x='Role', y='Experience',
                         title='Experience Distribution', color='Role',
                         color_discrete_sequence=['#636EFA', '#EF553B'])
        fig_exp.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_exp, width='stretch')
    with col2:
        city1_counts       = df_role1['city'].value_counts().head(5).reset_index()
        city1_counts.columns = ['city', 'count']
        city1_counts['role'] = role1.title()
        city2_counts       = df_role2['city'].value_counts().head(5).reset_index()
        city2_counts.columns = ['city', 'count']
        city2_counts['role'] = role2.title()
        city_combined = pd.concat([city1_counts, city2_counts])
        fig_city = px.bar(city_combined, x='city', y='count', color='role',
                          barmode='group', title='Top Cities — Side by Side',
                          color_discrete_sequence=['#636EFA', '#EF553B'],
                          labels={'count': 'Openings', 'city': 'City'})
        fig_city.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig_city, width='stretch')

    st.markdown("---")
    st.markdown("###  Skills Common to Both Roles")
    common_skills  = set(skill1_df['skill'].tolist()) & set(skill2_df['skill'].tolist())
    unique_skills1 = set(skill1_df['skill'].tolist()) - common_skills
    unique_skills2 = set(skill2_df['skill'].tolist()) - common_skills
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("** Common Skills**")
        for skill in sorted(common_skills): st.success(f" {skill.title()}")
    with col2:
        st.markdown(f"** Only in {role1.title()}**")
        for skill in sorted(unique_skills1): st.info(f"→ {skill.title()}")
    with col3:
        st.markdown(f"** Only in {role2.title()}**")
        for skill in sorted(unique_skills2): st.error(f"→ {skill.title()}")

    st.markdown("---")
    st.markdown("###  Which Role Should You Choose?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### Choose {role1.title()} if you want:")
        st.markdown(f"- More openings: **{len(df_role1):,}**" if len(df_role1) > len(df_role2)
                    else "- Easier entry — lower experience needed")
        st.markdown(f"- Higher salary: **₹{avg1:.1f} LPA**" if avg1 and avg2 and avg1 > avg2
                    else "- More companies to choose from")
        st.markdown(f"- Focus on: **{skill1_df['skill'].iloc[0].title() if len(skill1_df) > 0 else 'N/A'}**")
    with col2:
        st.markdown(f"#### Choose {role2.title()} if you want:")
        st.markdown(f"- More openings: **{len(df_role2):,}**" if len(df_role2) > len(df_role1)
                    else "- Easier entry — lower experience needed")
        st.markdown(f"- Higher salary: **₹{avg2:.1f} LPA**" if avg1 and avg2 and avg2 > avg1
                    else "- More companies to choose from")
        st.markdown(f"- Focus on: **{skill2_df['skill'].iloc[0].title() if len(skill2_df) > 0 else 'N/A'}**")

st.markdown("---")

# ── COMPANY DEEP DIVE ─────────────────────────────────
st.subheader(" Company Deep Dive")
st.markdown("*Select any company and get complete hiring intelligence*")

top_companies_list = df_tech['companyName'].value_counts().head(100).index.tolist()
selected_company   = st.selectbox(" Search and Select a Company",
                                   sorted(top_companies_list),
                                   key='company_deep_dive')

df_company     = df_tech[df_tech['companyName'] == selected_company].copy()
df_company_sal = df_company[df_company['avgSalary'] >= 100000].copy()
df_company_sal['avgSalary_LPA'] = df_company_sal['avgSalary'] / 100000

st.markdown("---")
col1, col2, col3, col4, col5 = st.columns(5)
avg_sal    = df_company_sal['avgSalary_LPA'].mean() if len(df_company_sal) > 0 else None
avg_rating = df_company['AggregateRating'].mean()
with col1: st.metric(" Total Openings",   f"{len(df_company):,}")
with col2: st.metric(" Cities Hiring In", f"{df_company['city'].nunique():,}")
with col3: st.metric(" Unique Roles",     f"{df_company['title'].nunique():,}")
with col4: st.metric(" Avg Salary",       f"₹{avg_sal:.1f} LPA" if avg_sal else "Not Disclosed")
with col5: st.metric("Company Rating",   f"{avg_rating:.1f}/5" if not pd.isna(avg_rating) else "No Rating")

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    company_roles = df_company['title'].value_counts().head(10).reset_index()
    company_roles.columns = ['role', 'count']
    fig_cr = px.bar(company_roles, x='count', y='role', orientation='h',
                    title=f'Top Roles at {selected_company}',
                    color='count', color_continuous_scale='Blues',
                    labels={'count': 'Openings', 'role': 'Role'})
    fig_cr.update_layout(yaxis={'categoryorder': 'total ascending'},
                         height=400, showlegend=False)
    st.plotly_chart(fig_cr, width='stretch')
with col2:
    company_skills = []
    for skills in df_company['tagsAndSkills'].dropna():
        company_skills.extend([s.strip().lower() for s in skills.split(',')])
    company_skill_df = pd.DataFrame(Counter(company_skills).most_common(10),
                                    columns=['skill', 'count'])
    fig_csk = px.bar(company_skill_df, x='count', y='skill', orientation='h',
                     title=f'Top Skills {selected_company} Looks For',
                     color='count', color_continuous_scale='Greens',
                     labels={'count': 'Frequency', 'skill': 'Skill'})
    fig_csk.update_layout(yaxis={'categoryorder': 'total ascending'},
                          height=400, showlegend=False)
    st.plotly_chart(fig_csk, width='stretch')

col1, col2 = st.columns(2)
with col1:
    df_company_city = df_company[~df_company['city'].str.contains(
        '|'.join(invalid_cities), case=False, na=False)]
    company_cities  = df_company_city['city'].value_counts().head(10).reset_index()
    company_cities.columns = ['city', 'count']
    fig_cc = px.bar(company_cities, x='count', y='city', orientation='h',
                    title=f'Cities Where {selected_company} is Hiring',
                    color='count', color_continuous_scale='Oranges',
                    labels={'count': 'Openings', 'city': 'City'})
    fig_cc.update_layout(yaxis={'categoryorder': 'total ascending'},
                         height=400, showlegend=False)
    st.plotly_chart(fig_cc, width='stretch')
with col2:
    exp_dist = df_company['expCategory'].value_counts().reset_index()
    exp_dist.columns = ['expCategory', 'count']
    fig_ce = px.pie(exp_dist, values='count', names='expCategory',
                    title=f'Experience Level Distribution at {selected_company}',
                    color_discrete_sequence=px.colors.sequential.RdBu)
    fig_ce.update_traces(textposition='inside', textinfo='percent+label')
    fig_ce.update_layout(height=400)
    st.plotly_chart(fig_ce, width='stretch')

if len(df_company_sal) > 0:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        fig_csal = px.histogram(df_company_sal, x='avgSalary_LPA',
                                title=f'Salary Distribution at {selected_company}',
                                color_discrete_sequence=['#636EFA'],
                                labels={'avgSalary_LPA': 'Salary (LPA)'},
                                nbins=15)
        fig_csal.update_layout(height=350)
        st.plotly_chart(fig_csal, width='stretch')
    with col2:
        sal_by_exp = df_company_sal.groupby('expCategory')['avgSalary_LPA'].mean().reset_index()
        sal_by_exp = sal_by_exp.sort_values('avgSalary_LPA', ascending=False)
        fig_cse = px.bar(sal_by_exp, x='expCategory', y='avgSalary_LPA',
                         title=f'Avg Salary by Experience at {selected_company}',
                         color='avgSalary_LPA', color_continuous_scale='Viridis',
                         labels={'avgSalary_LPA': 'Avg Salary (LPA)',
                                 'expCategory': 'Experience Level'})
        fig_cse.update_layout(xaxis_tickangle=-15, height=350, showlegend=False)
        st.plotly_chart(fig_cse, width='stretch')

st.markdown("---")
st.markdown("###  Company Summary")
top_role      = company_roles['role'].iloc[0].title()     if len(company_roles) > 0     else 'N/A'
top_skill     = company_skill_df['skill'].iloc[0].title() if len(company_skill_df) > 0  else 'N/A'
top_city      = company_cities['city'].iloc[0]            if len(company_cities) > 0    else 'N/A'
fresher_pct   = len(df_company[df_company['avgExperience'] <= 2]) / len(df_company) * 100

col1, col2 = st.columns(2)
with col1:
    st.info(f" **{selected_company}** has **{len(df_company):,}** active job openings")
    st.info(f" Most hired role: **{top_role}**")
    st.info(f" Most required skill: **{top_skill}**")
with col2:
    st.info(f" Primary hiring city: **{top_city}**")
    st.info(f" Fresher friendly: **{fresher_pct:.0f}%** of jobs need 0-2 yrs exp")
    if avg_sal:
        st.info(f" Average salary offered: **₹{avg_sal:.1f} LPA**")
    if not pd.isna(avg_rating):
        if avg_rating >= 4:
            st.success(f"Great place to work! Rating: **{avg_rating:.1f}/5**")
        elif avg_rating >= 3:
            st.warning(f"Average workplace. Rating: **{avg_rating:.1f}/5**")
        else:
            st.error(f"Below average rating: **{avg_rating:.1f}/5**")

st.markdown("---")
st.markdown(f"###  How to Get Hired at {selected_company}")
st.markdown("*Based on actual job posting data*")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Must Have Skills:**")
    for i, skill in enumerate(company_skill_df['skill'].head(5).tolist(), 1):
        st.success(f"{i}. {skill.title()}")
with col2:
    st.markdown("**Best Roles to Target:**")
    for i, role in enumerate(company_roles['role'].head(5).tolist(), 1):
        st.info(f"{i}. {role.title()}")

# ── FOOTER ────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with  using Python, Pandas & Streamlit | Data Source: Kaggle")

