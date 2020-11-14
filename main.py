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


@app.route('/page3')
def page3():
    gfig, gtanso1, gtansuat1, gtstl1, gtanso2, gtansuat2, gtstl2, gbox1, gbox2, ghist1, ghist2, ddf_gdp, ddf_growth = tansuat_tso_tstl_page3()
    return render_template('page3.html', plot=gfig, tanso1=gtanso1, tansuat1=gtansuat1, tstl1=gtstl1, bang1=[ddf_gdp.to_html(classes='data', header="true")], tanso2=gtanso2, tansuat2=gtansuat2, tstl2=gtstl2, bang2=[ddf_growth.to_html(classes='data', header="true")], box1=gbox1, hist1=ghist1, box2=gbox2, hist2=ghist2,)


@app.route('/page4')
def page4():
    # bar = char1()
    bar, fig1, fig2, fig3, ddf, fig4, histo = tansuat_tso_tstl_page4()
    return render_template('page4.html', plot=bar, tanso=fig1, tansuat=fig2, tstl=fig3, box=fig4,  hist=histo, bang=[ddf.to_html(classes='data', header="true")])


@app.route('/page5')
def page5():
    # bar = char1()
    bar, fig1, fig2, fig3, ddf, fig4, histo = tansuat_tso_tstl_page5()
    return render_template('page5.html', plot=bar, tanso=fig1, tansuat=fig2, tstl=fig3, box=fig4,  hist=histo, bang=[ddf.to_html(classes='data', header="true")])


@app.route('/page6')
def page6():
    # bar = char1()
    bar, fig1, fig2, fig3, ddf, fig4, histo = tansuat_tso_tstl_page5()
    return render_template('page6.html', plot=bar, tanso=fig1, tansuat=fig2, tstl=fig3, box=fig4,  hist=histo, bang=[ddf.to_html(classes='data', header="true")])


@app.route('/page7')
def page7():
    # bar = char1()
    bar, fig1, fig2, fig3, ddf, fig4, histo = tansuat_tso_tstl_page7()
    return render_template('page7.html', plot=bar, tanso=fig1, tansuat=fig2, tstl=fig3, box=fig4,  hist=histo, bang=[ddf.to_html(classes='data', header="true")])


def getYear_Value(s):
    rs = col_ref.where('IndicatorName', '==', s).get()
    for item in rs:
        primary_income_payments = item.to_dict()["Year_Value"]
        # print(lst)
    year, value = [i['Year']for i in primary_income_payments], [
        float(i['Value'])for i in primary_income_payments]
    return year, value
# ---PAGE7---


def tansuat_tso_tstl_page7():
    year_Goods, value_Goods = getYear_Value(
        'Net trade in goods (BoP, current US$)')

    fig = px.line(x=year_Goods, y=value_Goods,
                  labels=dict(x="Năm", y="Thu nhập", color="Time Period"), height=800)
    fig.add_trace(go.Bar(x=year_Goods, y=value_Goods, text=value_Goods, textposition='outside',
                         marker=dict(color='#C39BD3'), name='Thu nhập buôn bán hàng hóa'))
    fig.update_layout(
        xaxis_title='Năm',
        yaxis_title='Thu Nhập ($US)')

    k_Goods = round((2*len(value_Goods))**(1/3))
    h_Goods = math.ceil(
        (float(max(value_Goods))-float(min(value_Goods)))/k_Goods)

    k1_Goods = min(value_Goods)+h_Goods
    k2_Goods = min(value_Goods)+2*h_Goods
    k3_Goods = min(value_Goods)+3*h_Goods

    khoang1_Goods, khoang2_Goods, khoang3_Goods, khoang4_Goods = [], [], [], []
    for i in value_Goods:
        if i < min(value_Goods)+h_Goods-1:
            khoang1_Goods.append(i)
        elif i >= min(value_Goods)+h_Goods and i < min(value_Goods)+2*h_Goods-1:
            khoang2_Goods.append(i)
        elif i >= min(value_Goods)+2*h_Goods and i < min(value_Goods)+3*h_Goods-1:
            khoang3_Goods.append(i)
        elif i >= min(value_Goods)+3*h_Goods:
            khoang4_Goods.append(i)

    khoang_Goods = ['< ' + str(k1_Goods-1), str(k1_Goods) + " - " + str(
        k2_Goods-1), str(k2_Goods) + " - " + str(k3_Goods-1), '>= '+str(k3_Goods)]

    tanso_Goods = [len(khoang1_Goods), len(khoang2_Goods),
                   len(khoang3_Goods), len(khoang4_Goods)]

    tanXuat_Goods = [round((i*100)/(sum(tanso_Goods)), 2) for i in tanso_Goods]

    tanXuatTL_Goods = []
    s_Goods = 0
    for i in tanXuat_Goods:
        s_Goods += i
        tanXuatTL_Goods.append(s_Goods)

    # Đưa dữ liệu vào pandas
    stt = [i for i in range(1, len(khoang_Goods)+1)]
    ddf_Goods = {'Khoảng (USD)': pd.Series(khoang_Goods, index=stt),
                 'Tần số': pd.Series(tanso_Goods, index=stt, dtype='int'),
                 'Tần xuất': pd.Series(tanXuat_Goods, index=stt, dtype='float'),
                 'Tần xuất tích lũy': pd.Series(tanXuatTL_Goods, index=stt, dtype='float')}
    ddf_Goods = pd.DataFrame(ddf_Goods)
    figTanSo = go.Figure()
    figTanSo.add_trace(go.Bar(x=khoang_Goods, y=tanso_Goods, text=tanso_Goods,
                              textposition='inside', marker=dict(color='#C39BD3')))
    figTanSo.update_layout(
        xaxis_title='US ($)',
        yaxis_title='Tần số')
    figTanSo.update_yaxes(range=[0, 15])

    figTanSuat = go.Figure()
    figTanSuat.add_trace(
        go.Pie(labels=khoang_Goods, values=tanXuat_Goods))
    figTanSuat.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=- 1,
        xanchor="right",
        x=0.75
    ))

    figTstl = go.Figure()
    figTstl.add_trace(go.Scatter(
        x=khoang_Goods, y=tanXuatTL_Goods, marker=dict(color='#FF3366')))
    figTstl.update_layout(
        xaxis_title='US ($)',
        yaxis_title='Tần suất tích lũy')
    stt = [i for i in range(1, len(year_Goods)+1)]
    df_Goods = {'STT': pd.Series(stt, index=stt),
                'Year': pd.Series(year_Goods, index=stt),
                'Thu nhập trong mạng lưới buôn bán hàng hóa qua các năm (US$)': pd.Series(value_Goods, index=stt, dtype='double')}
    df_Goods = pd.DataFrame(df_Goods)
    figBox = go.Figure()
    figBox.add_trace(go.Box(y=df_Goods['Thu nhập trong mạng lưới buôn bán hàng hóa qua các năm (US$)'].values,
                            name='Thu nhập trong mạng lưới buôn bán hàng hóa qua các năm (US$)', boxpoints='all'))

    hist = go.Figure()
    hist.add_trace(go.Histogram(
        x=df_Goods['Thu nhập trong mạng lưới buôn bán hàng hóa qua các năm (US$)'].values, name='Thu nhập trong mạng lưới buôn bán hàng hóa qua các năm (US$)''giá trị gia tăng trong sản xuất(%)'))
    hist.update_layout(barmode='overlay')
    hist.update_traces(opacity=0.7)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(figTanSo, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(figTanSuat, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(figTstl, cls=plotly.utils.PlotlyJSONEncoder)
    graphBox = json.dumps(figBox, cls=plotly.utils.PlotlyJSONEncoder)
    histo = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, graphJSON1, graphJSON2, graphJSON3, ddf_Goods, graphBox, histo
# -----PGAE6------


def tansuat_tso_tstl_page6():
    year_Clothing, value_Clothing = getYear_Value(
        'Textiles and clothing (% of value added in manufacturing)')
    stt = [i for i in range(1, len(year_Clothing)+1)]
    df_Clothing = {'STT': pd.Series(stt, index=stt),
                   'Year': pd.Series(year_Clothing, index=stt),
                   'giá trị gia tăng trong sản xuất(%)': pd.Series(value_Clothing, index=stt, dtype='float')}
    k_Clothing = round((2*len(value_Clothing))**(1/3))
    h_Clothing = math.ceil(
        (float(max(value_Clothing))-float(min(value_Clothing)))/k_Clothing)

    k1_Clothing = round(min(value_Clothing)+h_Clothing, 2)
    k2_Clothing = round(min(value_Clothing)+2*h_Clothing, 2)

    khoang1_Clothing, khoang2_Clothing, khoang3_Clothing, khoang4_Clothing = [], [], [], []
    for i in value_Clothing:
        if i < min(value_Clothing)+h_Clothing-0.01:
            khoang1_Clothing.append(i)
        elif i >= min(value_Clothing)+h_Clothing and i < min(value_Clothing)+2*h_Clothing-0.01:
            khoang2_Clothing.append(i)
        elif i >= min(value_Clothing)+2*h_Clothing:
            khoang3_Clothing.append(i)

    khoang_Clothing = ['< '+str(k1_Clothing-0.01), str(k1_Clothing) +
                       " -" + str(round(k2_Clothing-0.01, 2)), '>=' + str(k2_Clothing)]

    tanso_Clothing = [len(khoang1_Clothing), len(
        khoang2_Clothing), len(khoang3_Clothing)]

    tanXuat_Clothing = [round((i*100)/(sum(tanso_Clothing)), 2)
                        for i in tanso_Clothing]

    tanXuatTL_Clothing = []
    s_Clothing = 0
    for i in tanXuat_Clothing:
        s_Clothing += i
        tanXuatTL_Clothing.append(s_Clothing)

    # Đưa dữ liệu vào pandas
    stt = [j for j in range(1, len(khoang_Clothing)+1)]
    ddf_Clothing = {'Khoảng (Giá trị gia tăng %)': pd.Series(khoang_Clothing, index=stt),
                    'Tần số': pd.Series(tanso_Clothing, index=stt, dtype='int'),
                    'Tần xuất': pd.Series(tanXuat_Clothing, index=stt, dtype='float'),
                    'Tần xuất tích lũy': pd.Series(tanXuatTL_Clothing, index=stt, dtype='float')}
    ddf_Clothing = pd.DataFrame(ddf_Clothing)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=year_Clothing, y=value_Clothing, text=value_Clothing,
                         textposition='inside', marker=dict(color='#E67E22')))
    fig.update_layout(
        xaxis_title='Năm',
        yaxis_title='giá trị gia tăng trong sản xuất (%)')
    fig.update_yaxes(range=[0, 30])
    figTanSo = go.Figure()
    figTanSo.add_trace(go.Bar(x=khoang_Clothing, y=tanso_Clothing, text=tanso_Clothing,
                              textposition='inside', marker=dict(color='#FF3366')))
    figTanSo.update_layout(title='Biểu đồ tần số sự tăng trưởng trong nghành dệt may ',
                           xaxis_title='Giá trị gia tăng (%)',
                           yaxis_title='Tần số')
    figTanSo.update_yaxes(range=[0, 15])

    figTanSuat = go.Figure()
    figTanSuat.add_trace(
        go.Pie(labels=khoang_Clothing, values=tanXuat_Clothing))

    figTstl = go.Figure()
    figTstl.add_trace(go.Scatter(x=khoang_Clothing,
                                 y=tanXuatTL_Clothing, marker=dict(color='#FF3366')))
    figTstl.update_layout(
        xaxis_title='Giá trị gia tăng',
        yaxis_title='Tần xuất tích lũy')

    figBox = go.Figure()
    figBox.add_trace(go.Box(y=df_Clothing['giá trị gia tăng trong sản xuất(%)'].values,
                            boxpoints='all'))

    hist = go.Figure()
    hist.add_trace(go.Histogram(
        x=df_Clothing['giá trị gia tăng trong sản xuất(%)'].values, name='giá trị gia tăng trong sản xuất(%)'))
    hist.update_layout(barmode='overlay')
    hist.update_traces(opacity=0.7)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(figTanSo, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(figTanSuat, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(figTstl, cls=plotly.utils.PlotlyJSONEncoder)
    graphBox = json.dumps(figBox, cls=plotly.utils.PlotlyJSONEncoder)
    histo = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, graphJSON1, graphJSON2, graphJSON3, ddf_Clothing, graphBox, histo
# -----PAGE5--------


def tansuat_tso_tstl_page5():
    year_Trades, value_Trades = getYear_Value(
        'Trade (% of GDP)')
    fig = go.Figure()
    fig.add_trace(go.Bar(x=year_Trades, y=value_Trades, text=value_Trades,
                         textposition='outside', marker=dict(color='#FF3366')))
    fig.update_layout(
        xaxis_title='Năm',
        yaxis_title='%GDP')
    stt = [i for i in range(1, len(year_Trades)+1)]
    df_Trades = {'STT': pd.Series(stt, index=stt),
                 'Year': pd.Series(year_Trades, index=stt),
                 'GDP(%)': pd.Series(value_Trades, index=stt, dtype='float')}
    df_Trades = pd.DataFrame(df_Trades)

    k_Trade = round((2*len(value_Trades))**(1/3))
    h_Trade = math.ceil(
        (float(max(value_Trades))-float(min(value_Trades)))/k_Trade)

    k1_Trade = round(min(value_Trades)+h_Trade, 2)
    k2_Trade = round(min(value_Trades)+2*h_Trade, 2)
    k3_Trade = round(min(value_Trades)+3*h_Trade, 2)

    khoang1_Trade, khoang2_Trade, khoang3_Trade, khoang4_Trade = [], [], [], []
    for i in value_Trades:
        if i < min(value_Trades)+h_Trade-0.01:
            khoang1_Trade.append(i)
        elif i >= min(value_Trades)+h_Trade and i < min(value_Trades)+2*h_Trade-0.01:
            khoang2_Trade.append(i)
        elif i >= min(value_Trades)+2*h_Trade and i < min(value_Trades)+3*h_Trade-0.01:
            khoang3_Trade.append(i)
        elif i >= min(value_Trades)+3*h_Trade:
            khoang4_Trade.append(i)

    khoang_Trade = ['< '+str(k1_Trade-0.01), str(k1_Trade) + " -" + str(
        k2_Trade-0.01), str(k2_Trade) + " - " + str(k3_Trade-0.01), '>=' + str(k3_Trade)]

    tanso_Trade = [len(khoang1_Trade), len(khoang2_Trade),
                   len(khoang3_Trade), len(khoang4_Trade)]

    tanXuat_Trade = [round((i*100)/(sum(tanso_Trade)), 2) for i in tanso_Trade]

    tanXuatTL_Trade = []
    s_Trade = 0
    for i in tanso_Trade:
        s_Trade += i
        tanXuatTL_Trade.append(s_Trade)

    # Đưa dữ liệu vào pandas
    stt = [j for j in range(1, len(khoang_Trade)+1)]
    ddf_Trade = {'Khoảng (%Tăng trưởng thương mại)': pd.Series(khoang_Trade, index=stt),
                 'Tần số': pd.Series(tanso_Trade, index=stt, dtype='int'),
                 'Tần xuất': pd.Series(tanXuat_Trade, index=stt, dtype='float'),
                 'Tần xuất tích lũy': pd.Series(tanXuatTL_Trade, index=stt, dtype='float')}
    ddf_Trade = pd.DataFrame(ddf_Trade)
    x_Trade = []
    x_Trade.append('0 - '+str(k1_Trade-0.01))
    x_Trade.append(str(round(k1_Trade, 2)) + " - " +
                   str(round(k2_Trade, 2)-0.01))
    x_Trade.append(str(round(k2_Trade, 2)) + " - " +
                   str(round(k3_Trade, 2)-0.01))
    x_Trade.append(str(round(k3_Trade, 2))+" - " +
                   str(round(max(value_Trades), 2)))

    tanso_Trade = [len(khoang1_Trade), len(khoang2_Trade),
                   len(khoang3_Trade), len(khoang4_Trade)]

    figTanSo = go.Figure()
    figTanSo.add_trace(go.Bar(x=khoang_Trade, y=tanso_Trade, text=tanso_Trade,
                              textposition='inside', marker=dict(color='#FF3366')))
    figTanSo.update_layout(title='Biểu đồ tần số sự tăng trưởng thương mại',
                           xaxis_title='Giá trị gia tăng (%)',
                           yaxis_title='Tần số')
    figTanSo.update_yaxes(range=[0, 15])

    figTanSuat = go.Figure()
    figTanSuat.add_trace(go.Pie(labels=khoang_Trade, values=tanXuat_Trade))

    figTstl = go.Figure()
    figTstl.add_trace(go.Scatter(
        x=khoang_Trade, y=tanXuatTL_Trade, marker=dict(color='#FF3366')))
    figTstl.update_layout(
        xaxis_title='Giá trị gia tăng ',
        yaxis_title='Tần xuất tích lũy')
    figBox = go.Figure()
    figBox.add_trace(go.Box(y=df_Trades['GDP(%)'].values,
                            name='GDP(%) ', boxpoints='all'))

    hist = go.Figure()
    hist.add_trace(go.Histogram(x=df_Trades['GDP(%)'].values, name='GDP(%)'))
    hist.update_layout(barmode='overlay')
    hist.update_traces(opacity=0.7)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(figTanSo, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(figTanSuat, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(figTstl, cls=plotly.utils.PlotlyJSONEncoder)
    graphBox = json.dumps(figBox, cls=plotly.utils.PlotlyJSONEncoder)
    histo = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, graphJSON1, graphJSON2, graphJSON3, ddf_Trade, graphBox, histo
# ---------PAGE4---------


def tansuat_tso_tstl_page4():
    year_Gross, value_Gross = getYear_Value(
        'Gross national expenditure (% of GDP)')
    value_Gross = [round(i, 2) for i in value_Gross]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=year_Gross, y=value_Gross, text=value_Gross,
                         textposition='inside', marker=dict(color='#339966')))
    fig.update_layout(
        xaxis_title='Năm',
        yaxis_title='USD')
    fig.update_yaxes(range=[60, 120])

    vl = [i for i in range(153, 180)]
    k_Gross = round((2*len(value_Gross))**(1/3))
    h_Gross = math.ceil(
        (float(max(value_Gross))-float(min(value_Gross)))/k_Gross)

    k1_Gross = round(min(value_Gross)+h_Gross, 2)
    k2_Gross = round(min(value_Gross)+2*h_Gross, 2)
    k3_Gross = round(min(value_Gross)+3*h_Gross, 2)

    khoang1_Gross, khoang2_Gross, khoang3_Gross, khoang4_Gross = [], [], [], []
    for i in value_Gross:
        if i < k1_Gross-0.01:
            khoang1_Gross.append(i)
        elif i >= k1_Gross and i < k2_Gross-0.01:
            khoang2_Gross.append(i)
        elif i >= k2_Gross and i < k3_Gross-0.01:
            khoang3_Gross.append(i)
        elif i >= k3_Gross:
            khoang4_Gross.append(i)

    khoang_Gross = ['< '+str(k1_Gross-0.01), str(k1_Gross) + " - " + str(
        k2_Gross-0.01), str(k2_Gross) + " - " + str(k3_Gross-0.01), '>=' + str(k3_Gross)]

    tanso_Gross = [len(khoang1_Gross), len(khoang2_Gross),
                   len(khoang3_Gross), len(khoang4_Gross)]
    tanXuat_Gross = [round((i*100)/(sum(tanso_Gross)), 2) for i in tanso_Gross]
    tanXuatTL_Gross = []
    s_Gross = 0
    for i in tanXuat_Gross:
        s_Gross += i
        tanXuatTL_Gross.append(s_Gross)
    # Đưa dữ liệu vào pandas
    stt = [j for j in range(1, len(khoang_Gross)+1)]
    ddf_Gross = {'Khoảng (%Chi tiêu Quốc gia)': pd.Series(khoang_Gross, index=stt),
                 'Tần số': pd.Series(tanso_Gross, index=stt, dtype='int'),
                 'Tần xuất': pd.Series(tanXuat_Gross, index=stt, dtype='float'),
                 'Tần xuất tích lũy': pd.Series(tanXuatTL_Gross, index=stt, dtype='float')}
    ddf_Gross = pd.DataFrame(ddf_Gross)

    tanso_Gross = [len(khoang1_Gross), len(khoang2_Gross),
                   len(khoang3_Gross), len(khoang4_Gross)]

    figTanSo = go.Figure()

    figTanSo.add_trace(go.Bar(x=khoang_Gross, y=tanso_Gross, text=tanso_Gross,
                              textposition='inside', marker=dict(color='#339966')))
    figTanSo.update_layout(title='Biểu đồ tần số tổng chi tiêu của Quốc gia',
                           xaxis_title='USD (%)',
                           yaxis_title='Tần số')
    figTanSo.update_yaxes(range=[0, 10])

    tanXuat_Gross = [round((i*100)/(sum(tanso_Gross)), 2) for i in tanso_Gross]
    figTanSuat = go.Figure()
    figTanSuat.add_trace(go.Pie(labels=khoang_Gross, values=tanXuat_Gross))

    figTstl = go.Figure()
    figTstl.add_trace(go.Scatter(
        x=khoang_Gross, y=tanXuatTL_Gross, marker=dict(color='#339966')))
    figTstl.update_layout(
        xaxis_title='USD',
        yaxis_title='Tần xuất tích lũy')

    stt = [i for i in range(1, len(year_Gross)+1)]
    df_Gross = {'STT': pd.Series(stt, index=stt),
                'Year': pd.Series(year_Gross, index=stt),
                'GDP(%) ': pd.Series(value_Gross, index=stt, dtype='float')}
    df_Gross = pd.DataFrame(df_Gross)
    figBox = go.Figure()
    figBox.add_trace(go.Box(y=df_Gross['GDP(%) '].values,
                            name='GDP(%) ', boxpoints='all'))

    hist = go.Figure()
    hist.add_trace(go.Histogram(x=df_Gross['GDP(%) '].values, name='GDP(%) '))
    hist.update_layout(barmode='overlay')
    hist.update_traces(opacity=0.7)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(figTanSo, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(figTanSuat, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(figTstl, cls=plotly.utils.PlotlyJSONEncoder)
    graphBox = json.dumps(figBox, cls=plotly.utils.PlotlyJSONEncoder)
    histo = json.dumps(hist, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, graphJSON1, graphJSON2, graphJSON3, ddf_Gross, graphBox, histo
# -----------PAGE3-----------


def tansuat_tso_tstl_page3():
    GDP_AFF_year, GDP_AFF_value = getYear_Value(
        'Agriculture, forestry, and fishing, value added (% of GDP)')
    Growth_AFF_year, Growth_AFF_value = getYear_Value(
        'Agriculture, forestry, and fishing, value added (annual % growth)')
    GDP_AFF_year.pop(-1)
    GDP_AFF_value.pop(-1)
    GDP_AFF_value = [round(i, 2) for i in GDP_AFF_value]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=Growth_AFF_year, y=Growth_AFF_value, mode='lines+markers',
                             name='% Tăng trưởng hàng năm', marker=dict(color='#fc6d00')))
    fig.add_trace(go.Bar(x=GDP_AFF_year, y=GDP_AFF_value, text=GDP_AFF_value,
                         textposition='outside', marker=dict(color='#0099ff'), name='%GDP'))
    fig.update_layout(title='Biểu đồ %GDP và % tăng trưởng hàng năm của nông, lâm, ngư nghiệp',
                      xaxis_title='Năm',
                      yaxis_title='Phần trăm')
    k_gdp = round((2*len(GDP_AFF_value))**(1/3))
    h_gdp = math.ceil((float(max(GDP_AFF_value)) -
                       float(min(GDP_AFF_value)))/k_gdp)

    k1_gdp = min(GDP_AFF_value)+h_gdp
    k2_gdp = min(GDP_AFF_value)+2*h_gdp
    k3_gdp = min(GDP_AFF_value)+3*h_gdp

    khoang1_gdp, khoang2_gdp, khoang3_gdp, khoang4_gdp = [], [], [], []
    for i in GDP_AFF_value:
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

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Chia khoảng % Tăng trưởng

    k_growth = round((2*len(Growth_AFF_value))**(1/3))
    h_growth = math.ceil(
        (int(max(Growth_AFF_value))-int(min(Growth_AFF_value)))/k_growth)

    k1_growth = min(Growth_AFF_value)+h_growth
    k2_growth = min(Growth_AFF_value)+2*h_growth
    k3_growth = min(Growth_AFF_value)+3*h_growth

    khoang1_growth, khoang2_growth, khoang3_growth, khoang4_growth = [], [], [], []
    for i in Growth_AFF_value:
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
    stt = [i for i in range(1, k_gdp+1)]
    ddf_gdp = {'Khoảng (GDP)': pd.Series(khoang_gdp, index=stt),
               'Tần số': pd.Series(tanso_gdp, index=stt, dtype='int'),
               'Tần xuất': pd.Series(tanXuat_gdp, index=stt, dtype='float'),
               'Tần xuất tích lũy': pd.Series(tanXuatTL_gdp, index=stt, dtype='float')}
    ddf_gdp = pd.DataFrame(ddf_gdp)
    stt = [j for j in range(1, k_growth+1)]
    ddf_growth = {'Khoảng (Tăng trưởng)': pd.Series(khoang_growth, index=stt),
                  'Tần số': pd.Series(tanso_growth, index=stt, dtype='int'),
                  'Tần xuất': pd.Series(tanXuat_growth, index=stt, dtype='float'),
                  'Tần xuất tích lũy': pd.Series(tanXuatTL_growth, index=stt, dtype='float')}
    ddf_growth = pd.DataFrame(ddf_growth)

    figTanSo1 = go.Figure()
    figTanSo1.add_trace(go.Bar(x=khoang_gdp, y=tanso_gdp, text=tanso_gdp,
                               textposition='inside', marker=dict(color='#0099ff')))

    figTanSo1.update_layout(
        xaxis_title='GDP (%)',
        yaxis_title='Tần số')
    stt = [i for i in range(1, len(GDP_AFF_year)+1)]
    df2 = {'STT': pd.Series(stt, index=stt),
           'Year': pd.Series(GDP_AFF_year, index=stt),
           'GDP': pd.Series(GDP_AFF_value, index=stt, dtype='float'),
           'Growth': pd.Series(Growth_AFF_value, index=[i for i in range(1, len(Growth_AFF_year)+1)], dtype='float')}
    df2 = pd.DataFrame(df2)
# lam toi day---------------------------------
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
        xaxis_title='GDP (%)',
        yaxis_title='Tần xuất tích lũy')

    box1 = px.box(df2, y='GDP', points="all")
    box1.update_layout(xaxis_title='GDP',
                       yaxis_title='Phần trăm')
    hist1 = px.histogram(df2, x='GDP')

    figTanSo2 = go.Figure()
    figTanSo2.add_trace(go.Bar(x=khoang_growth, y=tanso_growth, text=tanso_growth,
                               textposition='inside', marker=dict(color='#0099ff')))
    figTanSo2.update_layout(
        xaxis_title='Tăng trưởng (%)',
        yaxis_title='Tần số')

    figTanSuat2 = go.Figure()
    figTanSuat2.add_trace(go.Pie(labels=khoang_growth, values=tanXuat_growth))
    figTanSuat2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        xanchor="right",
        x=0.75
    ))
    figTSTL2 = go.Figure()
    figTSTL2.add_trace(go.Scatter(x=khoang_growth, y=tanXuatTL_growth))
    figTSTL2.update_layout(
        xaxis_title='Tăng trưởng(%)',
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

    box2 = px.box(df2, y='Growth', points="all")
    box2.update_layout(xaxis_title='Tăng trưởng',
                       yaxis_title='Phần trăm')

    hist2 = px.histogram(df2, x='Growth')

    gfig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    gtanso1 = json.dumps(figTanSo1, cls=plotly.utils.PlotlyJSONEncoder)
    gtansuat1 = json.dumps(figTanSuat1, cls=plotly.utils.PlotlyJSONEncoder)
    gtstl1 = json.dumps(figTSTL1, cls=plotly.utils.PlotlyJSONEncoder)
    gtanso2 = json.dumps(figTanSo2, cls=plotly.utils.PlotlyJSONEncoder)
    gtansuat2 = json.dumps(figTanSuat2, cls=plotly.utils.PlotlyJSONEncoder)
    gtstl2 = json.dumps(figTSTL2, cls=plotly.utils.PlotlyJSONEncoder)
    gbox1 = json.dumps(box1, cls=plotly.utils.PlotlyJSONEncoder)
    gbox2 = json.dumps(box2, cls=plotly.utils.PlotlyJSONEncoder)
    ghist1 = json.dumps(hist1, cls=plotly.utils.PlotlyJSONEncoder)
    ghist2 = json.dumps(hist2, cls=plotly.utils.PlotlyJSONEncoder)

# bang1 = json.dumps(ddf_gdp, cls=plotly.utils.PlotlyJSONEncoder)
# bang2 = json.dumps(ddf_growth, cls=plotly.utils.PlotlyJSONEncoder)

    return gfig, gtanso1, gtansuat1, gtstl1, gtanso2, gtansuat2, gtstl2, gbox1, gbox2, ghist1, ghist2, ddf_gdp, ddf_growth
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
                         textposition='outside', marker=dict(color='#f6c768')))
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
    for i in range(4):
        GDP_GS_year.pop(-1)
        GDP_GS_value.pop(-1)
    GDP_GS_value = [round(i, 2) for i in GDP_GS_value]
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
    fig.update_layout(title='Biểu đồ %GDP và % tăng trưởng hàng năm của xuất khẩu hàng hóa và dịch vụ',
                      xaxis_title='Năm',
                      yaxis_title='Phần trăm')
    figTanSo1 = go.Figure()
    figTanSo1.add_trace(go.Bar(x=khoang_gdp, y=tanso_gdp, text=tanso_gdp,
                               textposition='inside', marker=dict(color='#0099ff')))
    figTanSo1.update_layout(
        xaxis_title='GDP(%)',
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
        xaxis_title='GDP(%)',
        yaxis_title='Tần xuất tích lũy GDP')

    figTanSo2 = go.Figure()
    figTanSo2.add_trace(go.Bar(x=khoang_growth, y=tanso_growth, text=tanso_growth,
                               textposition='inside', marker=dict(color='#0099ff')))
    figTanSo2.update_layout(
        xaxis_title='Tăng trưởng (%)',
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
        xaxis_title='Tăng trưởng (%)',
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
