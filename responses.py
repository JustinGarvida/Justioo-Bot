from random import choice, randint


def get_response(user_input: str) -> str:
   lowered: str = user_input.lower()
   if lowered == " ":
       return "Are you there?"
   elif 'bye' in lowered:
       return "Bye!"
   elif "roll dice" in lowered:
       return f'You rolled {randint(1,6)}'
   else:
       return;
