# MSC双周脑震荡——预测NBA队伍季后赛晋级概率
## 安装
本程序基于python2.7+numpy+scipy+scikit-learn实现。在运行前请先安装所有环境和依赖库。
下面给出所有环境和库的资源下载地址和注意事项。

 - python2.7
 [点击下载python2.7.13][1]
*注意：安装python时要勾选添加环境变量选项，或者安装后人工添加，详见：[python2.7安装教程][2]。*

 - pip
 [点击下载pip][3]
*注意：如果你安装的是python2.7版本，pip是预装好的，可以直接使用无需安装。如果你无法使用pip请人工安装，详见：[pip安装教程][4]。*

 - numpy+mkl
[点击下载numpy+mkl][5]
*注意：本程序需要的是numpy+mkl库而不是numpy库，若已存在numpy库请先卸载numpy库，然后安装numpy+mkl。*
```
pip uninstall numpy # 卸载numpy
pip install numpy-1.11.3+mkl-cp27-cp27m-win_amd64.whl # 安装numpy-mkl
```
 - scipy
 [点击下载scipy][6]
 *注意：scipy依赖于numpy+mkl请安装好numpy+mkl后进行安装。*
 

```
pip install scipy-0.18.1-cp27-cp27m-win_amd64.whl #安装scipy
```

 - scikit-learn
 [点击下载scikit-learn][7]
 *注意：完成前面的步骤后，可以直接使用pip下载并安装scikit-learn，或者点击上面的链接下载scikit-learn的whl文件，使用和前面一样的方法安装scikit-learn。*

```
pip install -U scikit-learn # 方法一 下载并安装scikit-learn
pip install scikit_learn-0.18.1-cp27-cp27m-win_amd64.whl # 方法二 安装下载好的whl文件
```

 - pyExcelerator
 *注意：未找到本库的whl文件，可以直接使用pip安装。*
 

```
pip install pyExcelerator # 安装pyExcelerator
```

## 运行
使用命令行进入app文件夹路径下，在命令行输入：

```
python main.py
```
程序会自动读取所有测试数据（年份能被3整除的数据），并输出所有预测结果。
若要输出单一年份的结果，在命令行输入：

```
python main.py 86
```
*注意：*
 1. *为了解决windows端命令行中文输出乱码问题，代码中对输出进行了转码。此时若使用pyCharm等IDE运行会出现乱码，若使用IDE运行，请将*`nba_predict`*文件中*`predict_output()`*函数的所有*`.decode('utf-8').encode('gbk')`*代码删去即可。*
 2. *为了防止作弊程序内没有任何可以直接输出结果的代码，唯一的数据是data文件夹中的原始数据，该数据已经根据对阵情况进行了排名的修正。在程序第一次运行之后data_processed_rank和data_processed_diff文件夹内会有程序处理后的格式化的数据文件缓存，请不要改变目录结构。*



## 解题思路
在季后赛对决中，对阵规则是尽可能的让排名高球队和排名低球队先进行对决，排名高低不仅在一定程度上代表球队实力强弱，也能决定是否具有主场优势。在季后赛晋级预测中仅根据“排名高+主场赢得可能性大”这一规则即可达到较高准确率。
在本规则的基础之上，本程序训练了两个模型进行预测，帮助决策：

 - 提取两两季后赛对决球队之间的投篮、三分、罚球命中率、篮板数、助攻数、抢断数、盖帽数、失误数、场均得分、场均失分、胜场数各个值的差值作为特征，对决结果（胜或负）作为label，输入到Gradient Boosting Decision Tree（GBDT）模型中，训练出分类器进行预测。
 - 提取每支球队各项数据在当年对应联盟的排名作为特征，该球队每一轮是否晋级作为label，输入到GBDT模型中，训练出模型进行预测。

由于时间跨越30年，联盟的主流打法也有了很大的改变，为了让不同时期的预测符合当时的情况，在训练集构建的时候采用时间滑窗的方法，取与预测年份较为接近的训练数据进行训练。
最终将“排名+主客场”规则和两个模型进行加权融合得到最终的模型。
由于ensemble方法存在一定的随机性，为了使结果稳定，本程序每次预测将用最终模型预测多次，对结果进行投票，输出票数最高者。

  [1]: https://www.python.org/downloads/release/python-2713/
  [2]: http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001374738150500472fd5785c194ebea336061163a8a974000
  [3]: https://pypi.python.org/pypi/pip#downloads
  [4]: http://www.tuicool.com/articles/eiM3Er3
  [5]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
  [6]:http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
  [7]:http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-learn