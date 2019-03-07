import pandas as pd
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pyecharts import Geo
from pyecharts import Map

a=pd.read_excel(r'E:\ppp\ppp.xls')

#地区分布
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  #解决坐标轴负数的负号显示问题
plt.xlabel("地区")
plt.title("地区分布")
dd=pd.value_counts(a['地点'])
print(dd)
dd[:10].plot(kind='bar',rot=0)
plt.show()


data =[('北京',329),('上海',187),('杭州',69),('深圳',64),('广州',49),('南京',17),('成都',18),('武汉',16),('西安',9),('郑州',9),('长沙',8),('苏州',5),('福州',6),('厦门',4),('重庆',4),('宁波',4),('石家庄',3),('珠海',4),('天津',3),('烟台',2),('青岛',2),('昆明',2),('大连',2),('合肥',3),('菏泽',1)]
geo = Geo("地点分布", "分布对比图", title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value,type='heatmap',visual_range=[0, 300], maptype='china', visual_text_color="#fff", is_visualmap=True)
geo.render("地区分布对比图.html")

data =[('北京',329),('上海',187),('杭州',69),('深圳',64),('广州',49),('南京',17),('成都',18),('武汉',16),('西安',9),('郑州',9),('长沙',8),('苏州',5),('福州',6),('厦门',4),('重庆',4),('宁波',4),('石家庄',3),('珠海',4),('天津',3),('烟台',2),('青岛',2),('昆明',2),('大连',2),('合肥',3),('菏泽',1)]
geo = Geo("地点分布", "分布区域图", title_color="#fff",
          title_pos="center", width=1200,
          height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value,type='heatmap',visual_range=[0, 50], maptype='china', visual_text_color="#fff", is_visualmap=True)
geo.render("地区分布区域图.html")

#区域分布
top_10=a.groupby(['地点','区域'])['区域'].count().sort_values(ascending=False)
print(top_10[:10])
districts = ['朝阳区', '海淀区', '东城区','丰台区','大兴区','石景山区','西城区']
areas = [162,126,19,10,8,2,2]
map_1 = Map("北京市主要岗位分布", width=1200, height=600)
map_1.add("", districts, areas, maptype='北京', is_visualmap=True, visual_range=[min(areas), max(areas)],
        visual_text_color='#000', is_map_symbol_show=False, is_label_show=True)
map_1.render('北京市主要岗位分布.html')

from pyecharts import Map
data = [('嘉定区',1), ('宝山区',1), ('徐汇区',39),('普陀区',6),('杨浦区',21),('松江区',2),('浦东新区',51),('虹口区',7),('长宁区',31),('闵行区',12),('闸北区',2),('青浦区',1),('静安区',8),('黄浦区',5)]
attr, value = geo.cast(data)
map_1 = Map("上海市主要岗位分布", width=1200, height=600)
map_1.add("", attr,value, maptype='上海', is_visualmap=True, visual_range=[1,51],
        visual_text_color='#000', is_map_symbol_show=False, is_label_show=True)
map_1.render('上海市主要岗位分布.html')

#规模
plt.title("公司规模")
gm=pd.value_counts(a['规模'])
print(gm)
gm.plot(kind='bar',rot=0)
plt.show()

#经验
plt.title("经验要求")
jy=pd.value_counts(a['经验'])
print(jy)
jy.plot(kind='barh',rot=0)
plt.show()

#学历要求
plt.title("学历要求")
xl=pd.value_counts(a['学历'])
print(xl)
xl.plot(kind='barh',rot=0)
plt.show()

#工资分布
def avg_gz(gz):
    try:
        s_list=gz.split('-')
        s_min=int(s_list[0][:-1])
        s_max=int(s_list[1][:-1])
        s_avg=float(s_max+s_min)/2
    except UnicodeEncodeError:
        s_list=gz.split('k')
        s_avg=float(int(s_list[0][:-1]))
    return s_avg
a['工资均值']=a['工资'].apply(avg_gz)
ax2=plt.subplot(111)
rect=ax2.hist(a['工资均值'],bins=30)
plt.title('工资分布情况')
plt.xlabel('k/月')
plt.xticks(range(5,50,2))
plt.show()

#分地区工资水平
cbcs=a.groupby(['地点'])['工资均值']
sdbc=dd[:5]
df=[]
for i in sdbc.index:
    c=cbcs.get_group(i).values
    df.append(c)
ax3=plt.subplot(111)
rect=ax3.boxplot(df)
ax3.set_xticklabels(sdbc.index)
plt.yticks(range(0,60,5))
plt.show()

#分经验工资水平
gbe=a.groupby(['经验'])['工资均值']
df=[]
for i in jy.index:
    c=gbe.get_group(i).values
    df.append(c)
ax4=plt.subplot(111)
rect=ax4.boxplot(df)
ax4.set_xticklabels(jy.index)
plt.yticks(range(0,60,5))
plt.show()

#职业技能关键词
text = (open(r'E:\ppp\she.txt', 'r', encoding='utf-8')).read()
cut = jieba.cut(text)
string = ' '.join(cut)
wc = WordCloud(
    background_color='white',
    collocations=False,
    width=1000,
    height=800,
    font_path=(r'C:\Windows\Fonts\msyh.ttc'),
    stopwords=['and','学习能力强','数据分析','职位要求','职位描述','岗位职责','任职要求','工作职责','岗位要求','任职资格','本科以上学历','本科及以上学历'])
wc.generate(text)
plt.imshow(wc)
plt.axis('off')
plt.figure()
plt.show()
wc.to_file('数据分析关键词.png')

text = (open(r'E:\ppp\sjfx.txt', 'r', encoding='utf-8')).read()
cut = jieba.cut(text)
string = ' '.join(cut)
wc = WordCloud(
    background_color='white',
    collocations=False,
    width=1000,
    height=800,
)
wc.generate(text)
plt.imshow(wc)
plt.axis('off')
plt.figure()
plt.show()
wc.to_file('数据分析英文关键词.png')

text = (open(r'E:\ppp\岗位需求.txt', 'r', encoding='utf-8')).read()
cut = jieba.cut(text)
string = ' '.join(cut)
wc = WordCloud(
    background_color='white',
    width=1000,
    collocations=False,
    font_path=(r'C:\Windows\Fonts\msyh.ttc'),
    stopwords=['xa0','本科及以上学历','工作职责','工作职责1','职责描述','岗位要求','职位要求','ishumei','数据挖掘','任职资格','岗位描述','本科以上学历','com','www'],
    height=800,
)
wc.generate(text)
plt.imshow(wc)
plt.axis('off')
plt.figure()
plt.show()
wc.to_file('数据挖掘关键词.png')

text = (open(r'E:\ppp\sjwj.txt', 'r', encoding='utf-8')).read()
cut = jieba.cut(text)
string = ' '.join(cut)
wc = WordCloud(
    background_color='white',
    width=1000,
    collocations=False,
    height=800
)
wc.generate(text)
plt.imshow(wc)
plt.axis('off')
plt.figure()
plt.show()
wc.to_file('数据挖掘英文关键词.png')

