安装Detectron2: (Linux)

1、 pip install pycocotools

2、检查是否安装了torch，且torch版本是否与cuda版本匹配

检查cuda版本：nvcc -V

![image-20220421004950799](C:\Users\21104\AppData\Roaming\Typora\typora-user-images\image-20220421004950799.png)

检查torch版本：

python

import torch

torch.\__version__

![image-20220421005120639](C:\Users\21104\AppData\Roaming\Typora\typora-user-images\image-20220421005120639.png)

附注了其绑定cuda的版本，需要保证torch版本与cuda版本匹配，若不匹配，则pip uninstall torch之后重装

对应关系：https://pytorch.org/get-started/locally/

3. 安装detectron2：

   ```bash
   git clone https://github.com/facebookresearch/detectron2.git
   python -m pip install -e detectron2
   ```

   参见：https://detectron2.readthedocs.io/en/latest/tutorials/install.html