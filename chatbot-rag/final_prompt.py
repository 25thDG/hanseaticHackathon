import streamlit as st

def object_summary():
    return f"Das Wohngebäude wurde {st.session_state['YEAR']} erbaut und wird mittels einer {st.session_state['FUEL']} beheizt. Diese Heizung wurde 1996 in Betrieb genommen und läuft mit Gas. Das Wohngebäude verfügt über {st.session_state['INSULATION']} aktuelle Dämmung und Fenster mit Zweifachverglasung. Der Energiebedarf beträgt {st.session_state['KWH']} kWh für eine Wohnfläche von 160 qm, die über 3 Etagen verteilt ist."

# Queries

def year_query():
    return f"Wohngebäude aus dem Jahr {st.session_state['YEAR']}."

def heating_query():
    return f"??? {st.session_state['FUEL']} {st.session_state['KWH']}."

def insulation_query():
    return f"??? {st.session_state['INSULATION']}."

# Prompts

def year_prompt():
    return f"Fasse alle relevanten Textpassagen zusammen, die sich mit folgenden Informationen befassen: {object_summary()}\nFasse die Ergebnisse in leicht verständlicher Sprache zusammen."

def heating_prompt():
    return f"Fasse alle relevanten Textpassagen zusammen, die sich mit folgenden Informationen befassen: {object_summary()}\nFasse die Ergebnisse in leicht verständlicher Sprache zusammen."

def insulation_prompt():
    return f"Fasse alle relevanten Textpassagen zusammen, die sich mit folgenden Informationen befassen: {object_summary()}\nFasse die Ergebnisse in leicht verständlicher Sprache zusammen."

def final_prompt():
    return f"Es geht um folgendes Gebäude, für das ein Sanierungskonzept erstellt werden soll: {object_summary()}. Ersetze dazu in dem folgenden Template jeweils die Textpassagen in []. Hier kommt das Template: Einleitung: [schreibe eine passende Einleitung] Zusammenfassung: [fasse die Eckdaten des Gebäudes in tabellarischer Form zusammen] Maßnahmenkatalog: [wesentliche Sanierungsmaßnahmen]"
