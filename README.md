# 手术视频示教系统

本仓库是系统的后端部分，前端部分在[这里](https://github.com/Sddft97/coelomoscope-video-player)。

## 使用方式

### 配置环境

建议创建虚拟环境后使用。
使用python自带的`venv`模块，其具体使用说明可参考[官方文档](https://docs.python.org/zh-cn/3/tutorial/venv.html)。

进入虚拟环境后，安装所需依赖。

```shell
pip install -r requirements.txt
```

> 项目使用的python版本为3.8.9

### 启动项目

后端项目使用`Django`编写，采用`Django`项目的启动方式即可。

```shell
python manage.py runserver # 启动项目，默认监听3000端口
```

### 配置文件与环境变量

项目提供了两套配置文件，即`dev`版本和`prod`版本，默认情况下会加载`dev`版本的配置，可以通过配置环境变量改变这一行为。

* 配置环境变量`CURRENT_ENV=dev`则加载`dev`版本配置
* 配置环境变量`CURRENT_ENV=prod`则加载`prod`版本配置

### 数据库连接

数据库使用MySQL 8.0.15，最好采用MySQL 8版本，未验证MySQL 5版本能否正常工作。

运行项目前需要自行修改配置文件中的数据库相关配置，配置完成后使用Django的数据库工具进行数据库连接和迁移。

```shell
# 按顺序执行以下两条命令
python manage.py makemigrations
python manage.py migrate
```

## 接口文档

项目中提供了4种接口文档，可以根据需求配合使用。
启动项目后，访问如下地址：

* [http://localhost:3000/swagger.yaml](http://localhost:3000/swagger.yaml)
  或者[http://localhost:3000/swagger.json](http://localhost:3000/swagger.json)，直接下载接口的yaml或json格式文档
* [http://localhost:3000/swagger/](http://localhost:3000/swagger/)
  ，swagger文档界面，介绍比较详细，功能比较全面，可以直接在页面里发送请求调用相应的接口，缺点是美观度一般
* [http://localhost:3000/redoc/](http://localhost:3000/redoc/)，redoc文档界面，整体比较清晰美观，介绍比较全面，缺点是不能直接发送请求调用接口，缺少互动性
* [http://localhost:3000/docs/](http://localhost:3000/docs/)，coreapi文档界面，美观度最佳，展示效果好，但是一些接口信息的展示存在错误

> 注意，接口文档中使用到的静态资源是由项目本身作为静态资源服务器提供的，这一功能只有在Django的设置`debug=True`时才会开启，
> 因此查看接口文档时需要启用`dev`版本的配置文件。

## 其他注意事项

### FFmpeg

项目中视频处理的部分大量使用到FFmpeg，因此需要先安装[FFmpeg](https://ffmpeg.org/)工具，安装完成后将其添加到环境变量`path`
中。

### 视频上传与处理工作流

视频上传后，后端需要结合FFmpeg和去雾模型进行处理，由于去雾模型目前没有提供api接口，因此还没有整合到处理流程中，也就是说，目前的工作流尚不完整，缺少去雾处理这一步骤。
视频处理流程可查看[View中的`merge_chunk`方法](apps/video/views.py)，总的来说分为如下几个步骤：

1. 将文件切片合成为一个完整的大文件。这与视频的分段上传有关，与视频处理关系不大，可以忽略
2. 将合成好的完整文件移动到指定目录下
3. 生成mpd文件的路径和视频封面文件的路径
4. 更新数据库信息
5. 开启子线程，进行视频处理相关工作
    1. 为视频生成封面，存放到之前生成的封面路径下
    2. (未整合)调用去雾模块，将视频进行去雾处理
    3. 调用FFmpeg，将**原视频和去雾后的视频**转码生成*1980x1080, 1280x720, 640x360*
       三种分辨率，这一步会生成一个视频的6种版本(见[表](#同一个视频的6个版本))
    4. 将生成的6个视频通过FFmpeg整合进一个mpd文件中，实现DASH转码
    5. 处理完成后更新数据库状态

由于目前去雾模型尚未完全接入，因此工作流不完整，如果需要展示视频的去雾效果，可以手动完成上述流程，具体来说，分以下步骤进行：

#### 为视频生成封面

调用FFmpeg或者其他工具完成，这里使用FFmpeg，命令格式为：

```shell
ffmpeg -i input.mp4
       -ss 00:00:00
       -v:f 1
       poster.png
```

#### 调用去雾模块

去雾模型目前只接受图片输入，并且输出也是图片，因此对整个视频去雾需要借助FFmpeg进行抽帧和合并。

首先是通过FFmpeg对视频进行抽帧，先获取原视频的帧率（可通过右键属性查看，opencv，FFmpeg等等方式），设为`$fps`，则抽帧命令为：

```shell
ffmpeg -i input.mp4
       -r $fps
       slice_output/slice%d.png
```

这个命令会在`slice_output`文件夹下生成一系列形如`slice1.png`的抽样图片，它们就是去雾模型的数据集。

之后进入到去雾模型的工程，调用去雾模型进行处理：

```shell
python main.py 
       --dataset_dir slice_output # 上一步生成的数据集文件夹
       --testmodelpath ./model/cho.ckpt # 模型的路径
       --testImagepath result # 去雾后图片的存放位置
       --predicting True # 开启预测模式
```

处理完成后，在目标文件夹中可以找到去雾后的图片，之后再使用FFmpeg将其合并为视频：

```shell
ffmpeg -i result/dahezed/sample175_%d.jpg # 去雾的图片
       -r $fps
       video_dehazed.mp4 # 生成的去雾视频
```

#### 调整分辨率

通过以上步骤，已经获得了原版视频`video.mp4`和去雾视频`video_dehazed.mp4`，接下来对其进行分辨率转换：

```shell
ffmpeg -i video.mp4 
       -filter_complex "[0]scale=1980x1080,setdar=16/9[s0];[0]scale=1280x720,setdar=16/9[s1];[0]scale=640x360,setdar=16/9[s2]" 
       -map [s0] -b:v 8M video_1980x1080.mp4 
       -map [s1] -b:v 4.5M video_1280x720.mp4 
       -map [s2] -b:v 1.5M video_640x360.mp4
```

这个命令处理原版视频，会一次性生成原视频的三个分辨率版本。
对去雾视频也使用相同的命令即可，但要注意调整码率。

```shell
ffmpeg -i video_dehazed.mp4 
       -filter_complex "[0]scale=1980x1080,setdar=16/9[s0];[0]scale=1280x720,setdar=16/9[s1];[0]scale=640x360,setdar=16/9[s2]" 
       -map [s0] -b:v 8.1M video_dehazed_1980x1080.mp4 
       -map [s1] -b:v 4.6M video_dehazed_1280x720.mp4 
       -map [s2] -b:v 1.6M video_dehazed_640x360.mp4
```

使用命令时，需要格外注意以下几点：

1. 命令中的`setdar`，用于指定生成视频的展示纵横比（DAR, Display Aspect Ratio），它决定了播放器以什么比例展示视频。
   由于生成的6个视频后续要进行DASH编码，编排到同一个mpd文件中，因此它们的DAR必须相等，在这里处理时统一设定为16:9。
2. 命令中通过`b:v`设定视频码率，1980x1080的码率设置为8M，1280x720的码率设置为4.5M，640x360的码率设置为1.5M。由于后续
   dash播放器调度视频的需要，相同清晰度下去雾视频的码率需要略高于原版视频的码率[（见图）](#码率梯度)
   ，如上述的去雾视频1980x1080，码率为8.1M。

#### dash编排

通过以上步骤，已经获得了原版视频的三种分辨率和去雾视频的三种分辨率，接下来需要将这6个视频编排进同一个mpd文件中：

```shell
ffmpeg -i video_1980x1080.mp4
       -i video_1280x720.mp4
       -i video_640x360.mp4
       -i video_dehazed_1980x1080.mp4
       -i video_dehazed_1280x720.mp4
       -i video_dehazed_640x360.mp4
       -map 0 
       -map 1
       -map 2
       -map 3
       -map 4
       -map 5
       -f dash
       -adaptation_sets "id=0,streams=v id=1,streams=a"
       -seg_duration 5 # 每一分片5秒
       -vcodec h264
       -acodec aac
       dash/output.mpd
```

这个命令会在`dash`文件夹下生成所有的分片文件，以及最终的mpd编排文件。

#### 更新数据库

视频处理完毕后，需要更新到数据库才能在客户端查看，与之相关的表主要是`video`表。

| 列名                | 说明                                              |
|-------------------|-------------------------------------------------|
| id                | 主键字段，不用填写，交给数据库自增                               |
| videoId           | 代表一个视频，需要填写，格式参考之前的记录即可，注意不要重复                  |
| videoName         | 视频名称，可以随便填写，不要重复                                |
| videoUrl          | 视频路径，填写之前生成的mpd文件路径                             |
| coverImgUrl       | 视频封面路径，填写之前生成的封面路径，也可以先不填                       |
| createdAt         | 创建于，自动生成即可                                      |
| lastModifiedAt    | 上次修改于，自动生成即可                                    |
| courseId          | 视频所属的课程id，可以在`course`表中找一个合适的填写                 |
| resolutionVersion | 视频分辨率，之前生成了三种，所以这里填`1980x1080,1280x720,640x360` |
| status            | 视频状态，已经处理完成的视频填入`3`                             |

更新完成后，建议通过接口文档或者其他方式，调用一下查询接口，看看返回的 **url** 能否访问到视频，之后继续调整。
接口返回的 **url** 在最前面额外拼接了静态服务器的地址和端口号，因此和数据库里看到的并不完全一致。
静态服务器可以通过配置文件中的`STATIC_SERVER`项更改，转换过程可见[Serializer中的FileUrlField](utils/serializer.py)。

## 附录

#### 同一个视频的6个版本

|         | 1980x1080 | 1280x720 | 640x360 |
|---------|-----------|----------|---------|
| **原版**  | 1         | 2        | 3       |
| **去雾版** | 4         | 5        | 6       |

#### 码率梯度

![码率梯度](https://s2.loli.net/2023/06/02/1U68AMhwY5JdLy9.png)
