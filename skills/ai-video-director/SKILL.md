---
name: ai-video-director
description: Develop AI short videos from ideas into directed scenes, reference inputs, and generation-ready prompts. Also supports multi-clip continuity, review of actual footage, targeted revisions, and editing. 用于 AI 短视频创作、声画设计、参考图、提示词、审片、接续与剪辑。
---

# AI Video Director

Develop videos with a concrete viewing payoff and memorable people or form. Deliver a production package suited to the actual generation entry point. Audience-appeal judgments must refer to what the piece does; a design assessment is not evidence of real performance.

## Working context

Follow the current request, the project's AGENTS.md, and any configuration or brief it explicitly references. The project supplies personal identity, creative taste, asset libraries, directories, and platform settings. This skill also works without project files. Use the video model, platform, and duration suited to the task; the creative method is not tied to a particular generator.

Check only conditions that change the current design or execution: the platform and actual entry point, duration and aspect ratio, supported references and identity binding, and whether the task calls for text, a production package, or authorized tool execution. Reuse known facts. Ask only when a missing fact changes the work. Design characters as needed; do not assume the user appears. For Jimeng / Seedance, consult the [entry-point adapter](references/platforms/jimeng-seedance.md) when relevant; app, web, and API capabilities are not interchangeable.

Reference-image delivery may mean copyable image prompts, suitable existing assets, or images made with an authorized available tool. Finishing a package does not authorize a generation service. Use local tools for deterministic cropping, conversion, and alpha work; preserve originals. Before an entry point is confirmed, develop the scene without inventing upload syntax or settings.

Review actual footage within the host's capabilities. When audio cannot be heard, use the user's explicit listening feedback; transcripts and stream metadata are not listening evidence. Keep frame extracts, tests, caches, and mask previews in a system temporary directory.

The [Chinese entry guide](SKILL.zh-CN.md) is a language-equivalent companion. Detailed references are maintained in Chinese. Read the relevant method and deliver in the user's requested language.

## Start from what exists

Identify whether the user brings an idea, story, treatment, prompt, or actual video; whether this is a new work, development, local revision, diagnosis, or edit; and what is fixed versus editable. Reuse existing decisions. Ask only for unresolved facts that materially affect intent or execution and cannot be established from the materials.

All concepts, treatments, and prompts enter scene development; existing material is the starting point. A local revision needs only the original intent and affected decisions: follow [local revision](references/production-and-delivery.md#local-revision). Inspect actual footage rather than assuming it fulfilled the prompt.

When feedback arrives, distinguish the viewing payoff, staging, input assets, and actual generation. A weak payoff or relationship needs scene development, not only more scale or adjectives. If the main experience works and only a local detail fails, preserve unaffected material and revise that detail.

## Main workflow

**Task intake → Scene development → Generation preparation → Check and deliver.**

1. Read [scene development](references/creative.md). Establish what the audience will actually see or hear and how interest develops through the piece. Content, performance, camera, rhythm, and sound serve the same experience. Use [method selection](references/creative.md#method-use) as needed.
2. For a new direction, offer a few meaningfully different concepts with the main action, key filmmaking choices, and viewing payoff. Let the user choose, unless autonomous selection is authorized. Develop an already chosen direction directly. Work out a continuous experience with the actions, interactions, camera, and sound it requires. If fully realizing the plan would still miss the requested experience, improve those decisions before preparing generation. Then complete the package without an additional default approval gate for directing or image plans.
3. Read [generation preparation and delivery](references/production-and-delivery.md). Identify what the references must add; choose text, existing assets, or new images accordingly. Check useful information and any unwanted pose, layout, or state constraints they introduce. Compile a prompt compatible with the actual inputs, then check the text, bindings, and upload list against the chosen design. Return changes to locked requirements or execution scope to the user.

Respect requests such as “ideas first,” “show the treatment,” “no image generation yet,” or “prompt only.” Complete the creative and input decisions necessary for that deliverable; keep the remaining work within scope.

<a id="delivery-status"></a>

When the agreed text or package is complete, mark that deliverable complete and update project indexes only under the project's rules. Do not automatically create a waiting-for-generation state, a return reminder, or a follow-up task. A completed package is not a generated or approved video. If the user later supplies actual footage and requests post-production, follow [optional editing](references/post-production.md): **source review and edit plan → editing → checks and delivery**. Preserve original media and distinguish package completion from finished-video completion.

## Read by task

| Current need | Where to read |
| --- | --- |
| An idea, existing concept, treatment, or prompt | [Scene development](references/creative.md); [25 creative routes](references/methods.md) for the relevant bundled methods. |
| Camera, performance, light, sound, or moving relationships | [Technique index](references/techniques/INDEX.md); [shooting treatment](references/shooting-treatment.md) for scene functions, overall approach, and endings. |
| Reference selection or creation | [Reference purposes and tradeoffs](references/reference-images.md#reference-selection); read production and acceptance guidance only when images are needed. Use a project asset index when supplied. |
| A reference work or returned video | [Reference-video review](references/reference-videos.md): distinguish observation, user description, and this design. Reuse sufficient existing analysis. |
| Multiple clips or the next continuation | [Sequences and continuation](references/sequence-and-continuation.md): separate the whole-piece plan from actually adopted material. |
| A competition, brand, or official assignment | Apply the provided workflow and current brief; do not turn historical exceptions into universal rules. |
| Checks, platform feedback, or local repairs | [Problem handling](references/production-and-delivery.md#repair-decision): gather evidence, then revise the relevant decisions, text, or assets. Analysis alone does not authorize edits. |

For specific works, templates, or source prompts, follow [reference selection and adaptation](references/reference-adaptation.md). Respect a project's source scope and indexes. Outside materials supply references rather than a second workflow. Do not scan private cases or old deliverables merely because this skill is active. Bundled methods can be used without downloading source repositories.

## Files and prior work

Follow the user's or project's save location. Without a save request, deliver in the conversation; do not assume private directories or indexes. Follow [delivery and records](references/production-and-delivery.md#delivery) for files, formats, continuations, and updates.

Check against the current objective and actual evidence. Keep a good draft when no new issue warrants a change. One failed generation does not automatically justify a redesign; one accepted result does not establish a success rate.
