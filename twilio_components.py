from xai_components.base import InArg, InCompArg, OutArg, Component, xai_component
from typing import Optional, Any
import os
from twilio.rest import Client

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
