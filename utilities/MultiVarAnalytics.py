import matplotlib.pyplot as plt
import matplotlib
import scipy.stats as stats
from statsmodels.graphics.mosaicplot import mosaic

import statsmodels.api as sm
from statsmodels.formula.api import ols

import pandas as pd
import numpy as np
import scipy

import plotly.offline as py
from plotly import tools as tls
import plotly.graph_objs as go

class InteractionAnalytics():
    @staticmethod
    def rank_associations(df, conf_dict, col1, col2, col3, CheckWithPlotly = False):
        try:
            col2 = int(col2)
            col3 = int(col3)
        except:
            pass
        
        # Passed Variable is Numerical
        if not CheckWithPlotly:
            fig = plt.figure()
        else:#plotly
            fig = tls.make_subplots(rows=1, cols=2,
                                    subplot_titles=('Top {} Associated Numeric Variables'.format(str(col2)),
                                                    'Top {}  Associated Categoric Variables'.format(str(col2))))

        if (col1 in conf_dict['NumericalColumns']) :
            if len(conf_dict['NumericalColumns'])>1:
                
                # Interaction with numerical variables
                df2 = df[conf_dict['NumericalColumns']]
                corrdf = df2.corr()
                corrdf = abs(corrdf) # get the absolute values of correlations since negative correlations also matter
                corrdf2 = corrdf[corrdf.index==col1].reset_index()[[each for each in corrdf.columns \
                                                      if col1 not in each]].unstack().sort_values(kind="quicksort", 
                                                                                                  ascending=False).head(col2)
                corrdf2 = corrdf2.reset_index()
                corrdf2.columns = ['level0','level1','rsq']
                corrdf2.set_index('level0', inplace=True)

                tmp = corrdf2[['rsq']]
                x = [i for i in tmp.index]
                y = [j[0] for j in tmp.values]
                if not CheckWithPlotly:
                    ax1 = fig.add_subplot(121)
                    tmp.plot(kind='bar', ax=ax1)
                    ax1.legend().set_visible(False)
                    ax1.set_xlabel('Absolute Correlation')
                    ax1.set_title('Top {} Associated Numeric Variables'.format(str(col2)))
                else:#fully use plotly standard, not matplotlib_to_plotly to avoid poor chart & config
                    ax1 = go.Bar(x=x, y=y)
                    fig.append_trace(ax1, 1, 1)
                    fig['layout']['xaxis1'].update(title='Absolute Correlation')

                # Interaction with categorical variables
                etasquared_dict = {}
            if len(conf_dict['CategoricalColumns']) >= 1:
                for each in conf_dict['CategoricalColumns']:
                    mod = ols('{} ~ C({})'.format(col1, each),data=df[[col1,each]],missing='drop').fit()
                    aov_table = sm.stats.anova_lm(mod, typ=1)
                    esq_sm = aov_table['sum_sq'][0]/(aov_table['sum_sq'][0]+aov_table['sum_sq'][1])
                    etasquared_dict[each] = esq_sm

                topk_esq = pd.DataFrame.from_dict(etasquared_dict, orient='index').unstack().sort_values(\
                    kind = 'quicksort', ascending=False).head(col3).reset_index().set_index('level_1')
                topk_esq.columns = ['level_0', 'EtaSquared']

                tmp = topk_esq[['EtaSquared']]
                x = [i for i in tmp.index]
                y = [j[0] for j in tmp.values]
                if not CheckWithPlotly:
                    ax2 = fig.add_subplot(121)
                    tmp.plot(kind='bar',ax=ax2)
                    ax2.legend().set_visible(False)
                    ax2.set_xlabel('Eta-squared values')
                    ax2.set_title('Top {}  Associated Categoric Variables'.format(str(col2)))
                else:#fully use plotly standard, not matplotlib_to_plotly to avoid poor chart & config
                    ax2 = go.Bar(x=x, y=y)
                    fig.append_trace(ax2, 1, 2)
                    fig['layout']['xaxis2'].update(title='Eta-squared values')

        # Passed Variable is Categorical
        else:
            #Interaction with numerical variables
            if len(conf_dict['NumericalColumns']) >= 1:
                etasquared_dict = {}
                for each in conf_dict['NumericalColumns']:
                    mod = ols('{} ~ C({})'.format(each, col1), data = df[[col1,each]]).fit()
                    aov_table = sm.stats.anova_lm(mod, typ=1)
                    esq_sm = aov_table['sum_sq'][0]/(aov_table['sum_sq'][0]+aov_table['sum_sq'][1])
                    etasquared_dict[each] = esq_sm

                topk_esq = pd.DataFrame.from_dict(etasquared_dict, orient='index').unstack().sort_values(\
                    kind = 'quicksort', ascending=False).head(col2).reset_index().set_index('level_1')
                topk_esq.columns = ['level_0','EtaSquared']
                tmp = topk_esq[['EtaSquared']]
                x = [i for i in tmp.index]
                y = [j[0] for j in tmp.values]
                if not CheckWithPlotly:
                    ax1 = fig.add_subplot(121)
                    tmp.plot(kind='bar', ax=ax1)
                    ax1.legend().set_visible(False)
                    ax1.set_xlabel('Eta-squared values')
                    ax1.set_title('Top {} Associated Numeric Variables'.format(str(col2)))
                else:#plotly prepa
                    ax1 = go.Bar(x=x, y=y)
                    fig.append_trace(ax1, 1, 1)
                    fig['layout']['xaxis1'].update(title='Eta-squared values')


            # Interaction with categorical variables
            cramer_dict = {}
            if len(conf_dict['CategoricalColumns'])>1:
                for each in conf_dict['CategoricalColumns']:
                    if each !=col1:
                        tbl = pd.crosstab(df[col1], df[each])
                        chisq = stats.chi2_contingency(tbl, correction=False)[0]
                        try:
                            cramer = np.sqrt(chisq/sum(tbl))
                        except:
                            cramer = np.sqrt(chisq/tbl.as_matrix().sum())
                            pass
                        cramer_dict[each] = cramer

                topk_cramer = pd.DataFrame.from_dict(cramer_dict, orient='index').unstack().sort_values(\
                    kind = 'quicksort', ascending=False).head(col3).reset_index().set_index('level_1')
                topk_cramer.columns = ['level_0','CramersV']

                tmp = topk_cramer[['CramersV']]
                x = [i for i in tmp.index]
                y = [j[0] for j in tmp.values]
                if not CheckWithPlotly:
                    ax2 = fig.add_subplot(122)
                    tmp.plot(kind='bar', ax=ax2)
                    ax2.legend().set_visible(False)
                    ax2.set_xlabel("Cramer's V")
                    ax2.set_title('Top {} Associated Categoric Variables'.format(str(col2)))
                else:#plotly prepa
                    ax2 = go.Bar(x=x, y=y)
                    fig.append_trace(ax2, 1, 2)
                    fig['layout']['xaxis2'].update(title="Cramer's V")

        if CheckWithPlotly:
            py.iplot(fig)
        return fig

    @staticmethod
    def NoLabels(x):
        return ''
    @staticmethod
    def categorical_relations(df, col1, col2, CheckWithPlotly = False):
        if CheckWithPlotly:
            print("MOSAIC plot not available on plotly")
            return ""
    #     print col1, col2
        if col1 != col2:
            df2 = df[(df[col1].isin(df[col1].value_counts().head(10).index.tolist()))&(df[col2].isin(df[col2].value_counts().head(10).index.tolist())) ]
            df3 = pd.crosstab(df2[col1], df2[col2])
            df3 = df3+1e-8
        else:
            df3 = pd.DataFrame(df[col1].value_counts())[:10]
        fig,ax = plt.subplots()

        fig,rects = mosaic(df3.unstack(),ax=ax, statistic=False, labelizer=InteractionAnalytics.NoLabels, label_rotation=30)
    #     print rects 
        ax.set_ylabel(col1)
        ax.set_xlabel(col2)
        ax.set_title('{} vs {}'.format(col1, col2) )
    
    @staticmethod
    def numerical_relations(df, col1, col2, CheckWithPlotly = False):
        from statsmodels.nonparametric.smoothers_lowess import lowess
        x = df[col2]
        y = df[col1]
        lowess_results = lowess(y, x)  # [:,1]
        xs = lowess_results[:, 0]
        ys = lowess_results[:, 1]

        fit = np.polyfit(x, y, 1)
        fit1d = np.poly1d(fit)
        corr = round(scipy.stats.pearsonr(x, y)[0], 6)
        if not CheckWithPlotly:
            f, ax = plt.subplots(1)

            # lowess
            ax.scatter(x, y, c='g', s=6)
            ax.plot(xs,ys,'red',linewidth=1)

            #ols
            ax.plot(x, fit1d(x), '--b')
            ax.set_xlabel(col2)
            ax.set_ylabel(col1)
            ax.set_title('{} vs {}, Correlation {}'.format(col1, col2, corr))
            # return f
        else:
            # lowess
            t1 = go.Scatter(x=x,y=y,mode='markers', name='scatter(x,y)')
            t2 = go.Scatter(x=xs, y=ys, mode = 'lines', name='LOWESS(x,y)')#, line = dict(color = ('rgb(205, 12, 24)'))

            # ols
            t3 = go.Scatter(x=x, y=fit1d(x), mode='lines', line=dict(dash = 'dash'), name="poly1d[polyfit(x, y, 1)]")#color=('rgb(22, 96, 167)'),
            layout = go.Layout(title='{} vs {}, Correlation {}'.format(col1, col2, corr),
                               xaxis=dict(title=col2),
                               yaxis=dict(title=col1))
            fig = go.Figure(data=[t1, t2, t3], layout=layout)
            py.iplot(fig)
            # return fig

    @staticmethod
    def numerical_correlation(df, conf_dict, col1, CheckWithPlotly = False):
        from matplotlib.pyplot import quiver, colorbar, clim,  matshow
        df2 = df[conf_dict['NumericalColumns']].corr(method=col1)
        col_names = list(df[conf_dict['NumericalColumns']].columns)
    #     print col_names
        if not CheckWithPlotly:
            fig,ax = plt.subplots(1, 1)
            m = ax.matshow(df2, cmap=matplotlib.pyplot.cm.coolwarm)
            ax.grid(b=False)
            fig.colorbar(m)
            ax.set_xticklabels([' '] + col_names) #xticks extend the displayable area. Catering for this by adding a dummy value
            ax.set_yticklabels([' '] + col_names)
            #return df2
        else:
            t = go.Heatmap(z=df2.values,
                   x=col_names,
                   y=col_names)
            layout = go.Layout(title='Correlation of numerical variables')
            fig = go.Figure(data=[t], layout=layout)
            py.iplot(fig)

    @staticmethod
    def numerical_pca(df, conf_dict, col1, col2, col3, CheckWithPlotly = False):
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        num_numeric = len(conf_dict['NumericalColumns'])
        num_pca = num_numeric
        xticklabels = ['']
        for i in range(1,num_pca+1):
            xticklabels+=['Comp'+str(i)]
            xticklabels+=['']
        df2 = df[conf_dict['NumericalColumns']]
        X = StandardScaler().fit_transform(df2.values)
        pca = PCA(n_components=num_pca)
        pca.fit(X)

    #     print pca.explained_variance_ratio_

        if not CheckWithPlotly:
            fig = plt.figure()
        else:#plotly
            fig = tls.make_subplots(rows=1, cols=2, subplot_titles=('Top {} Associated Numeric Variables'.format(str(col2)),
                                                    'Top {}  Associated Categoric Variables'.format(str(col2))))

        x = np.arange(1,(num_numeric+1),1)
        y = pca.explained_variance_ratio_
        if not CheckWithPlotly:
            ax1 = fig.add_subplot(121)
            plt.bar(x, y)
            ax1.set_ylabel('% Variance Explained')
            ax1.set_xticklabels(xticklabels)
        else:
            ax1 = go.Bar(x=x, y=y, name="Comp.")
            fig.append_trace(ax1, 1, 1)
            fig['layout']['xaxis1'].update(title='% Variance Explained', ticktext=xticklabels, tickvals=list(x))

        x_pca_index = int(col2) - 1
        y_pca_index = int(col3) - 1

        Y_pca = pd.DataFrame(pca.fit_transform(X))
        Y_pca_labels = []
        for i in range(1,num_pca+1):
            Y_pca_labels.append('PC'+str(i))
        Y_pca.columns = Y_pca_labels
        
        Y_pca[col1] = df[col1]
        colors_dict = {}
        colors_list = ['r', 'y', 'c', 'y', 'k']
        j = 0
        for i in np.unique(df[col1]):
            colors_dict[i] = colors_list[j]
            j += 1
            if j == len(colors_list):
                j = 0

        colordf = pd.DataFrame.from_dict(colors_dict, orient='index').reset_index()
        colordf.columns = [col1, 'color']
        merged_df = pd.merge(colordf,Y_pca)
    #     print merged_df.head()
        grouped_df = merged_df.groupby(col1)
        if CheckWithPlotly:
            traces = []
        for name, group in grouped_df:
            x2 = group[Y_pca.columns[x_pca_index]]
            y2 = group[Y_pca.columns[y_pca_index]]

            if not CheckWithPlotly:
                ax2 = fig.add_subplot(122)
                plt.scatter(x2, y2,label=name,  # data
                   c=group['color'],                            # marker colour
        #             color='y',
                   marker='o',                                # marker shape
                   s=6                                       # marker size
                   )
            else:
                t = go.Scatter(x=x2,y=y2,mode='markers',name=name)
                fig.append_trace(t, 1, 2)
                #traces.append(t)

        if not CheckWithPlotly:
            ax2.set_xlabel(Y_pca.columns[x_pca_index])
            ax2.set_ylabel(Y_pca.columns[y_pca_index])
            ax2.legend(title=col1, fontsize=14)
        else:
            layout = go.Layout(title=col1)
            # fig.append_trace(traces, 1, 2)
            fig['layout']['xaxis2'].update(title=Y_pca.columns[x_pca_index])
            fig['layout']['yaxis2'].update(title=Y_pca.columns[y_pca_index])
            py.iplot(fig)
                
    @staticmethod
    def nc_relation(df, conf_dict, col1, col2, col3=None, CheckWithPlotly = False):
        tmp = df[[col1,col2]]
        mod = ols('{} ~ {}'.format(col1, col2), data=tmp).fit()
        aov_table = sm.stats.anova_lm(mod, typ=1)
        p_val = round(aov_table['PR(>F)'][0], 6)
        status = 'Passed'
        color = 'blue'
        if p_val < 0.05:
            status = 'Rejected'
            color = 'red'

        if not CheckWithPlotly:
            fig,ax = plt.subplots()
            f = tmp.boxplot(by=col2, ax=ax)

            #     ax.set_ylabel(col1)
            fig.suptitle('Ho {} (p_value = {})'.format( status, p_val), color=color, fontsize=10)
            #return p_val, status, color
        else:
            grouped = list(tmp.groupby(col2))
            # print(y)
            boxes = []
            for item in grouped:
                d = item[1][col1].values
                t = go.Box(y=d, name=item[0])
                boxes.append(t)
            layout = go.Layout(title='Ho {} (p_value = {})'.format( status, p_val),
                               font=dict(size=12, color=color))
            fig = go.Figure(data=boxes, layout=layout)
            py.iplot(fig)
    
    @staticmethod
    def pca_3d(df, conf_dict, col1, col2,  col3=None, CheckWithPlotly = False):
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        from mpl_toolkits.mplot3d import Axes3D
        df2 = df[conf_dict['NumericalColumns']]
        X = StandardScaler().fit_transform(df2.values)
        pca = PCA(n_components=4)
        pca.fit(X)
        Y_pca = pd.DataFrame(pca.fit_transform(X))
        Y_pca.columns = ['PC1','PC2','PC3','PC4']
        Y_pca[col1] = df[col1]

        colors_dict = {}
        colors_list = ['r', 'y', 'c', 'y', 'k']
        j = 0
        for i in np.unique(df[col1]):
            colors_dict[i] = colors_list[j]
            j += 1
            if j == len(colors_list):
                j = 0

        colordf = pd.DataFrame.from_dict(colors_dict, orient='index').reset_index()
        colordf.columns = [col1, 'color']
        merged_df = pd.merge(colordf, Y_pca)

        if not CheckWithPlotly:
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.view_init(elev=10, azim=int(col2))              # elevation and angle
            #     ax.dist=10
        else:#plotly
            traces = []

    #     print merged_df.head()
        grouped_df = merged_df.groupby(col1)
        for name, group in grouped_df:
            x = group['PC1']
            y = group['PC2']
            z = group['PC3']
            if not CheckWithPlotly:
                ax.scatter(x, y, z, label=name,  # data
                   c = group['color'],                            # marker colour
        #             color='y',
                   marker = 'o',                                # marker shape
                   s=6                                       # marker size
                   )
            else:
                t = go.Scatter3d(x=x, y=y, z=z, mode='markers', name=name)
                traces.append(t)

        if not CheckWithPlotly:
            ax.set_xlabel('PC1', labelpad=18)
            ax.set_ylabel('PC2', labelpad=18)
            ax.set_zlabel('PC3', labelpad=18)
            ax.legend(title=col1, fontsize=10)
        else:
            layout = go.Layout(
                scene=dict(
                    xaxis=dict(
                        title='PC1'),
                    yaxis=dict(
                        title='PC2'),
                    zaxis=dict(
                        title='PC3'), ),
                margin=dict(
                    r=20, b=10,
                    l=10, t=10)
            )
            fig = go.Figure(data=traces, layout=layout)
            py.iplot(fig)


    @staticmethod
    def pca_3d_new(df, conf_dict, col1, col2, col3, col4, col5, Export=False):
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        from mpl_toolkits.mplot3d import Axes3D
        df2 = df[conf_dict['NumericalColumns']]
        X = StandardScaler().fit_transform(df2.values)
        num_numeric = len(conf_dict['NumericalColumns'])
        pca = PCA(n_components=num_numeric)
        pca.fit(X)
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.view_init(elev=10, azim=int(col5))              # elevation and angle
    
        Y_pca = pd.DataFrame(pca.fit_transform(X))
        Y_pca_names = []
        for i in range(1, num_numeric+1):
            Y_pca_names.append('PC'+str(i))
        Y_pca.columns = Y_pca_names
        Y_pca[col1] = df[col1]
        colors_dict = {}
        colors_list = ['r', 'y', 'c', 'y', 'k']
        j = 0
        for i in np.unique(df[col1]):
            colors_dict[i] = colors_list[j]
            j += 1
            if j == len(colors_list):
                j = 0

        colordf = pd.DataFrame.from_dict(colors_dict, orient='index').reset_index()
        colordf.columns = [col1,'color']
        merged_df = pd.merge(colordf,Y_pca)
    
        grouped_df = merged_df.groupby(col1)
        for name, group in grouped_df:
            ax.scatter(
               group[Y_pca_names[int(col2)-1]], group[Y_pca_names[int(col3)-1]], group[Y_pca_names[int(col4)-1]], label=name,  # data
               c = group['color'],                            # marker colour
    #             color='y',
               marker = 'o',                                # marker shape
               s=6                                       # marker size
               )
        ax.set_xlabel(Y_pca_names[int(col2)-1], labelpad=18)
        ax.set_ylabel(Y_pca_names[int(col3)-1], labelpad=18)
        ax.set_zlabel(Y_pca_names[int(col4)-1], labelpad=18)
        ax.legend(title=col1, fontsize=10)
        
    @staticmethod
    def nnc_relation(df, conf_dict, col1, col2, col3, CheckWithPlotly = False):
        import itertools
        markers = ['x', 'o', '^']
        color = itertools.cycle(['r', 'y', 'c', 'y', 'k']) 
        groups = df[[col1, col2, col3]].groupby(col3)
        if not CheckWithPlotly:
            # Plot
            fig, ax = plt.subplots()
            ax.margins(0.05)

            #print groups
            for (name, group), marker in zip(groups, itertools.cycle(markers)):
                ax.plot(group[col1], group[col2], marker='o', linestyle='', ms=4, label=name)
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.legend(numpoints=1, loc='best', title=col3)
        else:
            # print(y)
            traces = []
            for item in groups:
                x = item[1][col1].values
                y = item[1][col2].values
                t = go.Scatter(x=x, y=y, mode = 'markers', name=item[0])
                traces.append(t)
            layout = go.Layout(title='',)
            fig = go.Figure(data=traces, layout=layout)
            fig['layout']['xaxis'].update(title=col1)
            fig['layout']['yaxis'].update(title=col2)
            py.iplot(fig)