gpsCalc v2 by znight@tom.com

一个经纬度计算程序

主要功能
1、经纬度与UTM坐标的转换
2、两点距离和方向的计算，包括大圆（最短）和固定（航行）距离
3、根据距离和方向计算目标点
4、国内县级以上单位经纬度
5、日出日落时间计算
6、磁偏角计算

数据来源：
大部分国内县级以上单位经纬度来自http://www.godeyes.cn
行政区划代码为截止至2005年12月31日的国家标准行政区划代码(国外部分除外)
地磁场数据来自NOAA

算法引用：
http://www.movable-type.co.uk/scripts/LatLong.html
http://williams.best.vwh.net/sunrise_sunset_algorithm.htm
http://www.ngdc.noaa.gov/seg/WMM/soft.shtml

附属工具：
c2g.pl 将城市坐标文件(citys.txt)转换为kml文件(citys.kml)
g2c.pl 将kml文件(由c2g生成的)转换成数据文件
upd.pl 将数据文件(由g2c生成的)转换成城市坐标文件(citys.txt.new)

Q&A:
什么是大圆距离和角度
	通过两点的地球表面的最大的圆(实际多为椭圆)，在这个圆上两点之间的弧是最短的，
	也就是说大圆距离是两点之间最短的距离。
	但是，由于大圆和经线切割的角度不是一定的，因此从起点到终点的航向也是不定的，
	即角度从初始角度变化到终止角度。
	由于地球上相对两点（比如0N0E和0N180E,10N100E和10S80W）之间的大圆是不确定
	的，因此本算法中相对两点间的大圆距离和角度不一定正确。
什么是固定航向距离和角度
	由于大圆航向的角度是不定的，因此不方便在航行时是用。而固定航向距离就是为了
	解决这个问题的。在固定航向中，起点到终点的径路以相同的角度切割所有的经线，
	因此初始角度和终止角度是相同的。由于固定航向距离不是大圆距离，所以路径不是
	最短的。
磁偏角是怎么计算的
	地球的磁极不是在北极点和南极点上，而是有比较大的偏移。另外，磁极每时每刻都
	在不停的运动着。再有，太阳风也影响了地磁场。因此，地磁场不是一个规则的形状。
	通过表格可以查到地球上几个测量点的磁偏角等数据，然后利用公式计算出任意地方
	的磁	偏角。磁偏角除了和经纬度相关，还和时间、高程相关。本程序适于计算2005年
	至2010年间的磁偏角数据。高程对于磁偏角的影响比较小，本程序计算中采用的高程
	为0。磁偏角数据为负数表示北磁极偏西，正数表示北磁极偏东。