CREATE TABLE IF NOT EXISTS user_events (
    id uuid primary key default gen_random_uuid(),
    event_type character varying(20) not null,
    user_id character varying(255) null,
    timestamp timestamp not null,
    session_id character varying(255) null,
    url text null,
    path character varying(500) null,
    title character varying(500) null,
    referrer text null,
    user_agent text null,
    screen_width integer null,
    screen_height integer null,
    target character varying(255) null,
    target_text text null,
    target_id character varying(255) null,
    target_class character varying(255) null,
    created_at timestamp default now()
);