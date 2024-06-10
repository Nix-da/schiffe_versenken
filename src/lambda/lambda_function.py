import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model import Response

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Handler for skill launch
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech_text = "Willkommen zu Schiffe Versenken! Möchtest du im Bot Modus oder Multiplayer Modus spielen?"
        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )


# Handler for SetSpielmodusIntent
class SetSpielmodusIntentHandler(AbstractRequestHandler):
    """Handler for SetSpielmodusIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("SetSpielmodusIntent")(handler_input)

    def handle(self, handler_input):
        try:
            slots = handler_input.request_envelope.request.intent.slots
            if "spielMode" in slots and slots["spielMode"].value:
                spiel_mode = slots["spielMode"].value.lower()
                logger.info(f"Spielmodus received: {spiel_mode}")

                # Set the game mode in session attributes
                session_attributes = handler_input.attributes_manager.session_attributes
                session_attributes["spiel_mode"] = spiel_mode

                if spiel_mode == "multiplayer mode":
                    speech_text = "Du hast den Multiplayer Modus gewählt. Bitte sage mir zuerst deine IP-Adresse."
                else:  # Assuming bot mode
                    speech_text = "Du hast den Bot Modus gewählt. Nun kannst du deine Schiffe auf dem Spielfeld platzieren oder sag 'Schiffe zufällig platzieren', um die Schiffe per Zufall auf dem Spielfeld zu verteilen."

            else:
                speech_text = "Entschuldigung, ich habe den Spielmodus nicht verstanden. Bitte sage entweder Bot Modus oder Multiplayer Modus."

            return handler_input.response_builder.speak(speech_text).ask(speech_text).response

        except Exception as e:
            logger.error(f"Error handling SetSpielmodusIntent: {e}")
            return handler_input.response_builder.speak(
                "Entschuldigung, es gab einen Fehler bei der Verarbeitung, bitte versuche es nochmal.").response


# Handler for SpielNeustartIntent
class SpielNeustartIntentHandler(AbstractRequestHandler):
    """Handler for SpielNeustartIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("SpielNeustartIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Das Spiel wurde neu gestartet. Möchtest du im Bot Modus oder Multiplayer Modus spielen?"
        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )


# Handler for SetIpAdresseIntent
class SetIpAdresseIntentHandler(AbstractRequestHandler):
    """Handler for SetIpAdresseIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("SetIpAdresseIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        if "ipAdresse" in slots and slots["ipAdresse"].value:
            ip_adresse = slots["ipAdresse"].value
            speech_text = f"Deine IP-Adresse ist {ip_adresse}. Nun kannst du deine Schiffe auf dem Spielfeld platzieren oder sag 'Schiffe zufällig platzieren', um die Schiffe per Zufall auf dem Spielfeld zu verteilen."
        else:
            speech_text = "Entschuldigung, ich habe die IP-Adresse nicht verstanden. Bitte wiederhole sie."

        return handler_input.response_builder.speak(speech_text).ask(speech_text).response


# Handler for SchiffeRandomPlatzierenIntent
class SchiffeRandomPlatzierenIntentHandler(AbstractRequestHandler):
    """Handler for SchiffeRandomPlatzierenIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("SchiffeRandomPlatzierenIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Die Schiffe wurden zufällig platziert. Was möchtest du nun tun?"
        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )


# Handler for SpielStartenIntent
class SpielStartenIntentHandler(AbstractRequestHandler):
    """Handler for SpielStartenIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("SpielStartenIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Das Spiel wird gestartet. Viel Spaß beim Spielen!"
        return (
            handler_input.response_builder
            .speak(speech_text)
            .response
        )

    # Handler for SetSpielzugIntent


class SetSpielzugIntentHandler(AbstractRequestHandler):
    """Handler for SetSpielzugIntent."""

    def can_handle(self, handler_input):
        return is_intent_name("SetSpielzugIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        if "spielfeld" in slots and slots["spielfeld"].value:
            spielfeld = slots["spielfeld"].value
            speech_text = f"Spielzug auf Feld {spielfeld} wurde gesetzt."
        else:
            speech_text = "Entschuldigung, ich habe das Spielfeld nicht verstanden. Bitte wiederhole es."

        return handler_input.response_builder.speak(speech_text).ask(speech_text).response


# Default handlers for built-in intents
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Über die Spracheingabe kannst du den Spielmodus wählen, deine IP-Adresse setzen, Schiffe zufällig platzieren, einen Spielzug machen oder das Spiel neu starten."

        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )


class CancelAndStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
            handler_input)

    def handle(self, handler_input):
        speech_text = "Auf Wiedersehen!"

        return (
            handler_input.response_builder
            .speak(speech_text)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent."""

    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Entschuldigung, ich weiß nicht, wie ich dir helfen kann. Bitte versuche es noch einmal."

        return (
            handler_input.response_builder
            .speak(speech_text)
            .ask(speech_text)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The Intent Reflector is used for interaction model testing and debugging.
    It simply repeats the intent the user said. You can create custom handlers for your intents by defining them above, then also adding them to the list in the SkillBuilder initialization below.
    """

    def can_handle(self, handler_input):
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = f"Du hast den Intent {intent_name} ausgelöst."

        return (
            handler_input.response_builder
            .speak(speech_text)
            .response
        )


# Skill builder
sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SetSpielmodusIntentHandler())
sb.add_request_handler(SpielNeustartIntentHandler())
sb.add_request_handler(SetIpAdresseIntentHandler())
sb.add_request_handler(SchiffeRandomPlatzierenIntentHandler())
sb.add_request_handler(SpielStartenIntentHandler())
sb.add_request_handler(SetSpielzugIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler())

lambda_handler = sb.lambda_handler()
