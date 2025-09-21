export interface Narrative {
    title: string;
    story: string;
    audience_segment: string;
}

export interface Opportunity {
    title: string;
    description: string;
    trend_momentum: number;
    days_to_event: number;
}

export interface Scenario {
    title: string;
    description: string;
    feasibility_status: string;
    prep_checklist: string[];
}

export interface InsightsBundle {
    narratives: Narrative[];
    opportunities: Opportunity[];
    scenarios: Scenario[];
}

export interface ArtisanProfile {
    name: string;
    craft: string;
    lineage: string;
    voice_note_url: string;
}
