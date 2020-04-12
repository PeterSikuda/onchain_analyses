import pandas as pd
import coinmetrics as cm
import pycoingecko as cg
import requests
import json
import plotly.graph_objs as go
import plotly.offline as po
import datetime
import time


com = cm.Community()

api = '041e6774-857f-4533-83ef-3baf35d1568e'


def cm_metric(asset,metric,start_date):
    asset = asset.lower()
    data = com.get_asset_metric_data(asset=asset,metrics=metric,start=start_date,end=datetime.datetime.now().strftime("%Y-%m-%d"))
    df = cm.cm_to_pandas(data)
    df.index = pd.to_datetime(df.index)

    return df


def gn_AdrActCnt(asset,start_date):
    start_date = int(time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    url = 'https://api.glassnode.com/v1/metrics/addresses/active_count?a='+ asset + '&s=' + str(start_date) + '&api_key=' + api
    r = requests.get(url=url)
    data = json.loads(r.content)
    df = pd.DataFrame(data,columns=['t','v'])
    df.columns = ['date','value']
    df['date'] = pd.to_datetime(df['date'],unit='s')
    df = df.set_index('date')
    df = df.tz_localize('UTC')
    return df


def gn_FeeTotNtv(asset,start_date):
    start_date = int(time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    url = 'https://api.glassnode.com/v1/metrics/fees/volume_sum?a='+ asset + '&s=' + str(start_date) + '&api_key=' + api
    r = requests.get(url=url)
    data = json.loads(r.content)
    df = pd.DataFrame(data,columns=['t','v'])
    df.columns = ['date','value']
    df['date'] = pd.to_datetime(df['date'],unit='s')
    df = df.set_index('date')
    df = df.tz_localize('UTC')
    return df


def gn_TxTfrValAdjNtv(asset,start_date):
    start_date = int(time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    url = 'https://api.glassnode.com/v1/metrics/transactions/transfers_volume_sum?a='+ asset + '&s=' + str(start_date) + '&api_key=' + api
    r = requests.get(url=url)
    data = json.loads(r.content)
    df = pd.DataFrame(data,columns=['t','v'])
    df.columns = ['date','value']
    df['date'] = pd.to_datetime(df['date'],unit='s')
    df = df.set_index('date')
    df = df.tz_localize('UTC')
    return df


def gn_TxTfrValMedNtv(asset,start_date):
    start_date = int(time.mktime(datetime.datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    url = 'https://api.glassnode.com/v1/metrics/transactions/transfers_volume_median?a='+ asset + '&s=' + str(start_date) + '&api_key=' + api    
    r = requests.get(url=url)
    data = json.loads(r.content)
    df = pd.DataFrame(data,columns=['t','v'])
    df.columns = ['date','value']
    df['date'] = pd.to_datetime(df['date'],unit='s')
    df = df.set_index('date')
    df = df.tz_localize('UTC')
    return df


def plot_AdrActCnt_diff(asset,start_date):
    try:
        cm_aac = cm_metric(asset,'AdrActCnt',start_date)
        gn_aac = gn_AdrActCnt(asset,start_date)
        trace_cm = go.Scatter(x=cm_aac.index,y=cm_aac.AdrActCnt,name='Coinmetrics',opacity=0.5)
        trace_gn = go.Scatter(x=gn_aac.index,y=gn_aac.value,name='Glassnode',opacity=0.5)
        gn_cm_diff = (cm_aac.AdrActCnt - gn_aac.value)/  cm_aac.AdrActCnt 
        diff = go.Scatter(x=cm_aac.index,y=gn_cm_diff,yaxis='y2',name='Difference in %',opacity=0.5)
        layout = go.Layout(title='{} Active Addresses'.format(asset),template='plotly_white',yaxis2=dict(overlaying='y',side='right',tickformat='%'),
                          legend=dict(xanchor='left',yanchor='top',orientation='h',x=0,y=1.1),hovermode='x')
        fig = go.Figure([trace_cm,trace_gn,diff],layout=layout)   
        return po.iplot(fig)
    
    except ValueError:
        return print('Active Addresses for {} are not available in one of the sources. Please select coin from the available list above'.format(asset))


def plot_FeeTotNtv_diff(asset,start_date):
    try:
        cm = cm_metric(asset,'FeeTotNtv',start_date)
        gn = gn_FeeTotNtv(asset,start_date)
        trace_cm = go.Scatter(x=cm.index,y=cm.FeeTotNtv,name='Coinmetrics',opacity=0.5)
        trace_gn = go.Scatter(x=gn.index,y=gn.value,name='Glassnode',opacity=0.5)
        gn_cm_diff = (cm.FeeTotNtv - gn.value)/  cm.FeeTotNtv 
        diff = go.Scatter(x=cm.index,y=gn_cm_diff,yaxis='y2',name='Difference in %',opacity=0.5)
        layout = go.Layout(title='{} Total Netwrok Fees (Usd)'.format(asset),template='plotly_white',yaxis2=dict(overlaying='y',side='right',tickformat='%'),
                          legend=dict(xanchor='left',yanchor='top',orientation='h',x=0,y=1.1),hovermode='x')
        fig = go.Figure([trace_cm,trace_gn,diff],layout=layout)      
        return po.iplot(fig)
    
    except ValueError:
        return print('Total Network Fees for {} are not available in one of the sources. Please select coin from the available list above'.format(asset))


def plot_TxTfrValAdjNtv_diff(asset,start_date):
    try:
        cm = cm_metric(asset,'TxTfrValAdjNtv',start_date)
        gn = gn_TxTfrValAdjNtv(asset,start_date)
        trace_cm = go.Scatter(x=cm.index,y=cm.TxTfrValAdjNtv,name='Coinmetrics',opacity=0.5)
        trace_gn = go.Scatter(x=gn.index,y=gn.value,name='Glassnode',opacity=0.5)
        gn_cm_diff = (cm.TxTfrValAdjNtv - gn.value)/  cm.TxTfrValAdjNtv 
        diff = go.Scatter(x=cm.index,y=gn_cm_diff,yaxis='y2',name='Difference in %',opacity=0.5)
        layout = go.Layout(title='{} Transfer Volume (Total)'.format(asset),template='plotly_white',yaxis2=dict(overlaying='y',side='right',tickformat='%'),
                          legend=dict(xanchor='left',yanchor='top',orientation='h',x=0,y=1.1),hovermode='x')
        fig = go.Figure([trace_cm,trace_gn,diff],layout=layout)
        return po.iplot(fig)
    except ValueError:
        return print('Transfer Volume (Total) {} are not available in one of the sources. Please select coin from the available list above'.format(asset))


def plot_TxTfrValMedNtv_diff(asset,start_date):
    try:
        cm = cm_metric(asset,'TxTfrValMedNtv',start_date)
        gn = gn_TxTfrValMedNtv(asset,start_date)
        trace_cm = go.Scatter(x=cm.index,y=cm.TxTfrValMedNtv,name='Coinmetrics',opacity=0.5)
        trace_gn = go.Scatter(x=gn.index,y=gn.value,name='Glassnode',opacity=0.5)
        gn_cm_diff = (cm.TxTfrValMedNtv - gn.value)/  cm.TxTfrValMedNtv 
        diff = go.Scatter(x=cm.index,y=gn_cm_diff,yaxis='y2',name='Difference in %',opacity=0.5)
        layout = go.Layout(title='{} Transfer Volume (Median)'.format(asset),template='plotly_white',yaxis2=dict(overlaying='y',side='right',tickformat='%'),
                          legend=dict(xanchor='left',yanchor='top',orientation='h',x=0,y=1.1),hovermode='x')
        fig = go.Figure([trace_cm,trace_gn,diff],layout=layout)
        return po.iplot(fig)
    except ValueError:
        return print('Transfer Volume (Median) for {} are not available in one of the sources. Please select coin from the available list above'.format(asset))


def plot_erc20_vs_mainnet(asset_erc,asset_main,metric):
    erc20 = cm_metric(asset_erc,metric)
    mainnet = cm_metric(asset_main,metric)
    trace_erc20 = go.Scatter(x=erc20.index,y=erc20[metric],name=asset_erc)
    trace_main = go.Scatter(x=mainnet.index,y=mainnet[metric],name=asset_main)
    layout = go.Layout(title='{} {} vs {}'.format(metric,asset_erc,asset_main),template='plotly_white',
                    legend=dict(xanchor='left',yanchor='top',orientation='h',x=0,y=1.1))
    fig = go.Figure([trace_erc20,trace_main],layout=layout)
    po.iplot(fig)