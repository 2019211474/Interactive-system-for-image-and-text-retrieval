# Interactive-system-for-image-and-text-retrieval
首先展示代码概览：

![code overview](https://github.com/user-attachments/assets/f5cdda02-4ae9-4845-ac30-975a1572478d)

接下来是我所创建项目的主页，包括以文搜图、以图搜图、图文搜图、以及比较实验
**主页**

![homepage](https://github.com/user-attachments/assets/2087bd01-3167-4013-aab4-89fe18028ca9)

**以文搜图**
顾名思义就是使用文本去描述寻找的目标图片，不断的使用人为描述，模型根据人为描述去搜索目标图片

![text2image](https://github.com/user-attachments/assets/41170cc7-8682-4f70-b085-139282f9ec05)

**以图搜图**
顾名思义就是使用原始图片去搜索目标图片，模型根据图片的相似度不断的进行多轮搜索，测试者可以更新更相似搜索结果替代原图片。

![image2image](https://github.com/user-attachments/assets/b2e9f30c-8513-4c2a-acaa-bf73692ebf23)

**图文搜索**
顾名思义就是结合图片和人为的语言描述去检索目标图片，模型根据不断变化的多模态信息找到目标图片

![(text image)2image](https://github.com/user-attachments/assets/2df28ce8-c189-49b2-b0b4-f298508fa41f)
我们实验的目的就是验证多模态信息的利用有利于用户意图的识别，加快用户的搜索进度和搜索体验。
**声明**

我个人全程参与或者说主持这个项目的系统开发过程，具体的算法模型是我师兄提供的。
