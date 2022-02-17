## Detectron2 Demo

We provide a command line tool to run a simple demo of builtin configs.
The usage is explained in [GETTING_STARTED.md](../GETTING_STARTED.md).

See our [blog post](https://ai.facebook.com/blog/-detectron2-a-pytorch-based-modular-object-detection-library-)
for a high-quality demo generated with this tool.

## 此Demo已与Detectron解耦合

通过修改VolleyBallDetect.py,可以改变其命令行参数，以达到不同的效果。

为了让配置不随文件位置移动而变化，我们将Detectron目录下的configs复制过来。只需要使用本路径下的configs即可。

### 其他说明

安装fvcore和的detectron2都是从官方下载下代码文件，自己在本地编译成python的库

之后可以在任何地方去调用detectron的库

detectron官方文件中的demo只是运用detectron2进行图像识别的例子，它不依赖于路径

