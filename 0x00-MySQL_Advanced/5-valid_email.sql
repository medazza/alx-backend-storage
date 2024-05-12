-- Creates a trigger that resets the attribute valid_email
-- only when the email has been changed.

DROP TRIGGER IF EXISTS reset_email;
DELIMITER //
CREATE TRIGGER reset_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.reset_email = 0;
    ELSE
        SET NEW.reset_email = NEW.reset_email;
    END IF;
END //
DELIMITER ;
