<p align="center"><strong>English</strong> · <a href="README.zh-CN.md">简体中文</a></p>

![AI Video Director — Make an idea worth watching. Films by SIRSWS.](assets/cover.png)

# AI Video Director

**Make an idea worth watching.**

An Agent Skill by **[SIRSWS](https://github.com/sirsws)** for developing AI videos: the idea, the performance, the camera, the sound, and the revisions after generation. Built through ongoing creative work and audience feedback. Use it with the video models you choose.

[Watch the work](#films-and-the-decisions-behind-them) · [Install the skill](#start-making) · [Explore the methods](skills/ai-video-director/references/methods.md)

## Films and the decisions behind them

### Even the King of the Underworld Won't Take Me

[![Actual published footage: the King of the Underworld reads a bill and loses his composure.](assets/showcase/underworld.gif)](https://www.douyin.com/video/7694977783864836837)

An ordinary man brings his unpaid bills to the afterlife. The terrifying ruler suddenly wants him to live another fifty years.

**220,000 views on WeChat Channels. 2,020 remakes on Jimeng.** ¹

The bill changes who holds the power. Costume, expression, dialogue, and the ruler's movement make that reversal visible.

[Watch the published video ↗](https://www.douyin.com/video/7694977783864836837) · [Read the directing notes](showcase/underworld.en.md)

### There's a Foreigner! Let's Take a Photo

[![Actual published footage: Chinese holidaymakers surround a bewildered Australian at the Sydney Opera House.](assets/showcase/sydney.gif)](https://www.douyin.com/video/7693037053788959673)

Chinese holidaymakers fill the Sydney Opera House waterfront. An Australian local becomes the rare sight everyone wants a photo with.

**308,000 views on WeChat Channels.** ¹

The landmark establishes where we are; the crowd changes what feels normal. A local's puzzled reaction completes the joke.

[Watch the published video ↗](https://www.douyin.com/video/7693037053788959673) · [Read the directing notes](showcase/sydney.en.md)

### Tonight, We All See Him Off

[![Actual published footage: Ji Gong smiles with his fan and walks down a lane as neighbors see him off.](assets/showcase/jigong.gif)](https://www.douyin.com/video/7689014871601832057)

A farewell to Ji Gong, a beloved Chinese fictional monk. Doors and windows open along a lane; a familiar smile and a fan carry the goodbye.

**3,517 likes, 276 comments, 309 saves on Douyin.** ²

A character's particular gestures and the people who stay behind give the farewell its emotional shape. In feedback on the farewell films, the creator singled out the expression, fan work, and music.

[Watch the published video ↗](https://www.douyin.com/video/7689014871601832057) · [Read the directing notes](showcase/jigong.en.md)

**Everyday moments can become spectacles, too.** The National Day travel films turn a crowded mountain path into a martial-arts assembly, and a camel-tour traffic jam into a cavalry departure. [Explore the travel-to-spectacle designs →](showcase/holiday-spectacle.en.md)

<details>
<summary>Dates and sources for the audience figures</summary>

¹ Creator-reported snapshots: *Underworld*, WeChat Channels 220,000 views on October 13, 2026; Jimeng 98,000 views and 2,020 remakes on October 21. *Sydney*, WeChat Channels 308,000 views on October 8. A remake is another user's “make the same” creation, not a view or a like.

² Public Douyin snapshot on November 8, 2026. Only the group-farewell film is featured here.

Preview loops are excerpts from the linked published videos. WeChat Channels and Jimeng figures belong to those platforms, not the linked Douyin copies. Figures are dated observations of these works, not a promise of future performance. Historical films do not benchmark every instruction in the evolving skill.

</details>

## What you make with it

Bring an idea, a chosen concept, reference images, a rough prompt, or actual generated footage. Work from whatever you already have.

| Creative decision | What the skill helps you develop |
| :--- | :--- |
| **Why watch?** | A specific experience: a joke that lands, a moving encounter, a reveal, a performance, or a spectacular change |
| **How does it happen?** | Actions, reactions, space, camera position, light, pacing, and sound developed together |
| **What should the model receive?** | Copyable video prompts, image prompts when useful, and clear roles for actual reference inputs |
| **What needs changing?** | Review of actual footage, targeted revisions, continuity between clips, and editing when requested |

Ask for ideas, deepen one direction, get a production package, or repair a specific problem. Generate the video yourself or use an available, authorized tool.

## Start making

Send this to an assistant that supports Agent Skills:

~~~text
Install skills/ai-video-director from
https://github.com/sirsws/ai-video-director
~~~

Or copy the entire `skills/ai-video-director` folder into your client's supported skills directory. Keep its references, scripts, and licenses together; reload the client to discover it.

~~~text
Use $ai-video-director to develop a funny AI short.
An everyday frustration spills into a fantasy world.
Give me a few distinct ideas, each with a concrete action,
a key camera choice, and a payoff. I'll choose one to develop.
~~~

Already have something?

~~~text
Use $ai-video-director to develop this chosen concept.
Keep the central event. Work out the performance, camera, and sound.
Deliver the video prompt and useful reference-image prompts in English.
I will generate the video myself.
~~~

~~~text
Use $ai-video-director to review this actual generated video.
Identify what the footage shows and what misses my intended experience.
Revise the relevant staging, prompt, or inputs. Preserve what works.
~~~

**Different models, different durations.** The creative method is shared; reference support, identity binding, audio, duration, and prompt syntax follow your actual app, web, API, or CLI entry point. Platform notes are read when relevant. The skill does not include a universal generation API or guarantee equal results across models.

**English and Chinese guides.** Detailed methods are currently maintained in Chinese. Ask your assistant to deliver in your preferred language. If you installed an earlier version, replace its old skill folder with `ai-video-director` and use the new invocation above.

## Inside the skill

| Need | Open |
| :--- | :--- |
| Find an approach | [25 creative routes](skills/ai-video-director/references/methods.md): comedy, narrative, action, music, spectacle, products, travel, animation, and more |
| Make filming choices | [Camera, performance, light, sound, and rhythm](skills/ai-video-director/references/techniques/INDEX.md) |
| Choose useful inputs | [Reference-image decisions](skills/ai-video-director/references/reference-images.md) |
| Continue across clips | [Continuity](skills/ai-video-director/references/sequence-and-continuation.md) |
| Review and edit footage | [Post-production](skills/ai-video-director/references/post-production.md) |
| Study a small exercise | [Rain-pavilion tutorial](examples/rain-pavilion.en.md), a written design exercise |

Read what the scene needs. No fixed genre, shot count, or plot formula.

For ideas and prompts, an assistant that can read the skill is enough. Optional helpers use Python 3.10+, FFmpeg/ffprobe for editing, Pillow for alpha processing, or Blender for geometric camera previews. Install only what your task needs. Generation services have their own tools, access, and fees.

## Sources and contributions

Methods draw on [LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance), [Emily2040/seedance-2.0](https://github.com/Emily2040/seedance-2.0), [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills), [liangdabiao/Seedance2-Storyboard-Generator](https://github.com/liangdabiao/Seedance2-Storyboard-Generator), [dexhunter/seedance2-skill](https://github.com/dexhunter/seedance2-skill), and [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage). Thank you to their authors. [Attribution, versions, and licenses →](THIRD_PARTY_NOTICES.md)

Original skill instructions, code, and documentation are MIT licensed. Showcase footage has [separate media terms](assets/README.md). Independent project by SIRSWS.

[Share a work, improve a method, or contribute a translation](CONTRIBUTING.md). If the skill helps you make a better video, [give it a star](https://github.com/sirsws/ai-video-director).
