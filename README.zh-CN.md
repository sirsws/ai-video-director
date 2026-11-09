<p align="center"><a href="README.md">English</a> · <strong>简体中文</strong></p>

<p align="center"><img src="assets/cover.png" alt="Seedance Video Skill：从构想到场景，邵看人生的 AI 视频创作与制作工具包。" width="100%"></p>

<h1 align="center">邵看人生的 AI 视频制作 Skill</h1>

<p align="center"><strong>让一个想法，有故事、有镜头、有声音。</strong><br>
从构想、声画设计到提示词、审片与剪辑的 Agent Skill。</p>

<p align="center"><a href="#开始使用">开始使用</a> · <a href="examples/rain-pavilion.zh-CN.md">试读完整示例</a> · <a href="skills/jimeng-12s-video/references/methods.md">探索创作方法</a></p>

<p align="center">
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-244A43?style=flat-square" alt="MIT 开源许可"></a>
<img src="https://img.shields.io/badge/Agent_Skill-9F422A?style=flat-square" alt="Agent Skill">
<img src="https://img.shields.io/badge/Creative_routes-25-244A43?style=flat-square" alt="25 类创作入口">
<img src="https://img.shields.io/badge/English_%2B_中文-F2E8D5?style=flat-square&amp;labelColor=244A43" alt="中英文使用指南">
</p>

由 **Seedance／即梦平台优质创作者 [邵看人生 · sirsws](https://github.com/sirsws)** 整理维护，来自持续 AI 视频创作中的方法积累。

## 把场景做得值得看

“电影感、唯美、史诗级”仍留下很多空白。这套 Skill 帮你先想清楚：**具体发生什么、镜头怎样让人看见、观众会听到什么**，再形成提示词。

内容与拍法一起发展：想法怎样变成有看点的行动，人物怎样进入空间，什么时候揭示信息，声音怎样改变一场戏。

| 你手上有什么 | 可以推进到哪里 |
| :--- | :--- |
| 一句话、题材或模糊构想 | 有具体观看过程、彼此有实质差异的方向 |
| 已经选定的构想 | 动作、表演、摄影、光色与声音方案 |
| 人物图、服装图、场景图 | 明确各图控制身份、造型、空间或起始状态的用途 |
| 一份初稿提示词 | 适配当前生成入口与实际素材的完整正文 |
| 实际生成的视频 | 有证据的诊断与针对性返修 |
| 多段素材 | 接续安排、剪辑方案与已获授权的本地处理 |

## 一个小场景，也能设计完整

**题目：** 旅人走进雨中的亭子，收伞。不打斗，不说话。

| 设计决定 | 它解决什么 |
| :--- | :--- |
| 人物到来前，先让亭子进入画面 | 路线和目的地清楚。 |
| 手、伞与门槛持续入画 | 收伞成为能被看清的动作。 |
| 水珠甩向干燥长凳之外 | 动作发生在真实的空间关系中。 |
| 进入亭下时，雨声从头顶退向外部 | 声音带出从淋雨到避雨的变化。 |

**[打开完整示例 →](examples/rain-pavilion.zh-CN.md)**：包含需求、拍法、可复制提示词与成片检查要点。这是文字设计演示，尚未作为视频生成效果验证。

## 开始使用

把下面的话发给支持 Agent Skills 的助手：

~~~text
请从 https://github.com/sirsws/seedance-video-skill
安装 skills/jimeng-12s-video 这个 Skill。
~~~

也可以下载仓库，将 `skills/jimeng-12s-video` **整个文件夹**放入所用客户端支持的 Skill 目录。保留参考文件、脚本和许可，刷新或重启客户端以加载。

安装后直接说：

~~~text
用 $jimeng-12s-video 做一个 15 秒的雨夜短片。
旅人走进木亭，收起雨伞，抖落雨水；不打斗，不说话。
把动作、镜头和声音设计清楚，给我最终视频提示词。
我自己去平台生成。
~~~

调用名保留为 `$jimeng-12s-video` 以兼容已有引用。**名字中的 `12s` 是历史名称，不限制实际时长。** 时长按你的任务和平台确定。

<details>
<summary><strong>已有想法或成片？也可以这样开始。</strong></summary>

**继续完善选定方向**

~~~text
用 $jimeng-12s-video 深化这个已选定的构想。
保留核心事件，完善调度、摄影和声音。
交付视频提示词与完整可复制的参考图制图词。
~~~

**复核真实生成结果**

~~~text
用 $jimeng-12s-video 审看这个实际生成的视频。
区分创意、拍法、提示词、参考图和平台执行的问题。
依据实际证据，只改受影响的内容，保留已经成立的部分。
~~~

</details>

## 工具包里有什么

**任务接入 → 内容与声画共同设计 → 参考输入与提示词 → 检查与交付。**

| 入口 | 可用内容 |
| :--- | :--- |
| [25 类创作方法](skills/jimeng-12s-video/references/methods.md) | 叙事、喜剧、悬疑、动作、歌舞、奇观、产品、旅行、动画等 |
| [摄影、表演与声音技法](skills/jimeng-12s-video/references/techniques/INDEX.md) | 机位、空间、表演、光色、声音、节奏与特效 |
| [参考图方法](skills/jimeng-12s-video/references/reference-images.md) | 选哪些输入、各自控制什么、应当保留哪些自由 |
| [完整设计示例](skills/jimeng-12s-video/references/examples.md) | 连续动作、拍摄安排与声音的具体落实 |
| [片段接续](skills/jimeng-12s-video/references/sequence-and-continuation.md) | 从实际采用的素材衔接下一段 |
| [剪辑后期](skills/jimeng-12s-video/references/post-production.md) | 素材审看、剪辑决定、本地执行与导出核验 |

**按当前问题读取所需方法。** 围绕这部作品组合使用，不因选了某种类别就固定剧情、镜头数量或风格。

### 语言与平台适配

- **中英文入口与指南。** 详细方法库目前以中文维护；可要求助手用中文或英文交付。
- **适用于 Seedance／即梦，也可适配其他入口。** 模型、时长、上传方式与身份绑定，以实际使用的 APP、网页、API 或 CLI 为准。
- **沿用你自己的偏好。** 身份、口味、默认画幅与图库规则，可以写在项目 `AGENTS.md` 中。
- **生成按授权执行。** Skill 提供方法与本地辅助脚本；实际调用生成服务需有可用工具及你的授权，费用按对应平台规则处理。

### 可选本地工具

| 任务 | 所需工具 |
| :--- | :--- |
| 构想、拍法与提示词 | 能读取 Skill 的助手 |
| 本地裁剪、拼接与字幕 | Python 3.10+、FFmpeg 与 ffprobe |
| 确定性 Alpha 处理 | Python 与 Pillow |
| 摄影与调度几何预演 | Blender |

只安装当前任务所需的工具。制作包与成片分别交付和判断；生成后的运动、口型与声音，仍需实际审看。

## 开放交流与来源

整理过程中参考并融合了 [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance)、[Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0)、[zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills)、[liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator)、[dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill) 和 [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) 的方法与思路，感谢原作者。

具体范围、固定版本与许可见[来源说明](THIRD_PARTY_NOTICES.zh-CN.md)。原创内容采用 [MIT 许可](LICENSE)，第三方许可分别保留。本项目由独立创作者维护，非 Seedance／即梦官方产品。

**用它做出了作品？** 欢迎[分享用法或提出改进](CONTRIBUTING.md)。可复核的实际观察，能帮助这套方法持续完善。

---

<p align="center"><strong>如果它帮你做出了更好的视频，欢迎点一颗 Star。</strong><br>
让更多创作者找到这套方法。<br><br>
<a href="https://github.com/sirsws/seedance-video-skill">在 GitHub 收藏</a> ·
<a href="https://github.com/sirsws/seedance-video-skill/issues">反馈与交流</a> ·
<a href="README.md">Read in English</a></p>
