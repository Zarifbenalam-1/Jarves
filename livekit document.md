LiveKit Docs › Integration guides › Overview

---

# LiveKit Agents integrations

> Guides for integrating supported AI providers into LiveKit Agents.

## Overview

LiveKit Agents includes support for a wide variety of AI providers, from the largest research companies to emerging startups.

The open source plugin interface makes it easy to adopt the best AI providers for your app, without needing customized code for each.

## Installing plugins

Each provider is available as a separate plugin package, included as an optional dependency on the base SDK for Python.

For example, to install the SDK with the Cartesia, Deepgram, and OpenAI plugins, run the following command:

```shell
pip install "livekit-agents[cartesia,deepgram,openai]~=1.0"

```

You may also install plugins as individual packages. For example, this is equivalent to the previous command:

```shell
pip install \
  "livekit-agents~=1.0" \
  "livekit-plugins-cartesia~=1.0" \
  "livekit-plugins-deepgram~=1.0" \
  "livekit-plugins-openai~=1.0"

```

## Using plugins

The AgentSession class accepts plugins as arguments using a standard interface. Each plugin loads its own associated API key from environment variables. For instance, the following code creates an AgentSession that uses the OpenAI, Cartesia, and Deepgram plugins installed in the preceding section:

** Filename: `agent.py`**

```python
from livekit.plugins import openai, cartesia, deepgram

session = AgentSession(
    llm=openai.LLM(model="gpt-4o"),
    tts=cartesia.TTS(model="sonic-english"),
    stt=deepgram.STT(model="nova-2"),
)  

```

** Filename: `.env`**

```shell
OPENAI_API_KEY=<your-openai-api-key>
DEEPGRAM_API_KEY=<your-deepgram-api-key>
CARTESIA_API_KEY=<your-cartesia-api-key>

```

## OpenAI API compatibility

Many providers have standardized around the OpenAI API format for chat completions and more. The LiveKit Agents OpenAI plugin provides easy compatibility with many of these providers through special methods which load the correct API key from environment variables. For instance, to use Cerebras instead of OpenAI, you can use the following code:

** Filename: `agent.py`**

```python
from livekit.plugins import openai

session = AgentSession(
    llm=openai.LLM.with_cerebras(model="llama-3.1-70b-versatile"),
    # ... stt, tts, etc ..
)  

```

** Filename: `.env`**

```shell
CEREBRAS_API_KEY=<your-cerebras-api-key>
# ... other api keys ...

```

## Core plugins

The following are the core plugin types used in LiveKit Agents, to handle the primary voice AI tasks. Many providers are available for most functions.

- **[Realtime models](https://docs.livekit.io/agents/integrations/realtime.md)**: Plugins for multimodal speech-to-speech models like the OpenAI Realtime API.

- **[Large language models (LLM)](https://docs.livekit.io/agents/integrations/llm.md)**: Plugins for AI models from OpenAI, Anthropic, and more.

- **[Speech-to-text (STT)](https://docs.livekit.io/agents/integrations/stt.md)**: Plugins for speech-to-text solutions like Deepgram, Whisper, and more.

- **[Text-to-speech (TTS)](https://docs.livekit.io/agents/integrations/tts.md)**: Plugins for text-to-speech solutions like Cartesia, ElevenLabs, and more.

## Additional plugins

LiveKit Agents also includes the following additional specialized plugins, which are recommended for most voice AI use cases. Each runs locally and requires no additional API keys.

- **[Silero VAD](https://docs.livekit.io/agents/build/turns/vad.md)**: Voice activity detection with Silero VAD.

- **[LiveKit turn detector](https://docs.livekit.io/agents/build/turns/turn-detector.md)**: A custom LiveKit model for improved end-of-turn detection.

- **[Enhanced noise cancellation](https://pypi.org/project/livekit-plugins-noise-cancellation/)**: LiveKit Cloud enhanced noise cancellation to improve voice AI performance.

## Build your own plugin

The LiveKit Agents plugin framework is extensible and community-driven. Your plugin can integrate with new providers or directly load models for local inference. LiveKit especially welcomes new TTS, STT, and LLM plugins.

To learn more, see the guidelines for contributions to the [Python](https://github.com/livekit/agents/blob/main/CONTRIBUTING.md) and [Node.js](https://github.com/livekit/agents-js/blob/main/CONTRIBUTING.md) SDKs.

---

This document was rendered at 2025-06-26T16:06:29.917Z.
For the latest version of this document, see [https://docs.livekit.io/agents/integrations.md](https://docs.livekit.io/agents/integrations.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).LiveKit Docs › Deployment & operations › Deploying to production

---

# Deploying to production

> Guide to running LiveKit Agents in a production environment.

## Overview

LiveKit Agents use a worker pool model suited to a container orchestration system like Kubernetes. Each worker — an instance of `python agent.py start` — registers with LiveKit server. LiveKit server balances job dispatch across available workers. The workers themselves spawn a new sub-process for each job, and that job is where your code and agent participant run.

Deploying to production generally requires a simple `Dockerfile` that ends in `CMD ["python", "agent.py", "start"]` and a deployment platform that scales your worker pool based on load.

![Diagram illustrating the LiveKit Agents worker pool with LiveKit server](/images/agents/agents-orchestration.svg)

## Where to deploy

LiveKit Agents can be deployed anywhere. The recommended approach is to use `Docker` and deploy to an orchestration service. The LiveKit team and community have found the following deployment platforms to be the easiest to deploy and autoscale workers.

- **[LiveKit Cloud Agents Beta](https://livekit.io/cloud-agents-beta)**: Run your agent on the same network and infrastructure that serves LiveKit Cloud, with builds, deployment, and scaling handled for you. Sign up for the public beta to get started.

- **[Kubernetes](https://github.com/livekit-examples/agent-deployment/tree/main/kubernetes)**: Sample configuration for deploying and autoscaling LiveKit Agents on Kubernetes.

- **[Render.com](https://github.com/livekit-examples/agent-deployment/tree/main/render.com)**: Sample configuration for deploying and autoscaling LiveKit Agents on Render.com.

- **[More deployment examples](https://github.com/livekit-examples/agent-deployment)**: Example `Dockerfile` and configuration files for a variety of deployment platforms.

## Networking

Workers use a WebSocket connection to register with LiveKit server and accept incoming jobs. This means that workers do not need to expose any inbound hosts or ports to the public internet.

You may optionally expose a private health check endpoint for monitoring, but this is not required for normal operation. The default health check server listens on `http://0.0.0.0:8081/`.

## Environment variables

It is best to configure your worker with environment variables for secrets like API keys. In addition to the LiveKit variables, you are likely to need additional keys for external services your agent depends on.

For instance, an agent built with the [Voice AI quickstart](https://docs.livekit.io/agents/start/voice-ai.md) needs the following keys at a minimum:

** Filename: `.env`**

```shell
DEEPGRAM_API_KEY=<Your Deepgram API Key>
OPENAI_API_KEY=<Your OpenAI API Key>
CARTESIA_API_KEY=<Your Cartesia API Key>
LIVEKIT_API_KEY=%{apiKey}%
LIVEKIT_API_SECRET=%{apiSecret}%
LIVEKIT_URL=%{wsURL}%

```

> ❗ **Project environments**
> 
> It's recommended to use a separate LiveKit instance for staging, production, and development environments. This ensures you can continue working on your agent locally without accidentally processing real user traffic.
> 
> In LiveKit Cloud, make a separate project for each environment. Each has a unique URL, API key, and secret.
> 
> For self-hosted LiveKit server, use a separate deployment for staging and production and a local server for development.

## Storage

Worker and job processes have no particular storage requirements beyond the size of the Docker image itself (typically <1GB). 10GB of ephemeral storage should be more than enough to account for this and any temporary storage needs your app has.

## Memory and CPU

Memory and CPU requirements vary significantly based on the specific details of your app. For instance, agents that apply [enhanced noise cancellation](https://docs.livekit.io/cloud/noise-cancellation.md) require more CPU and memory than those that don't.

LiveKit recommends 4 cores and 8GB of memory for every 25 concurrent sessions as a starting rule for most voice-to-voice apps.

> ℹ️ **Real world load test results**
> 
> LiveKit ran a load test to evaluate the memory and CPU requirements of a typical voice-to-voice app.
> 
> - 30 agents each placed in their own LiveKit Cloud room.
> - 30 simulated user participants, one in each room.
> - Each simulated participant published looping speech audio to the agents.
> - Each agent subscribed to the incoming audio of the user and ran the Silero VAD plugin.
> - Each agent published their own audio (simple looping sine wave).
> - One additional user participant with a corresponding voice AI agent to ensure subjective quality of service.
> 
> This test ran all agents on a single 4-Core, 8GB machine. This machine reached peak usage of:
> 
> - CPU: ~3.8 cores utilized
> - Memory: ~2.8GB used

## Rollout

Workers stop accepting jobs upon `SIGINT` or `SIGTERM`. Any job still running on the worker continues to run to completion. It's important that you configure a large enough grace period such that your jobs can finish without interrupting the user experience.

Voice AI apps might require a 10+ minute grace period to allow for conversations to finish.

Different deployment platforms have different ways of setting this grace period. In Kubernetes, it's the `terminationGracePeriodSeconds` field in the pod spec.

Consult your deployment platform's documentation for more information.

## Load balancing

LiveKit server includes a built-in balanced job distribution system. This system peforms round-robin distribution with a single-assignment principle that ensures each job is assigned to only one worker. If a worker fails to accept the job within a predetermined timeout period, the job is sent to another available worker instead.

LiveKit Cloud additionally exercises geographic affinity to prioritize matching users and workers that are geographically closest to each other. This ensures the lowest possible latency between users and agents.

## Worker availability

Worker availability is defined by the `load_fnc` and `load_threshold` parameters in the `WorkerOptions` configuration.

The `load_fnc` must return a value between 0 and 1, indicating how busy the worker is. `load_threshold` is the load value above which the worker stops accepting new jobs.

The default `load_fnc` is overall CPU utilization, and the default `load_threshold` is `0.75`.

## Autoscaling

To handle variable traffic patterns, add an autoscaling strategy to your deployment platform. Your autoscaler should use the same underlying metrics as your `load_fnc` (the default is CPU utilization) but should scale up at a _lower_ threshold than your worker's `load_threshold`. This ensures continuity of service by adding new workers before existing ones go out of service. For example, if your `load_threshold` is `0.75`, you should scale up at `0.50`.

Since voice agents are typically long running tasks (relative to typical web requests), rapid increases in load are more likely to be sustained. In technical terms: spikes are less spikey. For your autoscaling configuration, you should consider _reducing_ cooldown/stabilization periods when scaling up. When scaling down, consider _increasing_ cooldown/stabilization periods because workers take time to drain.

For example, if deploying on Kubernetes using a Horizontal Pod Autoscaler, see [stabilizationWindowSeconds](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#default-behavior).

---

This document was rendered at 2025-06-26T16:06:25.753Z.
For the latest version of this document, see [https://docs.livekit.io/agents/ops/deployment.md](https://docs.livekit.io/agents/ops/deployment.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).LiveKit Docs › Building voice agents › Overview

---

# Building voice agents

> In-depth guide to voice AI with LiveKit Agents.

## Overview

Building a great voice AI app requires careful orchestration of multiple components. LiveKit Agents is built on top of the [Realtime SDK](https://github.com/livekit/python-sdks) to provide dedicated abstractions that simplify development while giving you full control over the underlying code.

## Agent sessions

The `AgentSession` is the main orchestrator for your voice AI app. The session is responsible for collecting user input, managing the voice pipeline, invoking the LLM, and sending the output back to the user.

Each session requires at least one `Agent` to orchestrate. The agent is responsible for defining the core AI logic - instructions, tools, etc - of your app. The framework supports the design of custom [workflows](https://docs.livekit.io/agents/build/workflows.md) to orchestrate handoff and delegation between multiple agents.

The following example shows how to begin a simple single-agent session:

```python
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, cartesia, deepgram, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

session = AgentSession(
    stt=deepgram.STT(),
    llm=openai.LLM(),
    tts=cartesia.TTS(),
    vad=silero.VAD.load(),
    turn_detection=turn_detector.MultilingualModel(),
)

await session.start(
    room=ctx.room,
    agent=Agent(instructions="You are a helpful voice AI assistant."),
    room_input_options=RoomInputOptions(
        noise_cancellation=noise_cancellation.BVC(),
    ),
)

```

### RoomIO

Communication between agent and user participants happens using media streams, also known as tracks. For voice AI apps, this is primarily audio, but can include vision. By default, track management is handled by `RoomIO`, a utility class that serves as a bridge between the agent session and the LiveKit room. When an AgentSession is initiated, it automatically creates a `RoomIO` object that enables all room participants to subscribe to available audio tracks.

To learn more about publishing audio and video, see the following topics:

- **[Agent speech and audio](https://docs.livekit.io/agents/build/audio.md)**: Add speech, audio, and background audio to your agent.

- **[Vision](https://docs.livekit.io/agents/build/vision.md)**: Give your agent the ability to see images and live video.

- **[Text and transcription](https://docs.livekit.io/agents/build/text.md)**: Send and receive text messages and transcription to and from your agent.

- **[Realtime media](https://docs.livekit.io/home/client/tracks.md)**: Tracks are a core LiveKit concept. Learn more about publishing and subscribing to media.

- **[Camera and microphone](https://docs.livekit.io/home/client/tracks/publish.md)**: Use the LiveKit SDKs to publish audio and video tracks from your user's device.

#### Custom RoomIO

For greater control over media sharing in a room,  you can create a custom `RoomIO` object. For example, you might want to manually control which input and output devices are used, or to control which participants an agent listens to or responds to.

To replace the default one created in `AgentSession`, create a `RoomIO` object in your entrypoint function and pass it an instance of the `AgentSession` in the constructor. For examples, see the following in the GitHub repository:

- **[Toggling audio](https://github.com/livekit/agents/blob/main/examples/voice_agents/push_to_talk.py)**: Create a push-to-talk interface to toggle audio input and output.

- **[Toggling input and output](https://github.com/livekit/agents/blob/main/examples/voice_agents/toggle_io.py)**: Toggle both audio and text input and output.

## Voice AI providers

You can choose from a variety of providers for each part of the voice pipeline to fit your needs. The framework supports both high-performance STT-LLM-TTS pipelines and speech-to-speech models. In either case, it automatically manages interruptions, transcription forwarding, turn detection, and more.

You may add these components to the `AgentSession`, where they act as global defaults within the app, or to each individual `Agent` if needed.

- **[TTS](https://docs.livekit.io/agents/integrations/tts.md)**: Text-to-speech integrations

- **[STT](https://docs.livekit.io/agents/integrations/stt.md)**: Speech-to-text integrations

- **[LLM](https://docs.livekit.io/agents/integrations/llm.md)**: Language model integrations

- **[Multimodal](https://docs.livekit.io/agents/integrations/realtime.md)**: Realtime multimodal APIs

## Capabilities

The following guides, in addition to others in this section, cover the core capabilities of the `AgentSession` and how to leverage them in your app.

- **[Workflows](https://docs.livekit.io/agents/build/workflows.md)**: Orchestrate complex tasks among multiple agents.

- **[Tool definition & use](https://docs.livekit.io/agents/build/tools.md)**: Use tools to call external services, inject custom logic, and more.

- **[Pipeline nodes](https://docs.livekit.io/agents/build/nodes.md)**: Add custom behavior to any component of the voice pipeline.

---

This document was rendered at 2025-06-26T16:06:20.037Z.
For the latest version of this document, see [https://docs.livekit.io/agents/build.md](https://docs.livekit.io/agents/build.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).LiveKit Docs › Getting started › Voice AI quickstart

---

# Voice AI quickstart

> Build a simple voice assistant with Python in less than 10 minutes.

## Overview

This guide walks you through the setup of your very first voice assistant using LiveKit Agents for Python. In less than 10 minutes, you'll have a voice assistant that you can speak to in your terminal, browser, telephone, or native app.

## Requirements

The following sections describe the minimum requirements to get started with LiveKit Agents.

### Python

LiveKit Agents requires Python 3.9 or later.

> ℹ️ **Looking for Node.js?**
> 
> The Node.js beta is still in development and has not yet reached v1.0. See the [v0.x documentation](https://docs.livekit.io/agents/v0.md) for Node.js reference and join the [LiveKit Community Slack](https://livekit.io/join-slack) to be the first to know when the next release is available.

### LiveKit server

You need a LiveKit server instance to transport realtime media between user and agent. The easiest way to get started is with a free [LiveKit Cloud](https://cloud.livekit.io/) account. Create a project and use the API keys in the following steps. You may also [self-host LiveKit](https://docs.livekit.io/home/self-hosting/local.md) if you prefer.

### AI providers

LiveKit Agents [integrates with most AI model providers](https://docs.livekit.io/agents/integrations.md) and supports both high-performance STT-LLM-TTS voice pipelines, as well as lifelike multimodal models.

The rest of this guide assumes you use one of the following two starter packs, which provide the best combination of value, features, and ease of setup.

**STT-LLM-TTS pipeline**:

Your agent strings together three specialized providers into a high-performance voice pipeline. You need accounts and API keys for each.

![Diagram showing STT-LLM-TTS pipeline.](/images/agents/stt-llm-tts-pipeline.svg)

| Component | Provider | Required Key | Alternatives |
| STT | [Deepgram](https://deepgram.com/) | `DEEPGRAM_API_KEY` | [STT integrations](https://docs.livekit.io/agents/integrations/stt.md#providers) |
| LLM | [OpenAI](https://platform.openai.com/) | `OPENAI_API_KEY` | [LLM integrations](https://docs.livekit.io/agents/integrations/llm.md#providers) |
| TTS | [Cartesia](https://cartesia.ai) | `CARTESIA_API_KEY` | [TTS integrations](https://docs.livekit.io/agents/integrations/tts.md#providers) |

---

**Realtime model**:

Your agent uses a single realtime model to provide an expressive and lifelike voice experience.

![Diagram showing realtime model.](/images/agents/realtime-model.svg)

| Component | Provider | Required Key | Alternatives |
| Realtime model | [OpenAI](https://platform.openai.com/docs/guides/realtime) | `OPENAI_API_KEY` | [Realtime models](https://docs.livekit.io/agents/integrations/realtime.md#providers) |

## Setup

Use the instructions in the following sections to set up your new project.

### Packages

> ℹ️ **Noise cancellation**
> 
> This example integrates LiveKit Cloud [enhanced background voice/noise cancellation](https://docs.livekit.io/home/cloud/noise-cancellation.md), powered by Krisp.
> 
> If you're not using LiveKit Cloud, omit the plugin and the `noise_cancellation` parameter from the following code.
> 
> For telephony applications, use the `BVCTelephony` model for the best results.

**STT-LLM-TTS pipeline**:

Install the following packages to build a complete voice AI agent with your STT-LLM-TTS pipeline, noise cancellation, and [turn detection](https://docs.livekit.io/agents/build/turns.md):

```shell
pip install \
  "livekit-agents[deepgram,openai,cartesia,silero,turn-detector]~=1.0" \
  "livekit-plugins-noise-cancellation~=0.2" \
  "python-dotenv"

```

---

**Realtime model**:

Install the following packages to build a complete voice AI agent with your realtime model and noise cancellation.

```shell
pip install \
  "livekit-agents[openai]~=1.0" \
  "livekit-plugins-noise-cancellation~=0.2" \
  "python-dotenv"

```

### Environment variables

Create a file named `.env` and add your LiveKit credentials along with the necessary API keys for your AI providers.

**STT-LLM-TTS pipeline**:

** Filename: `.env`**

```shell
DEEPGRAM_API_KEY=<Your Deepgram API Key>
OPENAI_API_KEY=<Your OpenAI API Key>
CARTESIA_API_KEY=<Your Cartesia API Key>
LIVEKIT_API_KEY=%{apiKey}%
LIVEKIT_API_SECRET=%{apiSecret}%
LIVEKIT_URL=%{wsURL}%

```

---

**Realtime model**:

** Filename: `.env`**

```shell
OPENAI_API_KEY=<Your OpenAI API Key>
LIVEKIT_API_KEY=%{apiKey}%
LIVEKIT_API_SECRET=%{apiSecret}%
LIVEKIT_URL=%{wsURL}%

```

### Agent code

Create a file named `agent.py` containing the following code for your first voice agent.

**STT-LLM-TTS pipeline**:

** Filename: `agent.py`**

```python
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))


```

---

**Realtime model**:

** Filename: `agent.py`**

```python
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
)

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="coral"
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))


```

## Download model files

To use the `turn-detector`, `silero`, or `noise-cancellation` plugins, you first need to download the model files:

```shell
python agent.py download-files

```

## Speak to your agent

Start your agent in `console` mode to run inside your terminal:

```shell
python agent.py console

```

Your agent speaks to you in the terminal, and you can speak to it as well.

![Screenshot of the CLI console mode.](/images/agents/start/cli-console.png)

## Connect to playground

Start your agent in `dev` mode to connect it to LiveKit and make it available from anywhere on the internet:

```shell
python agent.py dev

```

Use the [Agents playground](https://docs.livekit.io/agents/start/playground.md) to speak with your agent and explore its full range of multimodal capabilities.

Congratulations, your agent is up and running. Continue to use the playground or the `console` mode as you build and test your agent.

> 💡 **Agent CLI modes**
> 
> In the `console` mode, the agent runs locally and is only available within your terminal.
> 
> Run your agent in `dev` (development / debug) or `start` (production) mode to connect to LiveKit and join rooms.

## Next steps

Follow these guides bring your voice AI app to life in the real world.

- **[Web and mobile frontends](https://docs.livekit.io/agents/start/frontend.md)**: Put your agent in your pocket with a custom web or mobile app.

- **[Telephony integration](https://docs.livekit.io/agents/start/telephony.md)**: Your agent can place and receive calls with LiveKit's SIP integration.

- **[Building voice agents](https://docs.livekit.io/agents/build.md)**: Comprehensive documentation to build advanced voice AI apps with LiveKit.

- **[Worker lifecycle](https://docs.livekit.io/agents/worker.md)**: Learn how to manage your agents with workers and jobs.

- **[Deploying to production](https://docs.livekit.io/agents/ops/deployment.md)**: Guide to deploying your voice agent in a production environment.

- **[Integration guides](https://docs.livekit.io/agents/integrations.md)**: Explore the full list of AI providers available for LiveKit Agents.

- **[Recipes](https://docs.livekit.io/recipes.md)**: A comprehensive collection of examples, guides, and recipes for LiveKit Agents.

---

This document was rendered at 2025-06-26T16:06:02.130Z.
For the latest version of this document, see [https://docs.livekit.io/agents/start/voice-ai.md](https://docs.livekit.io/agents/start/voice-ai.md).

To explore all LiveKit documentation, see [llms.txt](https://docs.livekit.io/llms.txt).