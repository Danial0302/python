-- filepath: /Users/apple/Desktop/python_kbtu/practice8/function.sql
/*1_EXE*/
CREATE OR REPLACE FUNCTION find_name_or_phone(phbok text)
RETURNS TABLE(p_name VARCHAR,p_phone VARCHAR) as $$
BEGIN
    RETURN QUERY
    SELECT pb.name,pb.phone
    FROM phonebook_pr8 pb
    WHERE pb.name ILIKE '%' ||phbok|| '%'
    OR pb.phone ILIKE '%' ||phbok|| '%';
END;
$$ LANGUAGE plpgsql;

/*2_EXE - Upsert single contact*/
CREATE OR REPLACE FUNCTION upsert_contact(p_name TEXT, p_phone TEXT)
RETURNS VOID AS $$
BEGIN
    INSERT INTO phonebook_pr8 (name, phone) 
    VALUES (p_name, p_phone)
    ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
END;
$$ LANGUAGE plpgsql;

/*3-exe*/
CREATE OR REPLACE FUNCTION insert_many_users(names_arr TEXT[], phones_arr TEXT[])
RETURNS TABLE(err_name TEXT, err_phone TEXT) AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1..array_length(names_arr, 1) LOOP
        IF length(phones_arr[i]) = 11 AND phones_arr[i] ~ '^[0-9]+$' THEN
            INSERT INTO phonebook_pr8 (name, phone) 
            VALUES (names_arr[i], phones_arr[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            err_name := names_arr[i];
            err_phone := phones_arr[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

/*4_exe*/
CREATE OR REPLACE FUNCTION get_contact_pages(p_limit INT,p_offset INT)
RETURNS TABLE (name VARCHAR,phone VARCHAR) AS $$
BEGIN 
    RETURN QUERY
    SELECT phb.name,phb.phone FROM phonebook_pr8 phb
    ORDER BY phb.name LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

/*5_EXE - Delete contact by name or phone*/
CREATE OR REPLACE FUNCTION delete_contact(identifier TEXT)
RETURNS VOID AS $$
BEGIN
    DELETE FROM phonebook_pr8 
    WHERE name = identifier OR phone = identifier;
END;
$$ LANGUAGE plpgsql;