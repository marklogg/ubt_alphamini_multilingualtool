# AlphaMini 内置语言资源文件转换工具
在AlphaMini机器人内置了一些文本和mp3文件,这些资源文件由优必选内置的一些技能所使用, 如果第三方用户想复用优必选已开发好的技能, 就需要对技能进行多语言化,
内置技能的多语言化, 需要用到本工具, 将内置技能所用的语言资源文件翻译好后, 放置到机器人里进行覆盖原有的资源文件. 本工具辅助开发者批量生成语言资源文件格式, 以简化
AlphaMini多语言国际化流程.

## 生成Res.apk文件
在工程`./excels`目录中的`.xlsx`文件, 是AlphaMini内置的技能应用需要使用的文本资源表, `AND_KEY`是文本资源ID列,不可修改, `Chinese`是文本资源的中文翻译,
`English`是文本资源的英文翻译, 假如要翻译成日文, 可以在`xlsx`中新增`Japanese`列并将对应文本翻译成日文, 当翻译完成后, 接下来在`./build_res_apks.py`脚本中,修改
`language = ("Japanese", "values-ja")` ; 然后运行脚本`python build_res_apks.py`, 就会在build目录下生成了日文res.apk资源.


## 生成localTts mp3音频文件
`./language_localTts.xlsx`表, 语言列所示文本是需要合成对应的mp3文件,并内置到机器人内的. 假如需要翻译成日文, 客户可以参考`English`列, 将`English`列文本依次翻译成日文.
当翻译完成后, 可以使用`./build_localtts.py`脚本合成日文离线的音频文件, 这是需要借助客户的text-to-speech接口的. 客户需要实现python的调用方法:
```python
def text_to_speech(file: str, text: str) -> bool:
    """
    Customers need to use their own text-to-speech interface to synthesize these texts into mp3 files.
    :param file:
    :param text:
    :return:
    """
    return False
```
接下来就可以用`python ./build_localtts.py`生成localTts mp3文件了.

## 如何使用生成的资源

* > 客户将制作完成的语言资源,发给优必选, 由我们在客户机器人出厂时直接内置到ROM里面

* > 客户将资源通过`adb push` 命令,将资源放置在`/data/files/`目录下



