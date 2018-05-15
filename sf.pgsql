--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.12
-- Dumped by pg_dump version 9.5.12

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: forums; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.forums (
    forum_id integer NOT NULL,
    forum_name character varying(256),
    forum_type character varying(64),
    forum_desc character varying(256),
    created_by character varying(128),
    parent_forum_id integer
);


ALTER TABLE public.forums OWNER TO "user";

--
-- Name: forums_forum_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.forums_forum_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.forums_forum_id_seq OWNER TO "user";

--
-- Name: forums_forum_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.forums_forum_id_seq OWNED BY public.forums.forum_id;


--
-- Name: incidents; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.incidents (
    incident_id integer NOT NULL,
    police_dept_id integer,
    source_id integer,
    user_id integer,
    inc_type character varying(64),
    latitude character varying(256),
    longitude character varying(256),
    address character varying(512),
    city character varying(256),
    state character varying(256),
    date timestamp without time zone,
    year integer,
    "time" character varying(256),
    description character varying(4096),
    police_rec_num character varying(256) NOT NULL,
    cop_name character varying(256),
    cop_badge character varying(256),
    cop_desc character varying(1024),
    cop_pic character varying(256),
    sting_strat character varying(2048),
    avoidance character varying(2048),
    other character varying(2047),
    db_added_date timestamp without time zone
);


ALTER TABLE public.incidents OWNER TO "user";

--
-- Name: incidents_incident_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.incidents_incident_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.incidents_incident_id_seq OWNER TO "user";

--
-- Name: incidents_incident_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.incidents_incident_id_seq OWNED BY public.incidents.incident_id;


--
-- Name: police; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.police (
    police_dept_id integer NOT NULL,
    name character varying(512),
    city character varying(256),
    state character varying(128)
);


ALTER TABLE public.police OWNER TO "user";

--
-- Name: police_police_dept_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.police_police_dept_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.police_police_dept_id_seq OWNER TO "user";

--
-- Name: police_police_dept_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.police_police_dept_id_seq OWNED BY public.police.police_dept_id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.posts (
    post_id integer NOT NULL,
    user_id integer,
    username character varying(64),
    forum_id integer,
    parent_post_id integer,
    content character varying(4096),
    p_datetime timestamp without time zone,
    edit_datetime timestamp without time zone,
    like_num integer,
    dislike_num integer
);


ALTER TABLE public.posts OWNER TO "user";

--
-- Name: posts_post_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.posts_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.posts_post_id_seq OWNER TO "user";

--
-- Name: posts_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.posts_post_id_seq OWNED BY public.posts.post_id;


--
-- Name: sources; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.sources (
    source_id integer NOT NULL,
    police_dept_id integer,
    s_name character varying(256),
    s_description character varying(512),
    s_notes character varying(1024),
    url character varying(256),
    s_type character varying(128)
);


ALTER TABLE public.sources OWNER TO "user";

--
-- Name: sources_source_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.sources_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sources_source_id_seq OWNER TO "user";

--
-- Name: sources_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.sources_source_id_seq OWNED BY public.sources.source_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    password character varying(64),
    username character varying(64),
    fname character varying(64),
    lname character varying(64),
    email character varying(256),
    description character varying(512),
    picture character varying(256),
    created_at timestamp without time zone,
    edited_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO "user";

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: forum_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.forums ALTER COLUMN forum_id SET DEFAULT nextval('public.forums_forum_id_seq'::regclass);


--
-- Name: incident_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.incidents ALTER COLUMN incident_id SET DEFAULT nextval('public.incidents_incident_id_seq'::regclass);


--
-- Name: police_dept_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.police ALTER COLUMN police_dept_id SET DEFAULT nextval('public.police_police_dept_id_seq'::regclass);


--
-- Name: post_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.posts ALTER COLUMN post_id SET DEFAULT nextval('public.posts_post_id_seq'::regclass);


--
-- Name: source_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.sources ALTER COLUMN source_id SET DEFAULT nextval('public.sources_source_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: forums; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.forums (forum_id, forum_name, forum_type, forum_desc, created_by, parent_forum_id) FROM stdin;
\.


--
-- Name: forums_forum_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.forums_forum_id_seq', 1, false);


--
-- Data for Name: incidents; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.incidents (incident_id, police_dept_id, source_id, user_id, inc_type, latitude, longitude, address, city, state, date, year, "time", description, police_rec_num, cop_name, cop_badge, cop_desc, cop_pic, sting_strat, avoidance, other, db_added_date) FROM stdin;
\.


--
-- Name: incidents_incident_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.incidents_incident_id_seq', 1, false);


--
-- Data for Name: police; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.police (police_dept_id, name, city, state) FROM stdin;
1	User_Input	\N	\N
2	San Franciso Police Department	San Francisco	CA
3	Oakland Police Department	Oakland	CA
\.


--
-- Name: police_police_dept_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.police_police_dept_id_seq', 1, false);


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.posts (post_id, user_id, username, forum_id, parent_post_id, content, p_datetime, edit_datetime, like_num, dislike_num) FROM stdin;
\.


--
-- Name: posts_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.posts_post_id_seq', 1, false);


--
-- Data for Name: sources; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.sources (source_id, police_dept_id, s_name, s_description, s_notes, url, s_type) FROM stdin;
3	2	DataSF	San Franciso Police API	Much of the pre-2015 data is well reported, but the data from recent years are extremely poorly and sporatically reported.	https://data.sfgov.org/resource/cuks-n6tp.json	gov api
2	2	DataSF	San Franciso Police API	Much of the pre-2015 data is well reported, but the data from recent years are extremely poorly and sporatically reported.	https://data.sfgov.org/resource/PdId.json	gov api
1	\N	User_report	\N	\N	\N	\N
4	3	oaklandnet_90_days	Oakland Police API Last 90 Days	Oakland only has the last 90 days available at any given time. SafeWork will do its best to stay updated, but there will be minimal data from pre-2018.	ftp://crimewatchdata.oaklandnet.com/crimePublicData.csv	gov api
\.


--
-- Name: sources_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.sources_source_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.users (user_id, password, username, fname, lname, email, description, picture, created_at, edited_at) FROM stdin;
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: forums_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.forums
    ADD CONSTRAINT forums_pkey PRIMARY KEY (forum_id);


--
-- Name: incidents_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT incidents_pkey PRIMARY KEY (incident_id);


--
-- Name: police_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.police
    ADD CONSTRAINT police_pkey PRIMARY KEY (police_dept_id);


--
-- Name: posts_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (post_id);


--
-- Name: sources_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_pkey PRIMARY KEY (source_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: forums_parent_forum_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.forums
    ADD CONSTRAINT forums_parent_forum_id_fkey FOREIGN KEY (parent_forum_id) REFERENCES public.forums(forum_id);


--
-- Name: incidents_police_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT incidents_police_dept_id_fkey FOREIGN KEY (police_dept_id) REFERENCES public.police(police_dept_id);


--
-- Name: incidents_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT incidents_source_id_fkey FOREIGN KEY (source_id) REFERENCES public.sources(source_id);


--
-- Name: incidents_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.incidents
    ADD CONSTRAINT incidents_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: posts_forum_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_forum_id_fkey FOREIGN KEY (forum_id) REFERENCES public.forums(forum_id);


--
-- Name: posts_parent_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_parent_post_id_fkey FOREIGN KEY (parent_post_id) REFERENCES public.posts(post_id);


--
-- Name: posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: sources_police_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.sources
    ADD CONSTRAINT sources_police_dept_id_fkey FOREIGN KEY (police_dept_id) REFERENCES public.police(police_dept_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

