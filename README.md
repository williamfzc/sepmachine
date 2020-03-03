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

[传送门](./example)

## license

[MIT](LICENSE)
