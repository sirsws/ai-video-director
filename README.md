# 邵看人生的 AI 视频制作 Skill

**Seedance／即梦平台优质创作者「邵看人生」的 AI 视频创作与制作方法。**

将一句构想逐步发展为具体的内容、人物表演、摄影、节奏和声音，再形成可用于生成的视频提示词与参考图方案。已有成片时，也可以用它审看问题、设计局部返修、衔接连续片段或完成本地剪辑。

作者：[邵看人生 · sirsws](https://github.com/sirsws)。这是个人创作实践中整理的方法，适合 Seedance／即梦，也可按实际能力适配其他 AI 视频平台。项目由独立创作者维护。

## 可以做什么

| 你手上有什么 | 可以推进到哪里 |
| --- | --- |
| 一句话、题材或模糊构想 | 找到值得看的具体过程，比较少量有实质差异的方向 |
| 已经选定的故事或拍法 | 完善动作、人物互动、镜头、声音与观看节奏 |
| 人物图、服装图、场景图 | 判断各图的用途，组织参考输入，编写完整制图词 |
| 一份视频提示词 | 检查表达是否落实已定方案，按实际平台与素材编译 |
| 实际生成的视频 | 根据实际素材分析问题，保留有效内容，局部返修 |
| 多段素材 | 设计接续、剪辑、字幕与声音安排，按授权执行本地处理 |

随包提供 **25 类方法入口**，覆盖叙事、对白、喜剧、悬疑、动作、歌舞、奇观、产品、旅行、动画等方向；摄影、表演、声音和输入方法按当前问题组合使用。

## 安装与开始使用

把下面这句话发给支持 Agent Skills 的助手：

> 请从 https://github.com/sirsws/seedance-video-skill 安装 `skills/jimeng-12s-video`，并读取其中的 SKILL.md。

也可以下载本仓库，将 `skills/jimeng-12s-video` **整个文件夹**放到所用客户端支持的 Skill 目录，保留 `references/`、`scripts/` 和 `agents/`，然后刷新或重启客户端以加载。

调用名称保留为 `$jimeng-12s-video`，便于兼容已有引用。名字中的 `12s` 是历史名称，实际时长按你的任务与生成入口确定。

安装后可以直接说：

```text
用 $jimeng-12s-video 做一个雨夜武侠短片。
主角只进亭、收伞、抖落雨水，不打斗。
先把动作与拍法设计清楚，再给我视频提示词。
```

```text
我已经选定这个构想，请继续完善摄影和声音。
只交付提示词和完整参考图制图词，我自己去平台生成。
```

```text
这是实际生成的视频。请看问题出在动作设计、参考图还是平台执行，
只改受影响的部分，保留已经成立的内容。
```

## 怎么工作

**接入已有要求 → 内容与声画共同设计 → 参考输入与提示词 → 检查与交付。**

已有方向就继续深化，局部修改就围绕反馈处理；全新方向才探索不同构想。希望先看想法、只要提示词或暂不出图，直接说明即可。

个人形象、默认画幅、平台入口、偏好与图库，可以写在自己的项目 `AGENTS.md` 中。Skill 根据当前项目配置工作，普通 AI 人物也能直接使用。

生成平台、模型、可用时长、参考素材与身份绑定方式，以你实际使用的入口为准。APP、网页、API 和 CLI 分别适配；需要直接执行生成时，使用另行配置且已获授权的工具。此 Skill 自身提供创作方法与本地辅助脚本，平台的会员、费用和生成权益按对应服务规则处理。

## 文件入口

- [Skill 主入口](skills/jimeng-12s-video/SKILL.md)：工作方式和按需阅读路线。
- [25 类创作方法](skills/jimeng-12s-video/references/methods.md)：从具体创作问题选择方法。
- [摄影、表演、声音等技法](skills/jimeng-12s-video/references/techniques/INDEX.md)：需要时再深入。
- [完整方法示例](skills/jimeng-12s-video/references/examples.md)：看内容、拍法与声音如何落实。
- [参考图方法](skills/jimeng-12s-video/references/reference-images.md)：组织身份、造型、场景与状态输入。
- [成片剪辑](skills/jimeng-12s-video/references/post-production.md)：根据实际媒体执行与核验。

日常写构想和提示词，读取相应方法即可。本地剪辑需要 Python 3.10+ 与 FFmpeg／ffprobe；Alpha 处理需要 Pillow；几何预演需要 Blender。只安装当前任务用到的工具。

制作包完成与成片完成分别判断。生成结果需要实际审看；静态画面、机器转写或参数检查，不能代替对运动、口型和声音的核验。创意判断也不承诺传播效果。

## 参考与致谢

整理过程中参考并融合了 [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance)、[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)、[zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills)、[liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator)、[dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) 和 [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) 的方法与思路，感谢原作者。

具体采用范围、固定版本与第三方许可见[来源与许可说明](THIRD_PARTY_NOTICES.md)。各来源的要求分别保留；来源作者与 Seedance／即梦平台未参与本项目维护。

本项目原创内容采用 [MIT 许可](LICENSE)；第三方改编部分保留对应版权与许可说明。
