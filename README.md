# 简单介绍
这个脚本用于获取免费的shadowsocks帐号。  
之前在看到这个项目https://github.com/yangyangwithgnu/autoshadower  自动获取免费的SS帐号，但是我在树莓派上编译运行了一下发现一开始获取帐号信息的时候就直接退出了，所以我就看了看他的源代码自己用python写了个脚本用于获取免费的ss帐号并存储为config.json文件。
# 使用方法
本脚本生成的```config.json```配置文件用于https://github.com/shadowsocks/shadowsocks-go 这个客户端使用，加载多个服务器设置。
将本脚本和```config.json```文件放在ss-go客户端所在的目录下用python运行即可。
