# 完整头区透明 Alpha

仅在实际处理含数字分身头部的图片、需要移除完整头区时读取并执行；包括带身体的造型图、多视图和完整画面。纯服装图和仅交付设计文字时无需读取本操作文件。

先生成并选定构图，再用 [transparent_head_alpha.py](../scripts/transparent_head_alpha.py) 对明确蒙版区域写入 Alpha。脚本只改变透明通道，不重新生成身体、服装或构图。

蒙版坐标必须根据每张选定图片重新确定，下面的数字只示意文件格式，不作为默认坐标。简单正面头区可以使用 ellipse；头发、颈部或遮挡关系复杂时，使用 polygon 或多个区域。

蒙版 JSON：

~~~json
{
  "coordinate_space": "normalized",
  "regions": [
    {
      "name": "user_full_head",
      "shape": "ellipse",
      "bbox": [0.40, 0.06, 0.60, 0.31]
    }
  ]
}
~~~

脚本依赖 Pillow。运行前只检查当前 Python 能否 `import PIL`；缺失时说明依赖，不擅自安装。调用时使用本 Skill 根目录的实际绝对路径，不假定当前工作目录就是 Skill 根目录：

~~~powershell
python -X utf8 "<本 Skill 根目录>\scripts\transparent_head_alpha.py" --input "<任务临时目录>\selected.png" --output "<任务临时目录>\selected-alpha.png" --spec "<任务临时目录>\head-mask.json" --preview-dir "<任务临时目录>\alpha-previews\<人物短名>"
~~~

脚本自动确认本次确实改变了 Alpha、RGB 未变化且输出同时包含透明与不透明像素；它不能识别人物或判断蒙版是否落在头部。交付前同时检查原图以及黑、白、绿底预览：

- 文件为 RGBA PNG，Alpha 同时包含 0 和 255。
- 透明区基本覆盖头发、脸、耳朵和领口以上颈部。
- 衣领、肩部、冠饰、道具和背景基本没有误删。
- 基本没有陌生脸缘、皮肤色边、白块、黑洞、键控色或画入的棋盘格。

蒙版细小错误可以接受，重大错误优先调整区域重跑。只有头部与必须保留的身体、道具或其他人物严重交叠，无法干净分离时，才重新生成构图。
