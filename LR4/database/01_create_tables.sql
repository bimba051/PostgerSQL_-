-- Table: public.courses

-- DROP TABLE IF EXISTS public.courses;

CREATE TABLE IF NOT EXISTS public.courses
(
    course_id integer NOT NULL DEFAULT nextval('courses_course_id_seq'::regclass),
    course_name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    credits integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT courses_pkey PRIMARY KEY (course_id),
    CONSTRAINT courses_credits_check CHECK (credits > 0)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.courses
    OWNER to postgres;
-- Index: idx_courses_course_name

-- DROP INDEX IF EXISTS public.idx_courses_course_name;

CREATE INDEX IF NOT EXISTS idx_courses_course_name
    ON public.courses USING btree
    (course_name COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;
-- Index: idx_courses_credits

-- DROP INDEX IF EXISTS public.idx_courses_credits;

CREATE INDEX IF NOT EXISTS idx_courses_credits
    ON public.courses USING btree
    (credits ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;



-- Table: public.enrollment_audit

-- DROP TABLE IF EXISTS public.enrollment_audit;

CREATE TABLE IF NOT EXISTS public.enrollment_audit
(
    audit_id integer NOT NULL DEFAULT nextval('enrollment_audit_audit_id_seq'::regclass),
    student_id integer,
    course_id integer,
    operation character varying(10) COLLATE pg_catalog."default",
    old_grade integer,
    new_grade integer,
    changed_by character varying(50) COLLATE pg_catalog."default",
    changed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT enrollment_audit_pkey PRIMARY KEY (audit_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.enrollment_audit
    OWNER to postgres;




-- Table: public.enrollments

-- DROP TABLE IF EXISTS public.enrollments;

CREATE TABLE IF NOT EXISTS public.enrollments
(
    enrollment_id integer NOT NULL DEFAULT nextval('enrollments_enrollment_id_seq'::regclass),
    student_id integer NOT NULL,
    course_id integer NOT NULL,
    grade numeric(4,2),
    CONSTRAINT enrollments_pkey PRIMARY KEY (enrollment_id),
    CONSTRAINT enrollments_course_id_fkey FOREIGN KEY (course_id)
        REFERENCES public.courses (course_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT enrollments_student_id_fkey FOREIGN KEY (student_id)
        REFERENCES public.students (student_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT enrollments_grade_check CHECK (grade >= 0::numeric AND grade <= 100::numeric)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.enrollments
    OWNER to postgres;

-- Trigger: enrollment_grade_audit

-- DROP TRIGGER IF EXISTS enrollment_grade_audit ON public.enrollments;

CREATE OR REPLACE TRIGGER enrollment_grade_audit
    AFTER UPDATE 
    ON public.enrollments
    FOR EACH ROW
    EXECUTE FUNCTION public.log_enrollment_grade_change();

-- Trigger: validate_enrollment_before_insert

-- DROP TRIGGER IF EXISTS validate_enrollment_before_insert ON public.enrollments;

CREATE OR REPLACE TRIGGER validate_enrollment_before_insert
    BEFORE INSERT OR UPDATE 
    ON public.enrollments
    FOR EACH ROW
    EXECUTE FUNCTION public.validate_enrollment_data();




-- Table: public.students

-- DROP TABLE IF EXISTS public.students;

CREATE TABLE IF NOT EXISTS public.students
(
    student_id integer NOT NULL DEFAULT nextval('students_student_id_seq'::regclass),
    first_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    last_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    birth_date date,
    group_name character varying(20) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT students_pkey PRIMARY KEY (student_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.students
    OWNER to postgres;
-- Index: idx_students_last_name

-- DROP INDEX IF EXISTS public.idx_students_last_name;

CREATE INDEX IF NOT EXISTS idx_students_last_name
    ON public.students USING btree
    (last_name COLLATE pg_catalog."default" ASC NULLS LAST)
    WITH (fillfactor=100, deduplicate_items=True)
    TABLESPACE pg_default;

-- Trigger: student_modified_timestamp

-- DROP TRIGGER IF EXISTS student_modified_timestamp ON public.students;

CREATE OR REPLACE TRIGGER student_modified_timestamp
    BEFORE UPDATE 
    ON public.students
    FOR EACH ROW
    EXECUTE FUNCTION public.update_student_timestamp();