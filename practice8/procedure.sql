/*2_EXE*/
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR,p_phone VARCHAR)
as $$
BEGIN
    /*insert into phonebook_pr8 (name,phone) values (p_name,p_phone)*/
    IF EXISTS (SELECT 1 FROM phonebook_pr8 WHERE name = p_name) THEN
        UPDATE phonebook_pr8 SET phone=p_phone WHERE name=p_name;
    ELSE
        insert into phonebook_pr8 (name,phone) values (p_name,p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;
/*5-EXE*/
CREATE OR REPLACE PROCEDURE delete_contact(p_search TEXT)
AS $$
BEGIN
    delete from phonebook_pr8
    where name = p_search OR phone = p_search;
END;
$$ LANGUAGE plpgsql;