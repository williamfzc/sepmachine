# sepmachine

![PyPI](https://img.shields.io/pypi/v/sepmachine)

stagesepx workflow in production

## 目标

本项目将把视频采集部分与 stagesepx 进行连接，形成 设备->sepmachine->结果 的闭环流程。

在此基础上，开发者将可以快速利用它完成 app 各阶段耗时的全自动计算，并支持各种程度的灵活定制以适配不同业务需求。

## 结构

最适合重复任务与可定制化的设计自然是流水线模式，现在大多数CI平台已经证明了这套设计非常有效，这个项目也基于该套结构进行开发。

简单来说，流水线将管控任务进行情况，其他组件将作为节点嵌入其中。

- (video) capture
    - different platforms
        - android
        - ios
        - external camera
        - ...
    - (record and) return a video path to handler
- (video) handler
    - with (or without) trained models
    - hook functions for custom actions
- pipeline
    - bind capture and handler together, and make them work
    - loop

## 例子

既然要跟终端绑定，势必会带来很多环境、稳定性之类的麻烦事情，这也是我一直比较懒得做这个事情的原因。不过比起这个，我还是希望这个项目能有一种比较漂亮的方式着陆吧。这个仓库应该可以帮到在落地上比较迷茫的同学，毕竟基于这个，需要写的代码量真的非常少了。

一些额外依赖是免不了的，落地时可以考虑一并打包：

- 需要 ffmpeg 安装好并配置在 $PATH 下
- 需要 scrcpy 安装好并配置在 $PATH 下
- 需要 pip 装一下 uiautomator2，例子里的自动化由他驱动，论坛搜一下好多帖子（非必备，可以替换成你喜欢的）

完成后可以开始试着跑一下脚本：[传送门](./example)

有问题请 [issue](https://github.com/williamfzc/sepmachine/issues)

## license

[MIT](LICENSE)
