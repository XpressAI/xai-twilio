from xai_components.base import InArg, InCompArg, OutArg, Component, xai_component
from typing import Optional, Any, List
import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.twiml.messaging_response import MessagingResponse

def get_twilio_client(account_sid=None, auth_token=None):
    """Get Twilio client from provided credentials or environment variables.
    
    Args:
        account_sid: Optional Twilio account SID
        auth_token: Optional Twilio auth token
        
    Returns:
        Twilio client object
    """
    # Use provided credentials if available
    if account_sid and auth_token:
        return Client(account_sid, auth_token)
    
    # Fall back to environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        raise EnvironmentError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables must be set")
    
    return Client(account_sid, auth_token)

@xai_component
class TwilioAuth(Component):
    """A component to authenticate with Twilio API and generate a client object.
    
    Uses credentials from either:
    1. The provided account_sid and auth_token
    2. TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables

    ##### inPorts:
    - account_sid: Optional Twilio account SID
    - auth_token: Optional Twilio auth token

    ##### outPorts:
    - client: A Twilio client object
    """
    account_sid: InArg[str]  # Optional Twilio account SID
    auth_token: InArg[str]  # Optional Twilio auth token
    client: OutArg[any]  # The Twilio client

    def execute(self, ctx) -> None:
        self.client.value = get_twilio_client(
            self.account_sid.value if self.account_sid else None,
            self.auth_token.value if self.auth_token else None
        )

@xai_component
class TwilioSendSMS(Component):
    """Sends an SMS message using Twilio.

    ##### inPorts:
    - client: Optional Twilio client from TwilioAuth
    - from_number: The Twilio phone number to send from
    - to_number: The recipient's phone number
    - message: The message content
    
    ##### outPorts:
    - message_sid: The SID of the sent message
    """
    client: InArg[any]  # Optional Twilio client
    from_number: InCompArg[str]  # Sender phone number
    to_number: InCompArg[str]  # Recipient phone number
    message: InCompArg[str]  # Message content
    message_sid: OutArg[str]  # The sent message SID

    def execute(self, ctx) -> None:
        client = self.client.value if self.client else get_twilio_client()
        message = client.messages.create(
            body=self.message.value,
            from_=self.from_number.value,
            to=self.to_number.value
        )
        self.message_sid.value = message.sid

@xai_component
class TwilioSendWhatsApp(Component):
    """Sends a WhatsApp message using Twilio.

    ##### inPorts:
    - client: Optional Twilio client from TwilioAuth
    - from_number: The Twilio WhatsApp number (format: whatsapp:+1234567890)
    - to_number: The recipient's WhatsApp number (format: whatsapp:+1234567890)
    - message: The message content
    
    ##### outPorts:
    - message_sid: The SID of the sent message
    """
    client: InArg[any]  # Optional Twilio client
    from_number: InCompArg[str]  # Sender WhatsApp number
    to_number: InCompArg[str]  # Recipient WhatsApp number
    message: InCompArg[str]  # Message content
    message_sid: OutArg[str]  # The sent message SID

    def execute(self, ctx) -> None:
        client = self.client.value if self.client else get_twilio_client()
        message = client.messages.create(
            body=self.message.value,
            from_=self.from_number.value,
            to=self.to_number.value
        )
        self.message_sid.value = message.sid

@xai_component
class TwilioMakeCall(Component):
    """Makes a phone call using Twilio.

    ##### inPorts:
    - client: Optional Twilio client from TwilioAuth
    - from_number: The Twilio phone number to call from
    - to_number: The recipient's phone number
    - twiml_url: URL to TwiML instructions for the call
    
    ##### outPorts:
    - call_sid: The SID of the initiated call
    """
    client: InArg[any]  # Optional Twilio client
    from_number: InCompArg[str]  # Caller phone number
    to_number: InCompArg[str]  # Recipient phone number
    twiml_url: InCompArg[str]  # URL to TwiML instructions
    call_sid: OutArg[str]  # The call SID

    def execute(self, ctx) -> None:
        client = self.client.value if self.client else get_twilio_client()
        call = client.calls.create(
            url=self.twiml_url.value,
            to=self.to_number.value,
            from_=self.from_number.value
        )
        self.call_sid.value = call.sid

@xai_component
class TwilioGetMessageStatus(Component):
    """Retrieves the status of a sent message.

    ##### inPorts:
    - client: Optional Twilio client from TwilioAuth
    - message_sid: The SID of the message to check
    
    ##### outPorts:
    - status: The message status
    """
    client: InArg[any]  # Optional Twilio client
    message_sid: InCompArg[str]  # Message SID to check
    status: OutArg[str]  # Message status

    def execute(self, ctx) -> None:
        client = self.client.value if self.client else get_twilio_client()
        message = client.messages(self.message_sid.value).fetch()
        self.status.value = message.status

@xai_component
class TwilioGetCallStatus(Component):
    """Retrieves the status of a call.

    ##### inPorts:
    - client: Optional Twilio client from TwilioAuth
    - call_sid: The SID of the call to check
    
    ##### outPorts:
    - status: The call status
    """
    client: InArg[any]  # Optional Twilio client
    call_sid: InCompArg[str]  # Call SID to check
    status: OutArg[str]  # Call status

    def execute(self, ctx) -> None:
        client = self.client.value if self.client else get_twilio_client()
        call = client.calls(self.call_sid.value).fetch()
        self.status.value = call.status

@xai_component
class TwilioListMessages(Component):
    """Lists messages from your Twilio account.

    ##### inPorts:
    - client: Optional Twilio client from TwilioAuth
    - limit: Maximum number of messages to return
    
    ##### outPorts:
    - messages: List of message records
    """
    client: InArg[any]  # Optional Twilio client
    limit: InArg[int]  # Maximum number of messages
    messages: OutArg[list]  # List of messages

    def execute(self, ctx) -> None:
        client = self.client.value if self.client else get_twilio_client()
        messages = client.messages.list(limit=self.limit.value if self.limit else 50)
        self.messages.value = [
            {
                'sid': msg.sid,
                'from': msg.from_,
                'to': msg.to,
                'body': msg.body,
                'status': msg.status,
                'date_sent': str(msg.date_sent),
                'price': msg.price
            }
            for msg in messages
        ]

@xai_component
class TwilioMakeTwiMLSay(Component):
    """Creates TwiML to speak text during a call.

    ##### inPorts:
    - message: Text to speak
    - voice: Optional voice to use (man, woman, alice)
    - language: Optional language code (e.g. 'en-US')
    - loop: Optional number of times to repeat
    
    ##### outPorts:
    - twiml: Generated TwiML XML string
    """
    message: InCompArg[str]
    voice: InArg[str]
    language: InArg[str]
    loop: InArg[int]
    twiml: OutArg[str]

    def execute(self, ctx) -> None:
        response = VoiceResponse()
        say_kwargs = {}
        if self.voice.value:
            say_kwargs['voice'] = self.voice.value
        if self.language.value:
            say_kwargs['language'] = self.language.value
        if self.loop.value:
            say_kwargs['loop'] = self.loop.value
            
        response.say(self.message.value, **say_kwargs)
        self.twiml.value = str(response)

@xai_component
class TwilioMakeTwiMLPlay(Component):
    """Creates TwiML to play an audio file during a call.

    ##### inPorts:
    - url: URL of the audio file to play
    - loop: Optional number of times to repeat
    
    ##### outPorts:
    - twiml: Generated TwiML XML string
    """
    url: InCompArg[str]
    loop: InArg[int]
    twiml: OutArg[str]

    def execute(self, ctx) -> None:
        response = VoiceResponse()
        play_kwargs = {}
        if self.loop.value:
            play_kwargs['loop'] = self.loop.value
            
        response.play(self.url.value, **play_kwargs)
        self.twiml.value = str(response)

@xai_component
class TwilioMakeTwiMLDial(Component):
    """Creates TwiML to dial one or more numbers.

    ##### inPorts:
    - numbers: List of phone numbers to dial
    - timeout: Optional timeout in seconds
    - caller_id: Optional caller ID to use
    
    ##### outPorts:
    - twiml: Generated TwiML XML string
    """
    numbers: InCompArg[List[str]]
    timeout: InArg[int]
    caller_id: InArg[str]
    twiml: OutArg[str]

    def execute(self, ctx) -> None:
        response = VoiceResponse()
        dial_kwargs = {}
        if self.timeout.value:
            dial_kwargs['timeout'] = self.timeout.value
        if self.caller_id.value:
            dial_kwargs['caller_id'] = self.caller_id.value
            
        dial = Dial(**dial_kwargs)
        for number in self.numbers.value:
            dial.number(number)
            
        response.append(dial)
        self.twiml.value = str(response)

@xai_component
class TwilioMakeTwiMLGather(Component):
    """Creates TwiML to gather DTMF input during a call.

    ##### inPorts:
    - prompt: Text to speak before gathering input
    - num_digits: Number of digits to gather
    - timeout: Optional timeout in seconds
    - action_url: URL to send gathered digits to
    
    ##### outPorts:
    - twiml: Generated TwiML XML string
    """
    prompt: InCompArg[str]
    num_digits: InCompArg[int]
    timeout: InArg[int]
    action_url: InCompArg[str]
    twiml: OutArg[str]

    def execute(self, ctx) -> None:
        response = VoiceResponse()
        gather_kwargs = {
            'num_digits': self.num_digits.value,
            'action': self.action_url.value
        }
        if self.timeout.value:
            gather_kwargs['timeout'] = self.timeout.value
            
        gather = response.gather(**gather_kwargs)
        gather.say(self.prompt.value)
        self.twiml.value = str(response)

@xai_component
class TwilioMakeTwiMLMessage(Component):
    """Creates TwiML for messaging responses.

    ##### inPorts:
    - message: Text message to send
    - media_url: Optional URL to media to include
    
    ##### outPorts:
    - twiml: Generated TwiML XML string
    """
    message: InCompArg[str]
    media_url: InArg[str]
    twiml: OutArg[str]

    def execute(self, ctx) -> None:
        response = MessagingResponse()
        msg = response.message(self.message.value)
        if self.media_url.value:
            msg.media(self.media_url.value)
        self.twiml.value = str(response)

@xai_component
class TwilioMakeTwiMLSayAndRecord(Component):
    """Creates TwiML to speak text and record the response.

    ##### inPorts:
    - message: Text to speak before recording
    - max_length: Maximum recording length in seconds
    - timeout: Optional silence timeout in seconds
    - transcribe: Whether to transcribe the recording
    - transcribe_callback: Optional URL to send transcription to
    - action_url: URL to send recording data to
    
    ##### outPorts:
    - twiml: Generated TwiML XML string
    """
    message: InCompArg[str]
    max_length: InCompArg[int]
    timeout: InArg[int]
    transcribe: InArg[bool]
    transcribe_callback: InArg[str]
    action_url: InCompArg[str]
    twiml: OutArg[str]

    def execute(self, ctx) -> None:
        response = VoiceResponse()
        response.say(self.message.value)
        
        record_kwargs = {
            'maxLength': self.max_length.value,
            'action': self.action_url.value
        }
        
        if self.timeout.value:
            record_kwargs['timeout'] = self.timeout.value
        if self.transcribe.value:
            record_kwargs['transcribe'] = True
        if self.transcribe_callback.value:
            record_kwargs['transcribeCallback'] = self.transcribe_callback.value
            
        response.record(**record_kwargs)
        self.twiml.value = str(response)
