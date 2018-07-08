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
            tmp = df[col1].value_counts()
            x = tmp.index
            y = tmp.values

            if not CheckWithPlotly:
                fig = plt.figure()
                ax0 = fig.add_subplot(121)
                tmp.plot(ax=ax0, kind='bar')
                ax0.set_title('Bar Plot of {}'.format(col1))

                ax1 = fig.add_subplot(122)
                tmp.plot(ax=ax1, kind='pie')
                ax1.set_title('Pie Chart of {}'.format(col1))
                return fig
            else:#fully use plotly standard, not matplotlib_to_plotly to avoid poor chart & config
                #TODO: Fix subplot for bar & pie together
                #fig = tls.make_subplots(rows=1, cols=2,subplot_titles=('Bar Plot of {}'.format(col1),'Pie Chart of {}'.format(col1)))
                ax0 = go.Bar(x=x, y=y)
                ax1 = go.Pie(labels=list(x), values=y)

                layout1 = go.Layout(title='Bar Plot of {}'.format(col1))#height=400, width=400, autosize=False,
                fig1 = go.Figure(data=[ax0], layout=layout1)
                py.iplot(fig1)

                layout2 = go.Layout(title='Pie Plot of {}'.format(col1))
                fig2 = go.Figure(data=[ax1], layout=layout2)
                py.iplot(fig2)
                # fig.append_trace(ax0, 1, 1)
                # fig.append_trace(ax1, 1, 2)
                # fig['layout'].update(height=600, width=800)
                # py.iplot(fig, filename=filename)
                return [fig1, fig2]

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
        tmp = df[col1].value_counts().nlargest(10)
        x = tmp.index
        y = tmp.values
        fig = plt.figure()

        ax0 = fig.add_subplot(121)
        if not CheckWithPlotly:
            tmp.plot(ax=ax0, kind='bar')
        else:
            plt.bar(x, y)
        ax0.set_xlabel(col1)
        ax0.set_title('Bar chart of {}'.format(col1))

        ax1 = fig.add_subplot(122)
        if not CheckWithPlotly:
            tmp.plot(ax=ax1, kind='pie')
        else:
            plt.pie(y, labels=x)
        ax1.set_title('Pie chart of {}'.format(col1))

        if CheckWithPlotly:  # transform to plotly viz
            # transform to plotly viz
            plotly_fig = tls.mpl_to_plotly(fig)
            f2 = py.iplot(plotly_fig)
            return f2

