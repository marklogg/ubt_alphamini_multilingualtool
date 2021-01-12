# AlphaMini built-in language resource file conversion tool
There are some text and mp3 files built into the AlphaMini robot. These resource files are used by some of the built-in skills of UBTECH. If third-party users want to reuse the skills developed by UBTECH, they need to multilingualize the skills.
The multilingualization of built-in skills requires this tool. After the language resource files used by the built-in skills are translated, they are placed in the robot to overwrite the original resource files. This tool assists developers in generating language resource file formats in batches. simplify
AlphaMini multilingual internationalization process.

## Generate Res.apk file
The `.xlsx` file in the project `./excels` directory is the text resource table used by the built-in skill application of AlphaMini, `AND_KEY` is the text resource ID column and cannot be modified, and `Chinese` is the Chinese translation of the text resource ,
`English` is the English translation of text resources. If you want to translate it into Japanese, you can add a `Japanese` column in `xlsx` and translate the corresponding text into Japanese. When the translation is completed, go to `./build_res_apks.py `Script, modify
`language = ("Japanese", "values-ja")`; Then run the script `python build_res_apks.py`, and the Japanese res.apk resource will be generated in the build directory.


## Generate localTts mp3 audio file
In the `./language_localTts.xlsx` table, the text shown in the language column needs to be synthesized into the corresponding mp3 file and built into the robot. If you need to translate it into Japanese, customers can refer to the `English` column and put the text in the `English` column in order Translated into Japanese.
When the translation is completed, you can use the `./build_localtts.py` script to synthesize Japanese offline audio files, which requires the help of the customer's text-to-speech interface. The customer needs to implement the python call method:
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
Then you can use `python ./build_localtts.py` to generate localTts mp3 files.

## How to use the generated resources

* > The customer will send the finished language resources to UBTECH, which will be directly built into the ROM when the customer's robot leaves the factory

* > The customer puts the resources in the `/data/files/` directory through the `adb push` command