<!--
SPDX-FileCopyrightText: 2017 The CC: Tweaked Developers

SPDX-License-Identifier: MPL-2.0
-->

# CCLuau — Minecraft 26.3

Independent, AI-assisted fork of CC: Tweaked, based on upstream `mc-26.3` at
`a95dbe739f99e47a399d120839177e77ac861896`. Fork changes are maintained here and
are never submitted to upstream for merging. Original licenses and attribution remain.

The first goal is to establish the existing Lua APIs and functionality. Luau,
the object/service facade and villager trade inspection are planned; they are not
implemented. The VM will be developed or forked in a separate repository.

Start with [the roadmap](docs/Roadmap.md), [existing APIs](docs/ExistingApi.md),
[agent instructions](AGENTS.md), [project context](AIContext.md), and
[invariants](docs/Invariants.md). Native/binary release qualification is pending.
This is a replacement fork retaining the `computercraft` identity; do not install
it alongside stock CC: Tweaked. No fork binaries have been released.

## Upstream project and attribution

The following describes the original CC: Tweaked project. Download links and
dependency coordinates below refer to upstream, not a CCLuau release.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./doc/logo-darkmode.png">
  <source media="(prefers-color-scheme: light)" srcset="./doc/logo.png">
  <img alt="CC: Tweaked" src="./doc/logo.png">
</picture>

[![Upstream build status](https://github.com/cc-tweaked/CC-Tweaked/workflows/Build/badge.svg)](https://github.com/cc-tweaked/CC-Tweaked/actions "Upstream build status; does not qualify this fork")
[![Download CC: Tweaked on Modrinth](https://img.shields.io/static/v1?label=Download&color=00AF5C&logoColor=00AF5C&logo=Modrinth&message=CC:%20Tweaked)][Modrinth]

CC: Tweaked is a mod for Minecraft which adds programmable computers, turtles and more to the game. A fork of the
much-beloved [ComputerCraft], it continues its legacy with improved performance and stability, along with a wealth of
new features.

CC: Tweaked can be installed from [Modrinth]. It runs on both [Minecraft Forge] and [Fabric].

## Contributing
Any contribution is welcome, be that using the mod, reporting bugs or contributing code. If you want to get started
developing this fork, [check out the fork instructions](CONTRIBUTING.md).

## Community
If you need help getting started with CC: Tweaked, want to show off your latest project, or just want to chat about
ComputerCraft, do check out our [GitHub discussions page][GitHub discussions]! There's also a fairly populated,
albeit quiet IRC channel on [EsperNet], if that's more your cup of tea. You can join `#computercraft` through your
desktop client, or online using [KiwiIRC].

We also host fairly comprehensive documentation at [tweaked.cc](https://tweaked.cc/ "The CC: Tweaked website").

## Using
CC: Tweaked is hosted on my maven repo, and so is relatively simple to depend on. You may wish to add a soft (or hard)
dependency in your `mods.toml` file, with the appropriate version bounds, to ensure that API functionality you depend
on is present.

```groovy
repositories {
  maven {
    url "https://maven.squiddev.cc"
    content {
      includeGroup("cc.tweaked")
    }
  }
}

dependencies {
  // Vanilla (i.e. for multi-loader systems)
  compileOnly("cc.tweaked:cc-tweaked-$mcVersion-common-api:$cctVersion")

  // Forge Gradle
  compileOnly("cc.tweaked:cc-tweaked-$mcVersion-forge-api:$cctVersion")
  runtimeOnly("cc.tweaked:cc-tweaked-$mcVersion-forge:$cctVersion")

  // Fabric Loom
  modCompileOnly("cc.tweaked:cc-tweaked-$mcVersion-fabric-api:$cctVersion")
  modRuntimeOnly("cc.tweaked:cc-tweaked-$mcVersion-fabric:$cctVersion")
}
```

You should also be careful to only use classes within the `dan200.computercraft.api` package. Non-API classes are
subject to change at any point. If you depend on functionality outside the API (or need to mixin to CC:T), please file
an issue to let me know!

We bundle the API sources with the jar, so documentation should be easily viewable within your editor. Alternatively,
the generated documentation [can be browsed online](https://tweaked.cc/javadoc/).

[computercraft]: https://github.com/dan200/ComputerCraft "ComputerCraft on GitHub"
[modrinth]: https://modrinth.com/mod/gu7yAYhd "Download CC: Tweaked from Modrinth"
[Minecraft Forge]: https://files.minecraftforge.net/ "Download Minecraft Forge."
[Fabric]: https://fabricmc.net/use/installer/ "Download Fabric."
[GitHub Discussions]: https://github.com/cc-tweaked/CC-Tweaked/discussions
[EsperNet]: https://www.esper.net/
[KiwiIRC]: https://kiwiirc.com/nextclient/#irc://irc.esper.net:+6697/#computercraft "#computercraft on EsperNet"
