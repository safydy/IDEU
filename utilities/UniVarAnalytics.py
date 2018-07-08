import matplotlib.pyplot as plt
import scipy.stats as stats
import plotly.offline as py
from plotly import tools as tls
import plotly.graph_objs as go

py.init_notebook_mode(connected=True) #initiate the Plotly Notebook mode

class TargetAnalytics():
    ReportedVariables = []
    @staticmethod
    def custom_barplot(df,filename='',col1='', Export=False, CheckWithPlotly = False):
        if not CheckWithPlotly:
            f, (ax0,ax1) = plt.subplots(1, 2)
            df[col1].value_counts().plot(ax=ax0, kind='bar')
            ax0.set_title('Bar Plot of {}'.format(col1))
            df[col1].value_counts().plot(ax=ax1, kind='pie')
            ax1.set_title('Pie Chart of {}'.format(col1))
        else: # Plotly code equivalent Transcode
            tmp = df[col1].value_counts()
            x = tmp.index
            y = tmp.values
            fig = plt.figure()
            ax0 = fig.add_subplot(121)
            ax0.title.set_text('Bar Plot of {}'.format(col1))
            plt.bar(x, y)
            ax1 = fig.add_subplot(122)
            ax1.title.set_text('Pie Chart of {}'.format(col1))
            plt.pie(y, labels = x)
            # transform to plotly viz
            plotly_fig = tls.mpl_to_plotly(fig)
            f2 = py.iplot(plotly_fig)
            return f2


class NumericAnalytics():
    @staticmethod
    def shapiro_test(x):
        p_val = round(stats.shapiro(x)[1],6)
        status = 'passed'
        color = 'blue'
        if p_val < 0.05:
            status = 'failed'
            color = 'red'
        return status, color, p_val

    @staticmethod
    def custom_barplot(df, filename='', col1='', Export=False):
        fig, axes = plt.subplots(2,2)
        axes = axes.reshape(-1)
    #     print df[col].describe()
        df[col1].plot(ax=axes[0], kind='hist')
        axes[0].set_title('Histogram of {}'.format(col1))
        df[col1].plot(ax=axes[1], kind='kde') # Not plt equivalent found
        axes[1].set_title('Density Plot of {}'.format(col1))
        ax3 = plt.subplot(223)
        stats.probplot(df[col1], plot=plt) # Not plt equivalent found
        axes[2].set_title('QQ Plot of {}'.format(col1))
        df[col1].plot(ax=axes[3], kind='box')
        axes[3].set_title('Box Plot of {}'.format(col1))
        status, color, p_val = NumericAnalytics.shapiro_test(df[col1])
        fig.suptitle('Normality test for {} {} (p_value = {})'.format(col1, status, round(p_val, 6)), color=color, fontsize=12)
        # return f

class CategoricAnalytics():
    @staticmethod
    def custom_barplot(df, filename='', col1='', Export=False, CheckWithPlotly = False):
        if not CheckWithPlotly:
            f, (ax0,ax1) = plt.subplots(1,2)
            df[col1].value_counts().nlargest(10).plot(ax=ax0, kind='bar')
            ax0.set_xlabel(col1)
            ax0.set_title('Bar chart of {}'.format(col1))
            df[col1].value_counts().nlargest(10).plot(ax=ax1, kind='pie')
            ax1.set_title('Pie chart of {}'.format(col1))
            # return f
        else:
            tmp = df[col1].value_counts().nlargest(10)
            x = tmp.index
            y = tmp.values
            fig = plt.figure()
            ax0 = fig.add_subplot(121)
            ax0.title.set_text('Bar chart of {}'.format(col1))
            plt.bar(x, y)
            ax1 = fig.add_subplot(122)
            ax1.title.set_text('Pie chart of {}'.format(col1))
            plt.pie(y, labels = x)
            # transform to plotly viz
            plotly_fig = tls.mpl_to_plotly(fig)
            f2 = py.iplot(plotly_fig)
            return f2
