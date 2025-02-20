# xai-twilio

A Xircuits component library for integrating Twilio services into your workflows. This library provides components for SMS, WhatsApp messaging, voice calls, and TwiML generation.

## Installation

Install this component library in Xircuits:

```bash
xircuits install xai-twilio
```

## Requirements

- Xircuits
- Twilio account credentials:
  - Account SID
  - Auth Token

You can provide credentials either through environment variables (`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`) or directly in the components.

## Available Components

### Authentication
- **TwilioAuth**: Initialize a Twilio client with your credentials

### Messaging
- **TwilioSendSMS**: Send SMS messages
- **TwilioSendWhatsApp**: Send WhatsApp messages
- **TwilioGetMessageStatus**: Check message delivery status
- **TwilioListMessages**: Retrieve message history

### Voice Calls
- **TwilioMakeCall**: Initiate phone calls
- **TwilioGetCallStatus**: Check call status

### TwiML Generation
Create voice and messaging response instructions:
- **TwilioMakeTwiMLSay**: Generate TwiML for text-to-speech
- **TwilioMakeTwiMLPlay**: Generate TwiML to play audio files
- **TwilioMakeTwiMLDial**: Generate TwiML for call forwarding
- **TwilioMakeTwiMLGather**: Generate TwiML to collect user input
- **TwilioMakeTwiMLMessage**: Generate TwiML for messaging responses

## Example Use Cases

1. **Automated SMS Notifications**
   - Use TwilioAuth and TwilioSendSMS to send automated messages

2. **Interactive Voice Response (IVR)**
   - Combine TwiML components with TwilioMakeCall for custom voice menus

3. **WhatsApp Business Integration**
   - Use TwilioSendWhatsApp for WhatsApp business messaging

4. **Agentic Phone Number**
   - Combine with the Xircuits Flask component library to create an AI-powered phone number that can:
     - Respond to incoming messages
     - Make automated calls
     - Handle voice interactions
     - Process user input

## Usage Tips

- Always initialize TwilioAuth first in your workflow
- Use environment variables for secure credential management
- Monitor message and call status with the respective status components
- Combine with other Xircuits libraries for advanced automation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

