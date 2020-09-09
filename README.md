## Custom Loader
由于 toolkit框架默认的loader 在镜头加载数据时，遇到比较多的资产调用，会比较繁琐，特开发适用镜头的loder,实现批量加载功能。
根据镜头的assets 字段，查询镜头相关引用资产比提供批量加载功能；根据上下游环节，提供加载相关环节的数据。
比较适用于走组装流程的工作方式。
![image](https://github.com/DiLinTian/tk-cfaloader/blob/master/loader.png)