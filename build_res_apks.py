"""
该模块用于创建机器人多语言环境时使用的apk文件
This module is used to create the apk file used in the robot multilingual environment
"""
import os
import subprocess

import pandas as pd

# 列表第一个值是要生成的apk名,不可修改;第二个值是对应的string所在的xlsx
# The first value of the tuple is the apk name to be generated and cannot be modified;
# the second value is the xlsx where the corresponding string is located
constraint = [["FallClimbString", "language_FallClimb.xlsx", "com.ubtechinc.fallclimb"],
              ["JSEngineString", "language_JSEngine.xlsx", "com.ubtrobot.jsengine"],
              ["MainAppString", "language_MainApp.xlsx", "com.ubtrobot.master.policy"],
              ["CodeMaoString", "language_MiniProgramme.xlsx", "com.ubtechinc.codemao"],
              ["PcCodeMaoString", "language_PcCodemao.xlsx", "com.ubt.pccodemao"],
              ["SauronString", "language_Sauron.xlsx", "com.ubt.alphamini.facedetector"],
              ["SpeechActorString", "language_SpeechActor.xlsx", "com.ubtechinc.speechactor"],
              ["UpgradeString", "language_Upgrade.xlsx", "com.ubtrobot.action_provider"],
              ]
# 元组第一个值是xlsx里语言列名, 第二个值是android/res/values-xx目录名; 如果想生成对应语言的apk, 在xlsx中为该语言翻译对应的文本, 并为该列命名, 这里一英语为例
# The first value of the tuple is the name of the language column in xlsx, and the second value is the name of the
# android/res/values-xx directory; if you want to generate an apk for the corresponding language, translate the
# corresponding text for the language in xlsx, and set it for this Column naming, here is an example in English
language = ("English", "values")


def create_str(it):
    """
    Generate the language value corresponding to each key
    :param it:
    :return:
    """
    key = it["AND_KEY"]
    val = it[language[0]]
    if val.startswith("<ubt_string-array>"):
        rel = val.replace("<ubt_string-array>", "").replace("</ubt_string-array>", "")
        arr_str = rel.split("<ubt/>")
        rel = f"<string-array name=\"{key}\">"
        for s in arr_str:
            s = s.replace("\"", "\\\"")
            rel += f"<item>{s}</item>"
        rel += "</string-array>"
        return rel
    else:
        val = val.replace("\\", "")
        val = val.replace("'", "\\'")
        val = val.replace("\"", "\\\"")
        return f"<string name=\"{key}\">{val}</string>"


def create_res_string(xlsx_name: str):
    """
    Generate the content of the entire string.xml
    :param xlsx_name:
    :return:
    """
    t = pd.read_excel(f"./excels/{xlsx_name}")
    t["ks"] = t.apply(create_str, axis=1)
    rel = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    rel += "<!--Auto generated file, do not edit it!-->\n"
    rel += "<resources xmlns:tools=\"http://schemas.android.com/tools\" tools:ignore=\"ExtraTranslation\">\n"
    rel += "<string name=\"app_name\">Resources</string>\n"
    for ks in t["ks"]:
        rel += ks
        rel += "\n"
    rel += "</resources>"
    return rel


def copy_apk_template(root_dir: str):
    """
    Create the template file needed when packaging the apk
    :param root_dir:
    :return:
    """
    build_root_dir = f"./build/{root_dir}"
    print(f"rum_cmd: cp -rf ./template/* {build_root_dir}")
    if not os.path.exists(f'{build_root_dir}'):
        os.mkdir(f"./build/{root_dir}")
    _run_cmd(f"cp -rf ./template/* ./build/{root_dir}")
    print("run_cmd:end")


def create_res_apk(apk_name: str, xlsx_name: str, pkg_name: str):
    """
    Package  apk
    :param apk_name:
    :param xlsx_name:
    :param pkg_name
    :return:
    """
    copy_apk_template(apk_name)
    str_out = create_res_string(xlsx_name)
    write_string_to_xml(apk_name, str_out)
    _run_cmd(f"cd ./build/{apk_name} && ./gradlew :resource:assembleDebug && cd ../../")
    if os.path.exists(f"./build/{apk_name}/resource/build/outputs/apk/debug/resource-debug.apk"):
        if not os.path.exists(f"./build/localTts"):
            os.mkdir(f"./build/localTts")
        if not os.path.exists(f"./build/localTts/{pkg_name}"):
            os.mkdir(f"./build/localTts/{pkg_name}")
        _run_cmd(f"mv ./build/{apk_name}/resource/build/outputs/apk/debug/resource-debug.apk ./build/localTts/{pkg_name}/{apk_name}.apk")
        _run_cmd(f"rm -rf ./build/{apk_name}")
    else:
        print(f"create apk: {apk_name}, fail")


def _run_cmd(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result_f = process.stdout
    error_f = process.stderr
    errors = error_f.readlines()
    for err in errors:
        print(f"{str(err)[2:-1]}")
    result_str = result_f.readlines()
    for res in result_str:
        print(f"{str(res)[2:-1]}")
    if result_f:
        result_f.close()
    if error_f:
        error_f.close()


def write_string_to_xml(apk_name, str_out):
    file = open(f"./build/{apk_name}/resource/src/main/res/{language[1]}/strings.xml", "w")
    file.write(str_out)
    file.close()


def main():
    for apk_name, xlsx_name, pkg_name in constraint:
        create_res_apk(apk_name, xlsx_name, pkg_name)


if __name__ == '__main__':
    main()
