<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

<p align="center"><i>Xircuits Component Library for Twilio! Integrate Twilio services seamlessly into your workflows.</i></p>

---

### Xircuits Component Library for Twilio

A Xircuits component library for integrating Twilio services into your workflows. This library provides components for SMS, WhatsApp messaging, voice calls, and TwiML generation.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Example Use Cases](#example-use-cases)
- [Usage Tips](#usage-tips)
- [Installation](#installation)


## Prerequisites

Before you begin, you will need the following:

1. Python3.9+.
2. Xircuits.
3. Twilio account credentials:
   - Account SID
   - Auth Token

You can provide credentials either as environment variables (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`) or directly within the components.

## Main Xircuits Components

### Authentication
- **TwilioAuth**: Initializes a Twilio client using provided credentials.



### Messaging
- **TwilioSendSMS**: Sends an SMS message.

   <img src="https://github.com/user-attachments/assets/85e148b7-4826-4674-a82c-f64a74833501" alt="Image" width="200" height="150" />

- **TwilioSendWhatsApp**: Sends a WhatsApp message.

   <img src="https://github.com/user-attachments/assets/4ac142c2-c804-424d-b790-bd3755a8a695" alt="Image" width="200" height="100" />

- **TwilioGetMessageStatus**: Retrieves the status of a sent message.
- **TwilioListMessages**: Lists message history.

### Voice Calls
- **TwilioMakeCall**: Initiates a voice call.
- **TwilioGetCallStatus**: Checks the status of a call.

### TwiML Generation
Create TwiML response instructions for interactive voice and messaging automation:
- **TwilioMakeTwiMLSay**: Converts text to speech.
- **TwilioMakeTwiMLPlay**: Plays an audio file.
- **TwilioMakeTwiMLDial**: Forwards a call.
- **TwilioMakeTwiMLGather**: Collects user input via voice.
- **TwilioMakeTwiMLMessage**: Creates messaging responses.

## Example Use Cases

### Automated SMS Notifications
- Uses `TwilioAuth` and `TwilioSendSMS` to send automated text messages.

### Interactive Voice Response (IVR)
- Combines TwiML components with `TwilioMakeCall` to create interactive voice menus.

### WhatsApp Business Messaging
- Use `TwilioSendWhatsApp` for WhatsApp business messaging

### Agentic Phone Number
- Integrates with Xircuits Flask components to create an AI-powered phone number that can:
  - Respond to messages.
  - Make automated calls.
  - Handle voice interactions.
  - Process user input.

## Usage Tips

- Always initialize TwilioAuth first in your workflow
- Use environment variables for secure credential management
- Monitor message and call status with the respective status components
- Combine with other Xircuits libraries for advanced automation

## Installation

To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install the Twilio library using the [component library interface](https://xircuits.io/docs/component-library/installation#installation-using-the-xircuits-library-interface), or through the CLI using:

```
xircuits install twilio
```

You can also install it manually by cloning the repository:

```
# base Xircuits directory

git clone https://github.com/XpressAI/xai-twilio xai_components/xai_twilio
pip install -r xai_components/xai_twilio/requirements.txt
```

