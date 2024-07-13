-- A stored procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    
    -- Declare cursor to iterate over all user IDs
    DECLARE user_cursor CURSOR FOR
    SELECT id FROM users;
    
    -- Declare a handler for when the cursor reaches the end
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN user_cursor;
    
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;
        
        -- Calculate the total weighted score and total weight for the current user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;
    
    CLOSE user_cursor;
END //

DELIMITER ;
