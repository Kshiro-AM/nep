# NEP

本仓库是对[NEP](https://github.com/ICTMCG/News-Environment-Perception)的复现，加入了Gossipcop数据集的实验。

# 运行

详情请参阅原仓库，此处只介绍Gossipcop数据集的预处理。

## Gossipcop

将Gossipcop数据放入preprocess/Gossipcop/data下，例如preprocess/Gossipcop/data/gossipcop_v3_origin.json.

Gossipcop数据集[下载](https://github.com/junyachen/Data-examples)。

运行如下命令，会在data目录下生成news.json, val.json, test.json, train.json四个文件，将他们按照NEP原文要求放入指定位置即可。

```bash
cd preprocess/Gossipcop
python get_fromat_with_news.py
```
