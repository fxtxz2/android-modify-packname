# android-modify-packname

## 参数配置
```python
# coding:utf-8
# 世界如此喧嚣 真相何其稀少
# 2016.05.26
# 原工程路径
src = "../AdSharePlugin2"
# 新工程路径
dst = "../AdSharePlugin3"
# 旧包名
oldPackage = "me.fengchuan.adshareplugin"
# 新包名
newPackage = "com.crazyspread.adshareplugin"
# 主项目名称
pro_name = "app"
# 还需要修改local.properties中的sdk.dir
# 排除的文件或目录
exclude_dir = [".svn/", ".idea/", "build/", "captures/", "22.iml", "crazyspread.iml"]
# =================上面参数可以修改=================
```

## 原理
chaning-package-name.py:批量修改Android工程的包名，主要过程是先生成签名库，并将相关签名库
信息保存到文件中；然后修改配置文件，.java和布局xml中的包名，以及主配置build.gradle中的签名库
相关信息；最后脚本自动调用./gradlew assembleRelease编译apk。

## 使用
配置好上述参数后
```shell
python ./chaning-package-name.py
```
