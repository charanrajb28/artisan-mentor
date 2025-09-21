from typing import List, Dict

class SignalsService:
    def get_evidence_chips(self, craft_profile: dict, signals: dict) -> List[str]:
        chips = []
        # Example implementation based on roadmap
        if signals.get('momentum_4w', 0) > 0:
            chips.append(f"+{signals['momentum_4w']}% 4-week momentum")
        if signals.get('days_to_event', 999) <= 30:
            # Assuming 'event_name' is available in signals for this chip
            event_name = signals.get('event_name', 'an event')
            chips.append(f"{signals['days_to_event']} days to {event_name}")
        return chips

    # Placeholder for other signal processing functions if needed
    def process_signals(self, data: Dict) -> Dict:
        # This would be where more complex signal processing happens
        # For now, just return the input data
        return data
