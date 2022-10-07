import streamlit as st
import warnings 
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime as dt
df1 = pd.read_excel("ADSL.xlsx")
df2 = pd.read_excel("ADVS.xlsx")
df3 = pd.read_excel("ADAE.xlsx")
adv_df = pd.DataFrame(df1[['DCDECOD','ARM','AGEGR1','SEX']].value_counts().index.tolist())
adv_df.columns = ['DCDECOD','ARM','AGEGR1','SEX']
adv_df['COUNT'] = df1[['DCDECOD','ARM','AGEGR1','SEX']].value_counts().values
df3_new = df3[df3['TRTEMFL']=='Y']
n = 24
top_24 = df3_new['AEDECOD'].value_counts().index.tolist()[:n]
df3_subset = df3_new[df3_new['AEDECOD'].isin(top_24)]
df1['Expo_Year'] = (df1['TRTEDT'] - df1['TRTSDT'] + dt.timedelta(days=1)).dt.days/365.25
ev_rt_A = df1[df1['ARM']=='ARM A']
ev_rt_B = df1[df1['ARM']=='ARM B']
ev_rt_C = df1[df1['ARM']=='ARM C']
EY_A = sum(ev_rt_A['Expo_Year'])
EY_B = sum(ev_rt_B['Expo_Year'])
EY_C = sum(ev_rt_C['Expo_Year'])
adv_eve = df3_new[['TRTA','AEDECOD']].value_counts()
adv_eve = adv_eve.reset_index()
adv_eve.rename({0:'Frequency'},axis=1,inplace=True)
trt=adv_eve['TRTA']
trt01=[EY_A if i=='ARM A' else EY_B if i=='ARM B' else EY_C for i in trt]
adv_eve['expo_year']=trt01
adv_eve['event_rate'] = (adv_eve['Frequency']/adv_eve['expo_year'])*100
adv_eve = adv_eve.sort_values(['TRTA','AEDECOD'])
adv_eve = adv_eve.reset_index(drop=True)
adv_eve = adv_eve[adv_eve['AEDECOD'].isin(top_24)]
heat_data = adv_eve.pivot("AEDECOD", "TRTA", "event_rate")
st.header("Overview of Adverse Events")
chart_selector = st.sidebar.selectbox("Select the type of chart", ['Treemap - Participation Overview','Stacked Bar - Treatment Emergent Adverse Events','Heat Map - Event Rate'])
if chart_selector=="Treemap - Participation Overview":
  st.write("### Standardized Disposition Term")
  figu = px.treemap(adv_df, path=[px.Constant('main'),'DCDECOD','ARM','AGEGR1','SEX'], values='COUNT', color='COUNT', color_continuous_scale='twilight_r')
  figu.update_layout(margin = dict(t=50, l=25, r=25, b=25))
  st.plotly_chart(figu,use_container_width = True)
if chart_selector=="Stacked Bar - Treatment Emergent Adverse Events":
  st.write("### Top 24 Treatment Emergent Adverse Events")
  fig2 = px.histogram(df3_subset, x="TRTA", color="AEDECOD",color_discrete_sequence=px.colors.qualitative.Light24)
  fig2.update_layout(
      legend_title="Adverse Events",
      xaxis_title="Treatment",
      yaxis_title="Count")
  st.plotly_chart(fig2,use_container_width = True)
if chart_selector=="Heat Map - Event Rate":
  st.write("### Top 24 Treatment Emergent Adverse Event Rates")
  fig = plt.figure(figsize=(15,12))  
  #sns.set(rc = {'figure.figsize':(15,12)})
  sns.heatmap(heat_data, annot=True, cmap='rocket_r',fmt='.2f')
  plt.xlabel("Treatment")
  plt.ylabel("Adverse Event")
  #p.set(xlabel="Treatment",ylabel="Adverse Event",title="Top 25 Treatment Emergent Adverse Event Rates")
  st.pyplot(fig,use_container_width = True)
