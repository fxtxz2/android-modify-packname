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
import os
import string
import random
import time
import ntpath
import subprocess
import re
# 生成签名库 v22copy/crazyspread/crazyspread.keystore
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
timestr = time.strftime("%Y-%m-%d_%H%M%S")
storeFilePath = os.path.join(dst + os.sep + pro_name + os.sep, timestr + ".keystore")
# 签名库文件名
storeFileName = path_leaf(storeFilePath)
storeFileDir = os.path.dirname(storeFilePath)
if not os.path.exists(storeFileDir):
    os.makedirs(storeFileDir)
# -dname "CN=名字与姓氏,OU=组织单位名称,O=组织名称,L=城市或区域名称,ST=州或省份名称,C=单位的两字母国家代码"
# 别名
alias = id_generator()
# 保存口令
storepass = id_generator()
# key口令
keypass = id_generator()
# 名字与姓氏
CN = id_generator()
# 组织单位名称
OU = id_generator()
# 组织名称
O = id_generator()
# 城市或区域名称
L = id_generator()
# 州或省份名称
ST = id_generator()
# 单位的两字母国家代码
C = id_generator(2, string.ascii_uppercase)
# 生存签名库
os.system("keytool -genkey -v -keyalg RSA -keysize 2048 -validity 10000 -keystore " + storeFilePath \
+ " -alias " + alias + " -storepass " + storepass + " -keypass " + keypass\
+ " -dname '" + "CN=" + CN + ",OU=" + OU + "," + "O=" + O + "," \
+ "L=" + L + "," + "ST=" + ST + "," + "C=" + C +"'")
# 获取签名库信息
output = subprocess.check_output("keytool -list -keystore " + storeFilePath + " -v -storepass " \
+ storepass + " | grep -E 'MD5'", shell=True)
storeFileMD5 = output.strip().split(" ")[1].replace(" ","").replace(":","")
storeReadMePath = os.path.join(dst + os.sep + pro_name + os.sep, storeFileName + ".readme")
storeReadMeDir = os.path.dirname(storeReadMePath)
if not os.path.exists(storeReadMeDir):
    os.makedirs(storeReadMeDir)
with open(storeReadMePath, "w") as readmeFile:
    readmeFile.write("签名库:" + storeFilePath + "\n")
    readmeFile.write("alias（别名）:" + alias + "\n")
    readmeFile.write("storepass（保存口令）:" + storepass + "\n")
    readmeFile.write("keypass（key口令）:" + keypass + "\n")
    readmeFile.write("CN（名字与姓氏）:" + CN + "\n")
    readmeFile.write("OU（组织单位名称）:" + OU + "\n")
    readmeFile.write("O（组织名称）:" + O + "\n")
    readmeFile.write("L（城市或区域名称）:" + L + "\n")
    readmeFile.write("ST（州或省份名称）:" + ST + "\n")
    readmeFile.write("C（单位的两字母国家代码）:" + C + "\n")
    readmeFile.write("MD5（微信应用签名）:" + storeFileMD5 + "\n")
readmeFile.closed

# 修改旧包名
for path, subdirs, files in os.walk(src):
    for name in files:
        oldPath = os.path.join(path, name)
        if oldPath == os.path.join(src, pro_name + "/build.gradle") \
        or oldPath == os.path.join(src, pro_name + "/src/main/AndroidManifest.xml") \
        or oldPath == os.path.join(src, pro_name + "/proguard-rules.txt"):
            new_pro_gradle_path = oldPath.replace(src, dst)
            dir = os.path.dirname(new_pro_gradle_path)
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(oldPath) as infile, open(new_pro_gradle_path, "w") as outfile:
                for line in infile:
                    # 修改3个配置文件 和 布局xml中旧包名
                    line = line.replace(oldPackage, newPackage)
                    # 修改签名库文件名
                    oldStoreFileName = re.findall(r"storeFile\sfile\(\"(.*?)\"\)", line)
                    if oldStoreFileName:
                        line = line.replace("".join(oldStoreFileName), storeFileName)
                    # 修改签名库保存口令
                    oldStorepass = re.findall(r"storePassword\s\"(.*?)\"", line)
                    if oldStorepass:
                        line = line.replace("".join(oldStorepass), storepass)
                    # 修改签名库别名
                    oldAlias = re.findall(r"keyAlias\s\"(.*?)\"", line)
                    if oldAlias:
                        line = line.replace("".join(oldAlias), alias)
                    # 修改签名库条目口令
                    oldKeypass = re.findall(r"keyPassword\s\"(.*?)\"", line)
                    if oldKeypass:
                        line = line.replace("".join(oldKeypass), keypass)
                    outfile.write(line)
            print("generate file:" + outfile.name)
            infile.closed
            outfile.closed
        elif name.endswith(".java"):
            # modify .java for crazyspread
            new_pro_java_path = oldPath.replace(oldPackage.replace(".", os.sep), newPackage.replace(".", os.sep)) \
            .replace(src,dst)
            dir = os.path.dirname(new_pro_java_path)
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(oldPath) as infile, open(new_pro_java_path, "w") as outfile:
                for line in infile:
                    line = line.replace(oldPackage, newPackage)
                    outfile.write(line)
            print("generate file:" + outfile.name)
            infile.closed
            outfile.closed
        elif all(i not in oldPath for i in exclude_dir):
            new_pro_gradle_path = oldPath.replace(src, dst)
            dir = os.path.dirname(new_pro_gradle_path)
            if not os.path.exists(dir):
                os.makedirs(dir)
            with open(oldPath) as infile, open(new_pro_gradle_path, "w") as outfile:
                for line in infile:
                    # 修改3个配置文件 和 布局xml中旧包名
                    line = line.replace(oldPackage, newPackage)
                    # 修改签名库文件名
                    oldStoreFileName = re.findall(r"storeFile\sfile\(\"(.*?)\"\)", line)
                    if oldStoreFileName:
                        line = line.replace("".join(oldStoreFileName), storeFileName)
                    # 修改签名库保存口令
                    oldStorepass = re.findall(r"storePassword\s\"(.*?)\"", line)
                    if oldStorepass:
                        line = line.replace("".join(oldStorepass), storepass)
                    # 修改签名库别名
                    oldAlias = re.findall(r"keyAlias\s\"(.*?)\"", line)
                    if oldAlias:
                        line = line.replace("".join(oldAlias), alias)
                    # 修改签名库条目口令
                    oldKeypass = re.findall(r"keyPassword\s\"(.*?)\"", line)
                    if oldKeypass:
                        line = line.replace("".join(oldKeypass), keypass)
                    outfile.write(line)
            print("generate file:" + outfile.name)
            infile.closed
            outfile.closed


# 运行shell
os.chdir(dst)
os.system("chmod 755 ./gradlew")
os.system("./gradlew assembleRelease")
print("install apk dir:" + os.getcwd() + os.sep + pro_name + "/build/outputs/apk")
