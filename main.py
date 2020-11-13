from flask import Flask, render_template
import plotly
import plotly.express as px
import plotly.graph_objs as go
import json
import math
import numpy as np
import pandas as pd
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials, firestore
import plotly.figure_factory as ff
app = Flask(__name__)

cred = credentials.Certificate('admin.json')
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': 'https://datavisual-94374.firebaseio.com'
                              }
                              )
db = firestore.client()
col_ref = db.collection('Data')
# db = firestore.client()
# coll = db.collection('Data')
# for i in coll.get():
#     if i['IndicatorName'] == 'Primary income payments (BoP, current US$)':
#          primary_income_payments = i['Year_Value']
# for item in primary_income_payments:
#     print(item)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/matplotlib')
def simplechart():
    return render_template('simplechart.html')


@app.route('/plotly')
def plotlyy():
    return render_template('plotly.html')


@app.route('/scatter')
def scatter():
    return render_template('scatter.html')


@app.route('/line')
def line():
    return render_template('line.html')


@app.route('/pie')
def pie():
    return render_template('pie.html')


@app.route('/boxplot')
def boxplot():
    return render_template('boxplot.html')


@app.route('/histogram')
def histogram():
    return render_template('histogram.html')


@app.route('/bar')
def bar():
    return render_template('bar.html')


@app.route('/page1')
def page1():
    # bar = char1()
    bar, fig1, fig2, fig3, ddf, fig4, histo = tansuat_tso_tstl_page1()
    return render_template('page1.html', plot=bar, data1=fig1, data2=fig2, data3=fig3, bangSoLieu=[ddf.to_html(classes='data', header="true")], box=fig4,  hist=histo)


@app.route('/page2')
def page2():
    gfig, gtanso1, gtansuat1, gtstl1, gtanso2, gtansuat2, gtstl2, gbox, ghist, gbang1, gbang2 = tansuat_tso_tstl_page2()
    return render_template('page2.html', plot=gfig, tanso1=gtanso1, tansuat1=gtansuat1, tstl1=gtstl1, bang1=[gbang1.to_html(classes='data', header="true")], tanso2=gtanso2, tansuat2=gtansuat2, tstl2=gtstl2, bang2=[gbang2.to_html(classes='data', header="true")], box=gbox, hist=ghist)


def getYear_Value(s):
    rs = col_ref.where('IndicatorName', '==', s).get()
    for item in rs:
        primary_income_payments = item.to_dict()["Year_Value"]
        # print(lst)
    year, value = [i['Year']for i in primary_income_payments], [
        float(i['Value'])for i in primary_income_payments]
    return year, value

# -------------PAGE1--------------------


def tansuat_tso_tstl_page1():
    year, value = getYear_Value('Primary income payments (BoP, current US$)')
    k = round((2*len(value))**(1/3))
    h = math.ceil((int(max(value))-int(min(value)))/k)
    # print(k)
    # print(h)

    k1 = min(value)+h
    k2 = min(value)+2*h
    k3 = min(value)+3*h

    khoang1, khoang2, khoang3, khoang4 = [], [], [], []
    for i in value:
        if i < min(value)+h-1:
            khoang1.append(i)
        elif i >= min(value)+h and i < min(value)+2*h-1:
            khoang2.append(i)
        elif i >= min(value)+2*h and i < min(value)+3*h-1:
            khoang3.append(i)
        elif i >= min(value)+3*h:
            khoang4.append(i)
    # Khoảng
    khoang_usd = ['< '+str(k1-1), str(k1) + " - " + str(k2-1),
                  str(k2) + " - " + str(k3-1), ">= "+str(k3)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=year, y=value, text=value,
                         textposition='outside', marker=dict(color='#75d397')))
    fig.update_layout(title='',
                      xaxis_title='Năm',
                      yaxis_title='USD',
                      )
    # Tần số
    tanso = [len(khoang1), len(khoang2), len(khoang3), len(khoang4)]
    # Tần xuất
    tanXuat = [round((i*100)/(sum(tanso)), 2) for i in tanso]
    # Tần xuất tích lũy
    tanXuatTL = []
    s = 0
    for i in tanXuat:
        s += i
        tanXuatTL.append(s)
    stt = [i for i in range(1, k+1)]
    ddf = {'Chia khoảng': pd.Series(khoang_usd, index=stt),
           'Tần số': pd.Series(tanso, index=stt, dtype='int'),
           'Tần xuất': pd.Series(tanXuat, index=stt, dtype='float'),
           'Tần xuất tích lũy': pd.Series(tanXuatTL, index=stt, dtype='float')}
    ddf = pd.DataFrame(ddf)

    ddf = {'Chia khoảng': pd.Series(khoang_usd, index=stt),
           'Tần số': pd.Series(tanso, index=stt, dtype='int'),
           'Tần xuất': pd.Series(tanXuat, index=stt, dtype='float'),
           'Tần xuất tích lũy': pd.Series(tanXuatTL, index=stt, dtype='float')}
    ddf = pd.DataFrame(ddf)

    figTanSo = go.Figure()
    figTanSo.add_trace(go.Bar(x=khoang_usd, y=tanso, text=tanso,
                              textposition='inside', marker=dict(color='#0099ff')))
    figTanSo.update_layout(
        xaxis_title='USD',
        yaxis_title='Tần số')
    figTanSuat = go.Figure()
    figTanSuat.add_trace(go.Pie(labels=khoang_usd, values=tanXuat))
    figTanSuat.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=0.75
    ))
    figTSTL = go.Figure()
    figTSTL.add_trace(go.Scatter(x=khoang_usd, y=tanXuatTL))
    figTSTL.update_layout(
        xaxis_title='USD',
        yaxis_title='Tần xuất tích lũy')
    # box
    stt = [i for i in range(1, len(year)+1)]
    df1 = {'STT': pd.Series(stt, index=stt),
           'Year': pd.Series(year, index=stt),
           'USD': pd.Series(value, index=stt, dtype='float')}
    df1 = pd.DataFrame(df1)
    figBox = px.box(df1, y='USD', points="all")
    figBox.update_yaxes(range=[500000000, 17500000000])
    # moTaBox = [int(i) for i in np.array(df1['USD'].describe())]
    # motaBox1 = df1['USD'].describe()

    # motaBox1 = {'25%': pd.Series(motaBox1['25%'], index=[1], dtype='long'),
    #             '50%': pd.Series(motaBox1['50%'], index=[1], dtype='long'),
    #             '75%': pd.Series(motaBox1['75%'], index=[1], dtype='long'),
    #             'Min': pd.Series(motaBox1['min'], index=[1], dtype='long'),
    #             'Max': pd.Series(motaBox1['max'], index=[1], dtype='long'),
    #             'Mean': pd.Series(motaBox1['mean'], index=[1], dtype='long'),
    #             'Std': pd.Series(motaBox1['std'], index=[1], dtype='long')}

    # motaBox1 = pd.DataFrame(motaBox1)
    # histogram
    # hist_data = [df1['USD'].values]
    # group_labels = ['USD']
    # hist = ff.create_distplot(hist_data, group_labels, bin_size=5*10**9)
    hist = px.histogram(df1, x="USD")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(figTanSo, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(figTanSuat, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(figTSTL, cls=plotly.utils.PlotlyJSONEncoder)
    graphBox = json.dumps(figBox, cls=plotly.utils.PlotlyJSONEncoder)
    histo = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, graphJSON1, graphJSON2, graphJSON3, ddf, graphBox, histo

# -----------------PAGE222222-----------------------------


def tansuat_tso_tstl_page2():
    GDP_GS_year, GDP_GS_value = getYear_Value(
        'Exports of goods and services (% of GDP)')
    Growth_GS_year, Growth_GS_value = getYear_Value(
        'Exports of goods and services (annual % growth)')
    # Chia khoảng % GDP
    k_gdp = round((2*len(GDP_GS_value))**(1/3))
    h_gdp = math.ceil((int(max(GDP_GS_value))-int(min(GDP_GS_value)))/k_gdp)

    k1_gdp = min(GDP_GS_value)+h_gdp
    k2_gdp = min(GDP_GS_value)+2*h_gdp
    k3_gdp = min(GDP_GS_value)+3*h_gdp

    khoang1_gdp, khoang2_gdp, khoang3_gdp, khoang4_gdp = [], [], [], []
    for i in GDP_GS_value:
        if i < k1_gdp-0.01:
            khoang1_gdp.append(i)
        elif i >= k1_gdp and i < k2_gdp-0.01:
            khoang2_gdp.append(i)
        elif i >= k2_gdp and i < k3_gdp-0.01:
            khoang3_gdp.append(i)
        elif i >= k3_gdp:
            khoang4_gdp.append(i)

    # Khoảng
    khoang_gdp = ['< '+str(k1_gdp-0.01), str(k1_gdp) + " - " + str(k2_gdp-0.01),
                  str(k2_gdp) + " - " + str(k3_gdp-0.01), '>= ' + str(k3_gdp)]
    # Tần số
    tanso_gdp = [len(khoang1_gdp), len(khoang2_gdp),
                 len(khoang3_gdp), len(khoang4_gdp)]
    # Tần xuất
    tanXuat_gdp = [round((i*100)/sum(tanso_gdp), 2)for i in tanso_gdp]
    # Tần xuất tích lũy
    tanXuatTL_gdp = []
    s_gdp = 0
    for i in tanXuat_gdp:
        s_gdp = round(s_gdp + i, 2)
        tanXuatTL_gdp.append(s_gdp)
    # Chia khoảng % Tăng trưởng

    k_growth = round((2*len(Growth_GS_value))**(1/3))
    h_growth = math.ceil(
        (int(max(Growth_GS_value))-int(min(Growth_GS_value)))/k_growth)
    k1_growth = min(Growth_GS_value)+h_growth
    k2_growth = min(Growth_GS_value)+2*h_growth
    k3_growth = min(Growth_GS_value)+3*h_growth

    khoang1_growth, khoang2_growth, khoang3_growth, khoang4_growth = [], [], [], []
    for i in Growth_GS_value:
        if i < k1_growth-0.01:
            khoang1_growth.append(i)
        elif i >= k1_growth and i < k2_growth-0.01:
            khoang2_growth.append(i)
        elif i >= k2_growth and i < k3_growth-0.01:
            khoang3_growth.append(i)
        elif i >= k3_growth:
            khoang4_growth.append(i)
    # Khoảng
    khoang_growth = ['< '+str(round(k1_growth-0.01, 2)), str(round(k1_growth, 2)) + " - " + str(round(
        k2_growth-0.01, 2)), str(round(k2_growth, 2)) + " - " + str(round(k3_growth-0.01, 2)), '>= ' + str(k3_growth)]
    # Tần số
    tanso_growth = [len(khoang1_growth), len(khoang2_growth),
                    len(khoang3_growth), len(khoang4_growth)]
    # Tần xuất
    tanXuat_growth = [round((i*100)/sum(tanso_growth), 2)for i in tanso_growth]
    # Tần xuất tích lũy
    tanXuatTL_growth = []
    s_growth = 0
    for i in tanXuat_growth:
        s_growth = round(s_growth + i, 2)
        tanXuatTL_growth.append(s_growth)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Growth_GS_year, y=Growth_GS_value, mode='lines+markers',
                             name='% Tăng trưởng hàng năm', marker=dict(color='#fc6d00')))
    fig.add_trace(go.Bar(x=GDP_GS_year, y=GDP_GS_value, text=GDP_GS_value,
                         textposition='inside', marker=dict(color='#0099ff'), name='%GDP'))
    fig.update_layout(
        xaxis_title='Năm',
        yaxis_title='Phần trăm')
    figTanSo1 = go.Figure()
    figTanSo1.add_trace(go.Bar(x=khoang_gdp, y=tanso_gdp, text=tanso_gdp,
                               textposition='inside', marker=dict(color='#0099ff')))
    figTanSo1.update_layout(
        xaxis_title='Phần trăm',
        yaxis_title='Tần số')

    figTanSuat1 = go.Figure()
    figTanSuat1.add_trace(go.Pie(labels=khoang_gdp, values=tanXuat_gdp))
    figTanSuat1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=0.75
    ))

    figTSTL1 = go.Figure()
    figTSTL1.add_trace(go.Scatter(x=khoang_gdp, y=tanXuatTL_gdp))
    figTSTL1.update_layout(
        xaxis_title='USD',
        yaxis_title='Tần xuất tích lũy')

    figTanSo2 = go.Figure()
    figTanSo2.add_trace(go.Bar(x=khoang_growth, y=tanso_growth, text=tanso_growth,
                               textposition='inside', marker=dict(color='#0099ff')))
    figTanSo2.update_layout(
        xaxis_title='Phần trăm',
        yaxis_title='Tần số')

    figTanSuat2 = go.Figure()
    figTanSuat2.add_trace(go.Pie(labels=khoang_gdp, values=tanXuat_gdp))
    figTanSuat2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=0.75
    ))
    figTSTL2 = go.Figure()
    figTSTL2.add_trace(go.Scatter(x=khoang_gdp, y=tanXuatTL_gdp))
    figTSTL2.update_layout(
        xaxis_title='USD',
        yaxis_title='Tần xuất tích lũy')

    stt = [j for j in range(1, k_gdp+1)]
    ddf_gdp = {'Chia khoảng': pd.Series(khoang_gdp, index=stt),
               'Tần số': pd.Series(tanso_gdp, index=stt, dtype='int'),
               'Tần xuất': pd.Series(tanXuat_gdp, index=stt, dtype='float'),
               'Tần xuất tích lũy': pd.Series(tanXuatTL_gdp, index=stt, dtype='float')}
    ddf_gdp = pd.DataFrame(ddf_gdp)

    ddf_growth = {'Chia khoảng': pd.Series(khoang_growth, index=stt),
                  'Tần số': pd.Series(tanso_growth, index=stt, dtype='int'),
                  'Tần xuất': pd.Series(tanXuat_growth, index=stt, dtype='float'),
                  'Tần xuất tích lũy': pd.Series(tanXuatTL_growth, index=stt, dtype='float')}
    ddf_growth = pd.DataFrame(ddf_growth)

    stt1 = [i for i in range(1, len(GDP_GS_year)+1)]
    df3 = {'STT': pd.Series(stt1, index=stt1),
           'Year': pd.Series(GDP_GS_year, index=stt1),
           '%GDP': pd.Series(GDP_GS_value, index=stt1, dtype='float'),
           '%Tăng trưởng': pd.Series(Growth_GS_value, index=[i for i in range(1, len(Growth_GS_year)+1)], dtype='float')}
    df3 = pd.DataFrame(df3)

    figBox = go.Figure()
    figBox.add_trace(go.Box(y=df3['%GDP'].values,
                            name='%GDP', boxpoints='all'))
    figBox.add_trace(
        go.Box(y=df3['%Tăng trưởng'].values, name='%Tăng trưởng', boxpoints='all'))

    hist = go.Figure()
    hist.add_trace(go.Histogram(x=df3['%GDP'].values, name='%GDP'))
    hist.add_trace(go.Histogram(
        x=df3['%Tăng trưởng'].values, name='%Tăng trưởng'))

    hist.update_layout(barmode='overlay')
    hist.update_traces(opacity=0.7)

    gfig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    gtanso1 = json.dumps(figTanSo1, cls=plotly.utils.PlotlyJSONEncoder)
    gtansuat1 = json.dumps(figTanSuat1, cls=plotly.utils.PlotlyJSONEncoder)
    gtstl1 = json.dumps(figTSTL1, cls=plotly.utils.PlotlyJSONEncoder)
    gtanso2 = json.dumps(figTanSo2, cls=plotly.utils.PlotlyJSONEncoder)
    gtansuat2 = json.dumps(figTanSuat2, cls=plotly.utils.PlotlyJSONEncoder)
    gtstl2 = json.dumps(figTSTL2, cls=plotly.utils.PlotlyJSONEncoder)
    gbox = json.dumps(figBox, cls=plotly.utils.PlotlyJSONEncoder)

    ghist = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    # bang1 = json.dumps(ddf_gdp, cls=plotly.utils.PlotlyJSONEncoder)
    # bang2 = json.dumps(ddf_growth, cls=plotly.utils.PlotlyJSONEncoder)

    return gfig, gtanso1, gtansuat1, gtstl1, gtanso2, gtansuat2, gtstl2, gbox, ghist, ddf_gdp, ddf_growth


# def char1():
#     year, value = getYear_Value('Primary income payments (BoP, current US$)')
#     fig = go.Figure()
#     fig.add_trace(go.Bar(x=year, y=value, text=value,
#                          textposition='outside', marker=dict(color='#75d397')))
#     fig.update_layout(title='',
#                       xaxis_title='Năm',
#                       yaxis_title='USD',
#                       )
#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJSON
